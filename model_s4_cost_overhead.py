#!/usr/bin/env python3
"""S4 follow-up: quantify redundancy/re-mapping cost (area, energy, latency, effective capacity)
for optimized candidate configurations. Conceptual (no measurements)."""
from __future__ import annotations
import csv, json, os, math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)

# Base candidate proxies (conceptual, from v0.8 metrics/objective analysis)
BASE = {
  'H3': {'name':'Open WDM-PCM (A1+G1+B3)','tops':3.5,'mem_mb':160,'bw_tbs':1.6,'area_cm2':40.0,'energy_pj_mac':0.57,'reconfig_s':2e-5},
  'G2': {'name':'Thin-film membrane stack (EO-tuned)','tops':5.5,'mem_mb':192,'bw_tbs':3.2,'area_cm2':30.0,'energy_pj_mac':0.35,'reconfig_s':1e-11},
  'G3': {'name':'Thin-film membrane stack (PCM+EO hybrid)','tops':5.0,'mem_mb':256,'bw_tbs':2.8,'area_cm2':32.0,'energy_pj_mac':0.50,'reconfig_s':5e-10},
  'H1': {'name':'Membrane-Brush NV (A1+G3+3D)','tops':9.0,'mem_mb':640,'bw_tbs':2.6,'area_cm2':100.0,'energy_pj_mac':0.55,'reconfig_s':1e-9},
  'H4': {'name':'Volumetric Tensor Membrane (G2/G3+F2+A1)','tops':10.0,'mem_mb':720,'bw_tbs':3.5,'area_cm2':90.0,'energy_pj_mac':0.52,'reconfig_s':5e-10},
}
# Optimized configs (aligned with model_s4_variability_yield.py best paths where available; G2 conceptual)
OPTS = {
  'H3': {'process':'Baseline process (current assumptions)','redundancy':0.14,'ecc_overhead':0.08,'calibration_eff':0.72,'raw_yield':1.0,'eff_yield':0.86,'remap_recovery_factor':0.55,'label':'Partitioned WDM tiles + closed-loop calibration + spare rings'},
  'G2': {'process':'Baseline process (current assumptions, EO)','redundancy':0.10,'ecc_overhead':0.06,'calibration_eff':0.80,'raw_yield':0.995,'eff_yield':0.8955,'remap_recovery_factor':0.60,'label':'EO trim + resonator stabilization + spare channels/drivers (no PCM write)'},
  'G3': {'process':'Baseline process (current assumptions)','redundancy':0.11,'ecc_overhead':0.07,'calibration_eff':0.78,'raw_yield':1.0,'eff_yield':0.89,'remap_recovery_factor':0.60,'label':'EO trim + PCM write scheduling + improved coupling'},
  'H1': {'process':'Improved process control (metrology/calibrated)','redundancy':0.22,'ecc_overhead':0.12,'calibration_eff':0.66,'raw_yield':1.0,'eff_yield':0.78,'remap_recovery_factor':0.50,'label':'Modular 3D partitioning + re-mapping spares + thermal vias/manifold'},
  'H4': {'process':'Pilot-line stabilized (tight control + thermal management)','redundancy':0.26,'ecc_overhead':0.14,'calibration_eff':0.62,'raw_yield':0.9997,'eff_yield':0.7398,'remap_recovery_factor':0.45,'label':'Hierarchical partitioning + alignment/calibration loops + higher redundancy'},
}

rows=[]
for k,b in BASE.items():
  o=OPTS[k]
  red=o['redundancy']; ecc=o['ecc_overhead']; rec=1.0-red
  # spare re-mapping recovers part of defective fraction functionally (conceptual)
  defect=max(0.0,1.0-o['raw_yield'])
  recovered=min(defect*o['remap_recovery_factor']* (red/0.2), defect)
  usable_fraction=min(1.0, (o['raw_yield']+recovered))
  area_total=b['area_cm2']*(1.0+red)  # physical area including spares
  area_eff=b['area_cm2']*rec          # payload-equivalent before defects
  tops_nom=b['tops']*rec              # nominal payload capacity reserved
  tops_eff=tops_nom*usable_fraction   # after defects/remap
  mem_nom=b['mem_mb']*rec
  mem_eff=mem_nom*usable_fraction
  bw_eff=b['bw_tbs']*rec*usable_fraction
  # overheads
  energy_over=(1.0+ecc*0.5 + red*0.15)  # ECC encode/decode + spare routing/control
  latency_over=(1.0+ecc*0.3 + 0.02)     # ECC/check + control
  cal_latency_over=(1.0 + (1.0-o['calibration_eff'])*0.05)
  tops_per_cm2_eff=tops_eff/area_total if area_total>0 else 0
  mem_per_cm2_eff=mem_eff/area_total if area_total>0 else 0
  rows.append({
    'key':k,'name':b['name'],'process':o['process'],'optimization':o['label'],
    'raw_yield':o['raw_yield'],'effective_yield_model':o['eff_yield'],
    'redundancy':red,'ecc_overhead':ecc,'recovered_defect_fraction':round(recovered,4),'usable_fraction':round(usable_fraction,4),
    'area_base_cm2':b['area_cm2'],'area_total_cm2':round(area_total,3),'area_overhead_pct':round(red*100,2),
    'tops_base':b['tops'],'tops_nominal_payload':round(tops_nom,3),'tops_effective':round(tops_eff,3),
    'mem_base_mb':b['mem_mb'],'mem_nominal_payload_mb':round(mem_nom,3),'mem_effective_mb':round(mem_eff,3),
    'bw_effective_tbs':round(bw_eff,3),
    'energy_overhead_factor':round(energy_over,4),'latency_overhead_factor':round(latency_over,4),'calibration_latency_factor':round(cal_latency_over,4),
    'tops_per_cm2_effective':round(tops_per_cm2_eff,4),'mem_mb_per_cm2_effective':round(mem_per_cm2_eff,4),
    'net_capacity_retention_tops':round(tops_eff/b['tops'],4),'net_capacity_retention_mem':round(mem_eff/b['mem_mb'],4),
  })

