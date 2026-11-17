#!/usr/bin/env python3
"""S2: System performance profiles (edge/ws/dc) for M0-M3/OMCC across GPU/NPU/TPU modes.

Conceptual functional model extending simulate_opgpu_system assumptions.
Outputs: outputs/s2_system_profiles.{json,csv,md} and figures/s2_system_profiles.png
"""
from __future__ import annotations
import csv, json, os, statistics
import numpy as np
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except Exception:
    plt = None

from simulate_opgpu_system import (
    SystemConfig, Workload, simulate_workload, opencl_queue_sim,
    peak_tops, pcie_bandwidth_gbps
)

OUT='outputs'; FIG='figures'
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)

def profiles():
    # Deployment envelopes: edge (power/therm constrained), workstation, datacenter
    return {
        'edge': dict(pcie_lanes=8, pcie_gen_gbps_per_lane=32.0, tiles_base=32, wdm=8, batch=1, target_latency_ms=10, target_tops=8),
        'ws':   dict(pcie_lanes=16, pcie_gen_gbps_per_lane=32.0, tiles_base=64, wdm=8, batch=4, target_latency_ms=20, target_tops=20),
        'dc':   dict(pcie_lanes=16, pcie_gen_gbps_per_lane=64.0, tiles_base=128, wdm=16, batch=8, target_latency_ms=50, target_tops=80),
    }

