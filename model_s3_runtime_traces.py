#!/usr/bin/env python3
"""S3 extension: functional runtime simulation over representative graph traces.
Models partition/fallback (A-D), H2D/D2H copies, queue/batch scheduling, DMA channels.
Conceptual (no RTL/driver traces).
"""
from __future__ import annotations
import csv,json,os,math,random
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
random.seed(7)

# load S3 partition coverage and base latencies
S3=json.load(open(os.path.join(OUT,'s3_pcie_openvino.json'),encoding='utf-8'))
part=S3.get('openvino_partition_results',[])
# representative traces (op sequences with compute/transfer weights)
TRACES=[
 {'name':'CNN_inference_trace','graph':'CNN_inference','ops':[
   {'op':'Convolution','ms':1.2,'h2d_kb':256,'d2h_kb':128},
   {'op':'Activation (ReLU/GELU approx)','ms':0.15,'h2d_kb':0,'d2h_kb':0},
   {'op':'Add/Mul (eltwise)','ms':0.12,'h2d_kb':0,'d2h_kb':0},
   {'op':'Convolution','ms':1.1,'h2d_kb':128,'d2h_kb':128},
   {'op':'MatMul/GEMM','ms':0.3,'h2d_kb':64,'d2h_kb':32},
   {'op':'FullyConnected','ms':0.25,'h2d_kb':32,'d2h_kb':16},
 ]},
 {'name':'MLP_classifier_trace','graph':'MLP_classifier','ops':[
   {'op':'FullyConnected','ms':0.5,'h2d_kb':64,'d2h_kb':32},
   {'op':'Activation (ReLU/GELU approx)','ms':0.08,'h2d_kb':0,'d2h_kb':0},
   {'op':'FullyConnected','ms':0.45,'h2d_kb':32,'d2h_kb':32},
   {'op':'MatMul/GEMM','ms':0.2,'h2d_kb':16,'d2h_kb':16},
 ]},
 {'name':'Transformer_block_trace','graph':'Transformer_encoder_block','ops':[
   {'op':'MatMul/GEMM','ms':1.0,'h2d_kb':256,'d2h_kb':128},
   {'op':'Attention (compuesto)','ms':1.6,'h2d_kb':128,'d2h_kb':128},
   {'op':'Softmax/LayerNorm','ms':0.9,'h2d_kb':64,'d2h_kb':64},
   {'op':'Add/Mul (eltwise)','ms':0.2,'h2d_kb':0,'d2h_kb':0},
   {'op':'FullyConnected','ms':0.7,'h2d_kb':128,'d2h_kb':64},
   {'op':'Activation (ReLU/GELU approx)','ms':0.1,'h2d_kb':0,'d2h_kb':0},
 ]},
]
ROUTES=['C_hetero','D_compiled','B_opencl','A_native']
ROUTE_LABEL={r['route']:r['route_label'] for r in part}
# op offloadability already in S3 model; approximate per-route impl factor via coverage ratio
op_support={o['op']:o['opgpu_offloadable'] for o in S3['openvino']['operator_support_initial']}
impl={'A_native':0.95,'B_opencl':0.80,'C_hetero':0.70,'D_compiled':0.75}
fallback_penalty={'A_native':1.15,'B_opencl':1.20,'C_hetero':1.35,'D_compiled':1.10}
# PCIe/DMA params (Gen4 x8 conceptual)
PCIE_GBPS=13.1; DMA_CH=2; COPY_SETUP_MS=0.003
QUEUE_CFGS=[{'name':'single','depth':1,'batch':1,'coalesce':1,'dma':1},
            {'name':'pipelined','depth':8,'batch':1,'coalesce':2,'dma':2},
            {'name':'batched','depth':16,'batch':4,'coalesce':4,'dma':2}]

def copy_ms(kb,dma):
    if kb<=0: return 0.0
    eff=PCIE_GBPS*(1.0-0.05*max(0,1-dma)) # small penalty if 1 channel
    return (kb*1024*8)/(eff*1e9)*1e3 + COPY_SETUP_MS