with open(os.path.join(OUT,'s4_cost_overhead.json'),'w',encoding='utf-8') as f:
  json.dump({'rows':rows,'note':'Conceptual overhead/cost model: redundancy reserves physical spares, ECC adds compute/control; remap recovers a fraction of defects; effective capacity depends on usable fraction and overheads. Not a signoff model.'},f,indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'s4_cost_overhead.csv'),'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# S4 — Coste de redundancia/re-mapeo (área, energía, latencia, capacidad efectiva)','',
    '> Modelo conceptual (no mediciones). Cuantifica overhead de optimizaciones S4 (spares, ECC, calibración, re-mapeo OMCC).','',
    '## Resumen','',
    '| Candidato | Redundancia | ECC | Área total (cm²) | TOPS base→efectivo | Mem base→efectiva (MB) | Retención TOPS | Retención Mem | Overhead energía | Overhead latencia | TOPS/cm² efectivo |',
    '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:
  md.append(f"| {r['key']} | {r['redundancy']} | {r['ecc_overhead']} | {r['area_total_cm2']} | {r['tops_base']}→{r['tops_effective']} | {r['mem_base_mb']}→{r['mem_effective_mb']} | {r['net_capacity_retention_tops']} | {r['net_capacity_retention_mem']} | {r['energy_overhead_factor']} | {r['latency_overhead_factor']} | {r['tops_per_cm2_effective']} |")
md+=['','## Detalle por candidato','']
for r in rows:
  md.append(f"### {r['key']} — {r['name']}")
  md.append(f"- Optimización: {r['optimization']} (proceso: {r['process']})")
  md.append(f"- Yield: bruto {r['raw_yield']}, efectivo modelo {r['effective_yield_model']}, fracción utilizable (con re-mapeo) {r['usable_fraction']}, defecto recuperado {r['recovered_defect_fraction']}")
  md.append(f"- Área: {r['area_base_cm2']} → {r['area_total_cm2']} cm² (+{r['area_overhead_pct']}% spares)")
  md.append(f"- Capacidad: TOPS {r['tops_base']}→{r['tops_effective']} (retención {r['net_capacity_retention_tops']}), Mem {r['mem_base_mb']}→{r['mem_effective_mb']} MB (retención {r['net_capacity_retention_mem']}), BW {r['bw_effective_tbs']} TB/s")
  md.append(f"- Overheads: energía ×{r['energy_overhead_factor']}, latencia ×{r['latency_overhead_factor']} (ECC/control) + calibración ×{r['calibration_latency_factor']}")
  md.append(f"- Densidad efectiva: {r['tops_per_cm2_effective']} TOPS/cm², {r['mem_mb_per_cm2_effective']} MB/cm²")
  md.append("")
md+=['## Conclusiones','- H3/G3 logran alta retención con overhead moderado (10–14% área, energía ×1.05–1.06) con NV; G2 (EO, sin escritura PCM) alcanza alta retención (~90%) y densidad efectiva con overhead bajo, a costa de menor persistencia NV.','- H1/H4 requieren mayor redundancia (22–26%) para asegurar yield bruto en 3D; retención neta ~74–78% TOPS/mem pero con mejora drástica de usabilidad vs baseline no optimizado.','- Re-mapeo OMCC es clave para convertir spares en capacidad utilizable; el coste real debe medirse en prototipos (área/ruteo, energía ECC, latencia de control).']
with open(os.path.join(OUT,'s4_cost_overhead.md'),'w',encoding='utf-8') as f: f.write('\n'.join(md)+'\n')
try:
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  keys=[r['key'] for r in rows]; x=range(len(keys)); w=0.35
  fig,ax=plt.subplots(1,2,figsize=(10,4))
  ax[0].bar([i-w/2 for i in x],[r['tops_base'] for r in rows],w,label='TOPS base')
  ax[0].bar([i+w/2 for i in x],[r['tops_effective'] for r in rows],w,label='TOPS efectivo')
  ax[0].set_xticks(list(x)); ax[0].set_xticklabels(keys); ax[0].set_title('Capacidad efectiva tras redundancia/re-mapeo'); ax[0].set_ylabel('TOPS'); ax[0].legend()
  ax[1].bar(keys,[r['net_capacity_retention_tops'] for r in rows], color='#54a24b', label='retención TOPS')
  ax[1].bar(keys,[r['energy_overhead_factor']-1 for r in rows], bottom=[r['net_capacity_retention_tops'] for r in rows], color='#e45756', alpha=0.6, label='overhead energía (Δ)')
  ax[1].set_ylim(0,1.4); ax[1].set_title('Retención y overhead de energía'); ax[1].legend(fontsize=8)
  fig.tight_layout(); fig.savefig(os.path.join(FIG,'s4_cost_overhead.png'),dpi=150); plt.close(fig)
except Exception as e:
  print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/s4_cost_overhead.*'}))