def workloads_for_profile(batch):
    return [
        Workload('GEMM_infer', ops=2*(1024**3)*batch, bytes_in=2*1024*1024*2*batch, bytes_out=1024*1024*2*batch, weight_bytes=1024*1024*2, weight_reuse=1024*batch, m2_working_set_bytes=8*1024*1024, intensity_ops_per_byte=512.0),
        Workload('Conv_infer', ops=2*64*64*128*3*3*128*batch, bytes_in=64*64*128*batch, bytes_out=64*64*128*batch, weight_bytes=128*3*3*128, weight_reuse=4096*batch, m2_working_set_bytes=4*1024*1024, intensity_ops_per_byte=300.0),
        Workload('Attention_block', ops=2*(512**3)*2*max(1,batch//2), bytes_in=3*512*512*2*max(1,batch//2), bytes_out=512*512*2*max(1,batch//2), weight_bytes=3*512*512*2, weight_reuse=512*batch, m2_working_set_bytes=16*1024*1024, intensity_ops_per_byte=200.0),
        Workload('Mixed_stream', ops=2*(768**3)*batch, bytes_in=3*768*768*2*batch, bytes_out=768*768*2*batch, weight_bytes=2*768*768*2, weight_reuse=256*batch, m2_working_set_bytes=12*1024*1024, intensity_ops_per_byte=150.0),
    ]

def build_configs(pname, p):
    lanes=p['pcie_lanes']; gen=p['pcie_gen_gbps_per_lane']; tb=p['tiles_base']; wdm=p['wdm']
    common=dict(pcie_lanes=lanes, pcie_gen_gbps_per_lane=gen, wdm_channels=wdm, omcc_enabled=True, prefetch_overlap=0.72, output_overlap=0.52, omcc_arbitration_ns=40.0, omcc_verify_overhead=0.12, m1_persistent=True, pcm_calibrated=True, pcm_bits=5, pcm_il_db_avg=0.123, pcm_step_energy_pj=0.0031, thermal_margin_c=41.6, thermal_write_serialization=1.15)
    # edge more constrained thermally/utilization
    if pname=='edge':
        common.update(prefetch_overlap=0.68, output_overlap=0.48, thermal_write_serialization=1.2, m2_refresh_overhead=0.003)
    if pname=='dc':
        common.update(prefetch_overlap=0.78, output_overlap=0.58, omcc_arbitration_ns=36.0)
    return [
        SystemConfig(name=f'{pname}-GPU', mode='GPU', tiles=tb, macs_per_tile_per_cycle=4096, **{k:v for k,v in common.items()}),
        SystemConfig(name=f'{pname}-NPU', mode='NPU', tiles=tb, macs_per_tile_per_cycle=4096, energy_pj_per_mac=0.57, **{k:v for k,v in common.items()}),
        SystemConfig(name=f'{pname}-TPU', mode='TPU', tiles=tb*2 if pname!='edge' else tb, macs_per_tile_per_cycle=8192 if pname!='edge' else 4096, energy_pj_per_mac=0.47, **{k:v for k,v in common.items()}),
    ]

def main():
    profs=profiles(); rows=[]; summary={}
    for pname,p in profs.items():
        cfgs=build_configs(pname,p); wls=workloads_for_profile(p['batch'])
        q=opencl_queue_sim(events=64, omcc_enabled=True)
        pres=[]
        for c in cfgs:
            for w in wls:
                r=simulate_workload(c,w)
                r['profile']=pname; r['batch']=p['batch']; r['target_latency_ms']=p['target_latency_ms']; r['target_tops']=p['target_tops']
                r['meets_latency']=r['latency_ms']<=p['target_latency_ms']
                r['meets_tops']=r['runtime_tops_effective']>=p['target_tops']
                rows.append(r); pres.append(r)
        by_mode={}
        for r in pres:
            by_mode.setdefault(r['mode'], []).append(r)
        summary[pname]={
            'batch': p['batch'], 'targets': {'latency_ms': p['target_latency_ms'], 'tops': p['target_tops']},
            'avg_runtime_tops_by_mode': {m: round(statistics.mean([x['runtime_tops_effective'] for x in v]),3) for m,v in by_mode.items()},
            'avg_latency_ms_by_mode': {m: round(statistics.mean([x['latency_ms'] for x in v]),4) for m,v in by_mode.items()},
            'latency_target_pass_rate_by_mode': {m: round(sum(1 for x in v if x['meets_latency'])/len(v),3) for m,v in by_mode.items()},
            'tops_target_pass_rate_by_mode': {m: round(sum(1 for x in v if x['meets_tops'])/len(v),3) for m,v in by_mode.items()},
            'queue_p95_ms': round(q['p95_queue_ms'],4), 'queue_avg_ms': round(q['avg_queue_ms'],4),
            'best_case': min(pres, key=lambda x: x['latency_ms'])['config']+'/'+min(pres,key=lambda x:x['latency_ms'])['workload']
        }
    out={'profiles': summary, 'rows': rows, 'disclaimer':'Conceptual S2 model (not measurements/signoff). Uses simulate_opgpu_system functional/perf assumptions with edge/ws/dc envelopes and M0-M3/OMCC+P1 params.'}
    with open(os.path.join(OUT,'s2_system_profiles.json'),'w',encoding='utf-8') as f: json.dump(out,f,indent=2,ensure_ascii=False)
    keys=list(rows[0].keys())
    with open(os.path.join(OUT,'s2_system_profiles.csv'),'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    md=['# S2 — Perfiles de sistema (edge / workstation / datacenter)','',
        '> Modelo funcional/conceptual S2 (no mediciones). Extiende `simulate_opgpu_system.py` con envolventes edge/ws/dc, colas OMCC y parámetros M0–M3/OMCC+P1.','',
        '## Resumen por perfil','',
        '| Perfil | Batch | Objetivo lat (ms) | Objetivo TOPS | TOPS medio NPU | TOPS medio TPU | Lat media NPU (ms) | Lat media TPU (ms) | Pass lat NPU | Pass TOPS NPU | Pass TOPS TPU | Cola p95 (ms) |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in ['edge','ws','dc']:
        s=summary[p]
        md.append(f"| {p} | {s['batch']} | {s['targets']['latency_ms']} | {s['targets']['tops']} | {s['avg_runtime_tops_by_mode'].get('NPU')} | {s['avg_runtime_tops_by_mode'].get('TPU')} | {s['avg_latency_ms_by_mode'].get('NPU')} | {s['avg_latency_ms_by_mode'].get('TPU')} | {s['latency_target_pass_rate_by_mode'].get('NPU')} | {s['tops_target_pass_rate_by_mode'].get('NPU')} | {s['tops_target_pass_rate_by_mode'].get('TPU')} | {s['queue_p95_ms']} |")
    md+=['','## Lectura','- **Edge:** limitado por PCIe x8, tiles y restricciones térmicas; adecuado a inferencia con cargas de intensidad media/alta si se amortizan pesos (persistencia M1/OMCC).','- **Workstation:** balance latencia/throughput con batching moderado; ruta preferente para demo OpenCL/OpenVINO heterogénea (C/D→B).','- **Datacenter:** mayor techo de TOPS efectivos con Gen5/tiles/WDM y batching, sujeto a partición y a que cuellos de transferencia sean solapables.','- Brechas frente a objetivos deben cerrarse con S3 (colas/DMA reales, partición de grafo, cuantización/calibración) y validación E3.','',
         '## Artefactos','- `outputs/s2_system_profiles.json`, `outputs/s2_system_profiles.csv`, `figures/s2_system_profiles.png`']
    with open(os.path.join(OUT,'s2_system_profiles.md'),'w',encoding='utf-8') as f: f.write('\n'.join(md)+'\n')
    if plt:
        fig,axes=plt.subplots(1,2,figsize=(10,4))
        modes=['GPU','NPU','TPU']; x=np.arange(len(modes)); w=0.25
        for i,p in enumerate(['edge','ws','dc']):
            vals=[summary[p]['avg_runtime_tops_by_mode'].get(m,0) for m in modes]
            axes[0].bar(x+i*w, vals, w, label=p)
        axes[0].set_xticks(x+w); axes[0].set_xticklabels(modes); axes[0].set_title('TOPS efectivo medio por perfil/modo'); axes[0].set_ylabel('TOPS'); axes[0].legend()
        for i,p in enumerate(['edge','ws','dc']):
            vals=[summary[p]['avg_latency_ms_by_mode'].get(m,0) for m in modes]
            axes[1].bar(x+i*w, vals, w, label=p)
        axes[1].set_xticks(x+w); axes[1].set_xticklabels(modes); axes[1].set_title('Latencia media por perfil/modo'); axes[1].set_ylabel('ms'); axes[1].legend()
        fig.tight_layout(); fig.savefig(os.path.join(FIG,'s2_system_profiles.png'), dpi=150); plt.close(fig)
    print(json.dumps({'profiles': list(summary.keys()), 'rows': len(rows), 'out':'outputs/s2_system_profiles.*'}))

if __name__=='__main__':
    main()