def run_trace(trace, route, q):
    # partition ops: offloaded portion runs on OPGPU (faster proxy) else fallback CPU
    total=0.0; off_ms=0.0; fb_ms=0.0; copy=0.0; offloaded=0.0; count=len(trace['ops'])
    for op in trace['ops']:
        cov=min(1.0, op_support.get(op['op'],0.0)*impl[route])
        # compute split
        opgpu_part=op['ms']*cov*0.55 # optical accel proxy
        fb_part=op['ms']*(1-cov)*fallback_penalty[route]
        off_ms+=opgpu_part; fb_ms+=fb_part
        offloaded+=cov
        # copies for offloaded portion (overlap partly in pipelined/batched)
        c=(copy_ms(op['h2d_kb'],q['dma'])+copy_ms(op['d2h_kb'],q['dma']))*(0.6+0.4*cov)
        copy+=c
    base_compute=off_ms+fb_ms
    overlap=0.25*min(copy,base_compute) if q['depth']>=8 else 0.05*min(copy,base_compute)
    batch_gain=0.18*math.log2(max(1,q['batch'])) if q['batch']>1 else 0.0
    service=max(0.05, base_compute+copy-overlap)*(1.0-batch_gain)
    # queueing approximation
    util=min(0.97, 0.4 + 0.15*(q['batch']/4.0) + (0.08 if trace['graph']=='Transformer_encoder_block' else 0.03))
    qwait = 0.0 if util>=0.999 else service*(util/(1-util))*0.35
    e2e=service+qwait*(0.85 if q['coalesce']>=2 else 1.0)
    cov_avg=offloaded/count
    return {'trace':trace['name'],'graph':trace['graph'],'route':route,'route_label':ROUTE_LABEL.get(route,route),
            'queue_cfg':q['name'],'batch':q['batch'],'dma_channels':q['dma'],
            'offload_coverage_avg':round(cov_avg,4),'opgpu_compute_ms':round(off_ms,4),'fallback_compute_ms':round(fb_ms,4),
            'copy_ms':round(copy,4),'service_ms':round(service,4),'queue_wait_ms':round(qwait,4),'e2e_ms':round(e2e,4)}

rows=[]
for t in TRACES:
    for r in ROUTES:
        for q in QUEUE_CFGS:
            rows.append(run_trace(t,r,q))

# summary best per trace/route-class
summary=[]
for t in TRACES:
    for cls,name,rset in [('near_term','C/D',('C_hetero','D_compiled')),('target','A/B',('A_native','B_opencl'))]:
        best=min([x for x in rows if x['trace']==t['name'] and x['route'] in rset and x['queue_cfg'] in ('pipelined','batched')], key=lambda x:x['e2e_ms'])
        summary.append({'trace':t['name'],'class':cls,'best_route':best['route_label'],'best_queue':best['queue_cfg'],'e2e_ms':best['e2e_ms'],'coverage':best['offload_coverage_avg'],'fallback_ms':best['fallback_compute_ms']})

out={'rows':rows,'best_summary':summary,'assumptions':{'pcie_gbps_eff':PCIE_GBPS,'dma_channels_options':[1,2],'note':'Conceptual runtime trace simulation; validate with real OpenVINO graphs and driver/FPGA traces.'}}
json.dump(out,open(os.path.join(OUT,'s3_runtime_traces.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'s3_runtime_traces.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# S3 — Simulación funcional de runtime sobre trazas (partición/fallback, colas, copias)','',
    '> Conceptual (sin trazas reales de driver/RTL). Extiende S3 con secuencias de operadores, partición por ruta A–D y scheduling por colas/batching/DMA.','',
    '## Resumen (mejores configs por traza)','',
    '| Traza | Horizonte | Mejor ruta | Cola | Cobertura offload | Fallback (ms) | E2E (ms) |','|---|---|---|---|---:|---:|---:|']
for s in summary:
    md.append(f"| {s['trace']} | {s['class']} | {s['best_route']} | {s['best_queue']} | {s['coverage']} | {s['fallback_ms']} | {s['e2e_ms']} |")
md+=['','## Lectura','- CNN/MLP logran menor E2E y mayor cobertura efectiva en C/D (corto plazo) y mejor aún en A/B; Transformer mantiene mayor fracción en fallback (softmax/norm/attention) y se beneficia de batching/pipelining.','- Colas profundas + batching + coalescing reducen espera relativa; el coste H2D/D2H y fallback dominan cuando la partición es incompleta.','- Validar con grafos OpenVINO reales y trazas FPGA/driver para latencias y contención reales.']
open(os.path.join(OUT,'s3_runtime_traces.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    traces=[t['name'] for t in TRACES]; x=range(len(traces)); w=0.18
    def get(route,qcfg,field):
        return [next(r[field] for r in rows if r['trace']==t and r['route']==route and r['queue_cfg']==qcfg) for t in traces]
    fig,ax=plt.subplots(figsize=(8,4))
    ax.bar([i-1.5*w for i in x], get('C_hetero','batched','e2e_ms'), w, label='C batched')
    ax.bar([i-0.5*w for i in x], get('D_compiled','batched','e2e_ms'), w, label='D batched')
    ax.bar([i+0.5*w for i in x], get('B_opencl','batched','e2e_ms'), w, label='B batched')
    ax.bar([i+1.5*w for i in x], get('A_native','batched','e2e_ms'), w, label='A batched')
    ax.set_xticks(list(x)); ax.set_xticklabels([t.replace('_trace','') for t in traces], rotation=10)
    ax.set_ylabel('E2E (ms)'); ax.set_title('S3 runtime trazas: E2E por ruta (batched)'); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(FIG,'s3_runtime_traces.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/s3_runtime_traces.*'}))
