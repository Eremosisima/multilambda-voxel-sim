#!/usr/bin/env python3
"""Realistic-ish OpenVINO graph traces and memory policy simulation (conceptual).
Extends S3 runtime traces with memory placement/reuse policies and reference-informed op mixes.
"""
from __future__ import annotations
import csv,json,os,math,copy
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
ref={}
rp=os.path.join('data','reference_params_supplement.json')
if os.path.exists(rp): ref=json.load(open(rp,encoding='utf-8'))
S3=json.load(open(os.path.join(OUT,'s3_pcie_openvino.json'),encoding='utf-8'))

op_support={o['op']:o['opgpu_offloadable'] for o in S3['openvino']['operator_support_initial']}
impl={'A_native':0.95,'B_opencl':0.80,'C_hetero':0.70,'D_compiled':0.75}
fallback_penalty={'A_native':1.15,'B_opencl':1.20,'C_hetero':1.35,'D_compiled':1.10}
ROUTE_LABEL={r['route']:r['route_label'] for r in S3.get('openvino_partition_results',[])}

# More realistic traces: layers/ops with tensor sizes and reuse
TRACES=[
 {'name':'ResNet50_infer','graph':'CNN_inference','seq':[
  ('Convolution',2.1,512,256,1.0),('Activation (ReLU/GELU approx)',0.2,0,0,0.8),('Add/Mul (eltwise)',0.15,256,0,0.6),
  ('Convolution',1.8,256,256,1.0),('Activation (ReLU/GELU approx)',0.18,0,0,0.8),('Convolution',1.5,256,128,0.9),
  ('Add/Mul (eltwise)',0.12,128,0,0.6),('FullyConnected',0.35,64,32,0.7),('MatMul/GEMM',0.25,32,16,0.8),('Quantize/Dequantize',0.08,16,16,0.9)
 ]},
 {'name':'BERT_base_block','graph':'Transformer_encoder_block','seq':[
  ('MatMul/GEMM',1.3,512,256,0.9),('Attention (compuesto)',2.2,256,256,0.6),('Softmax/LayerNorm',1.1,128,128,0.3),
  ('Add/Mul (eltwise)',0.25,128,0,0.7),('FullyConnected',0.9,256,128,0.9),('Activation (ReLU/GELU approx)',0.12,0,0,0.8),
  ('FullyConnected',0.85,128,128,0.9),('MatMul/GEMM',0.6,128,64,0.9),('Quantize/Dequantize',0.1,64,64,0.9)
 ]},
 {'name':'MLP_recommender','graph':'MLP_classifier','seq':[
  ('FullyConnected',0.7,128,64,0.9),('Activation (ReLU/GELU approx)',0.1,0,0,0.8),('FullyConnected',0.6,64,64,0.9),
  ('Add/Mul (eltwise)',0.08,64,0,0.7),('FullyConnected',0.4,64,32,0.9),('MatMul/GEMM',0.3,32,16,0.9),('Quantize/Dequantize',0.05,16,16,0.9)
 ]},
 {'name':'ViT_patch_head','graph':'Transformer_encoder_block','seq':[
  ('Convolution',1.0,512,256,0.95),('MatMul/GEMM',1.4,256,256,0.9),('Attention (compuesto)',1.8,256,256,0.6),
  ('Softmax/LayerNorm',0.9,128,128,0.3),('FullyConnected',0.6,128,64,0.9),('Activation (ReLU/GELU approx)',0.1,0,0,0.8),('MatMul/GEMM',0.4,64,32,0.9)
 ]},
]
MEM_POLICIES=[
 {'name':'host_staging','reuse':0.0,'h2d_factor':1.0,'d2h_factor':1.0,'lat_penalty':1.15,'desc':'weights/acts staged from host each subgraph'},
 {'name':'device_resident_weights','reuse':0.4,'h2d_factor':0.55,'d2h_factor':1.0,'lat_penalty':1.02,'desc':'weights persistent on device/NV, activations streamed'},
 {'name':'tiling_reuse','reuse':0.55,'h2d_factor':0.7,'d2h_factor':0.8,'lat_penalty':1.05,'desc':'tile/block reuse reduces transfers'},
 {'name':'full_on_device_pipeline','reuse':0.75,'h2d_factor':0.35,'d2h_factor':0.6,'lat_penalty':1.0,'desc':'max reuse, pipeline across layers (when memory fits)'},
]
ROUTES=['C_hetero','D_compiled','B_opencl','A_native']
PCIE_GBPS=13.1
def copy_ms(kb,factor):
    if kb<=0: return 0.0
    return (kb*factor*1024*8)/(PCIE_GBPS*1e9)*1e3 + 0.002
rows=[]
for t in TRACES:
    for route in ROUTES:
        for pol in MEM_POLICIES:
            off_ms=fb_ms=cpy=0.0; off_sum=0.0; n=0
            for op,ms,h2d,d2h,reuse_local in t['seq']:
                cov=min(1.0, op_support.get(op,0.0)*impl[route])
                eff_reuse=min(0.95, pol['reuse']*reuse_local + (0.15 if cov>0.7 else 0.0))
                opgpu_part=ms*cov*0.55
                fb_part=ms*(1-cov)*fallback_penalty[route]
                h2d_eff=h2d*pol['h2d_factor']*(1-eff_reuse*0.6)
                d2h_eff=d2h*pol['d2h_factor']*(1-eff_reuse*0.4)
                cpy += copy_ms(h2d_eff,1.0)+copy_ms(d2h_eff,1.0)
                off_ms+=opgpu_part; fb_ms+=fb_part; off_sum+=cov; n+=1
            compute=(off_ms+fb_ms)*pol['lat_penalty']
            overlap=0.3*min(cpy,compute)
            e2e=max(0.05, compute+cpy-overlap)
            rows.append({'trace':t['name'],'graph':t['graph'],'route':route,'route_label':ROUTE_LABEL.get(route,route),
                         'memory_policy':pol['name'],'policy_desc':pol['desc'],
                         'offload_cov_avg':round(off_sum/n,4),'compute_ms':round(compute,4),'copy_ms':round(cpy,4),
                         'overlap_ms':round(overlap,4),'e2e_ms':round(e2e,4)})

summary=[]
for t in TRACES:
    for cls,rset in [('near_term',('C_hetero','D_compiled')),('target',('A_native','B_opencl'))]:
        sub=[r for r in rows if r['trace']==t['name'] and r['route'] in rset]
        best=min(sub,key=lambda x:x['e2e_ms'])
        summary.append({'trace':t['name'],'class':cls,'best_route':best['route_label'],'best_memory_policy':best['memory_policy'],'e2e_ms':best['e2e_ms'],'coverage':best['offload_cov_avg'],'copy_ms':best['copy_ms']})

out={'rows':rows,'summary':summary,'memory_policies':MEM_POLICIES,'reference':ref.get('openvino_graph_profiles_reference'),'note':'Conceptual realistic-trace + memory-policy simulation; calibrate with real OpenVINO IR graphs, tensor sizes and device memory map.'}
json.dump(out,open(os.path.join(OUT,'openvino_realistic_traces.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'openvino_realistic_traces.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Trazas OpenVINO más realistas y políticas de memoria (conceptual)','',
    '> Extiende S3 con secuencias tipo ResNet50/BERT/MLP/ViT, reutilización y políticas de colocación de memoria (host, pesos residentes, tiling, pipeline on-device).','',
    '## Mejores resultados por traza','',
    '| Traza | Horizonte | Mejor ruta | Mejor política memoria | Cobertura | Copias (ms) | E2E (ms) |','|---|---|---|---|---:|---:|---:|']
for s in summary:
    md.append(f"| {s['trace']} | {s['class']} | {s['best_route']} | {s['best_memory_policy']} | {s['coverage']} | {s['copy_ms']} | {s['e2e_ms']} |")
md+=['','## Lectura','- Políticas con pesos residentes/tiling/pipeline on-device reducen copias H2D/D2H y E2E, especialmente en CNN/MLP; Transformer sigue penalizado por fallback en atención/softmax/norm.','- La memoria NV (PCM, M1/M3) favorece `device_resident_weights` y reduce tráfico PCIe; requiere gestión de coherencia y actualización térmicamente limitada.','- Calibrar con grafos IR reales, tamaños de tensores, layout DMA y mapa de memoria M0–M3/host.']
open(os.path.join(OUT,'openvino_realistic_traces.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    traces=[t['name'] for t in TRACES]; x=range(len(traces)); w=0.18
    pols=['host_staging','device_resident_weights','tiling_reuse','full_on_device_pipeline']
    fig,ax=plt.subplots(figsize=(9,4))
    for i,p in enumerate(pols):
        vals=[next(r['e2e_ms'] for r in rows if r['trace']==t and r['route']=='C_hetero' and r['memory_policy']==p) for t in traces]
        ax.bar([xi+(i-1.5)*w for xi in x], vals, w, label=p)
    ax.set_xticks(list(x)); ax.set_xticklabels(traces, rotation=10); ax.set_ylabel('E2E (ms)')
    ax.set_title('Trazas realistas: E2E por política de memoria (ruta C)'); ax.legend(fontsize=7,ncol=2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG,'openvino_realistic_traces.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/openvino_realistic_traces.*'}))
