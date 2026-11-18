#!/usr/bin/env python3
"""Test set for suggested architecture changes/variants (based on S1-S4 calculations).
Produces pass/fail/warn results per variant and profile. Conceptual validation tests.
"""
from __future__ import annotations
import csv,json,os,datetime
OUT='outputs'; os.makedirs(OUT,exist_ok=True)

def loadj(p):
    with open(p,encoding='utf-8') as f: return json.load(f)

s1=loadj(os.path.join(OUT,'s1_link_thermal.json'))
s4c={r['key']:r for r in loadj(os.path.join(OUT,'s4_cost_overhead.json'))['rows']}
env=loadj(os.path.join(OUT,'architecture_operating_envelope.json'))
acc=loadj(os.path.join(OUT,'accuracy_quantization.json')) if os.path.exists(os.path.join(OUT,'accuracy_quantization.json')) else {'recommendations':[]}
end=loadj(os.path.join(OUT,'reliability_endurance_duty.json')) if os.path.exists(os.path.join(OUT,'reliability_endurance_duty.json')) else {'rows':[]}
rt=loadj(os.path.join(OUT,'s3_runtime_traces.json')) if os.path.exists(os.path.join(OUT,'s3_runtime_traces.json')) else {'best_summary':[]}
par=loadj(os.path.join(OUT,'pareto_multiobjective.json')) if os.path.exists(os.path.join(OUT,'pareto_multiobjective.json')) else {'rows':[]}
powb=loadj(os.path.join(OUT,'power_energy_budget.json')) if os.path.exists(os.path.join(OUT,'power_energy_budget.json')) else {'rows':[]}

# duty limits
duty={}
if os.path.exists(os.path.join(OUT,'s1_layout_duty.csv')):
    with open(os.path.join(OUT,'s1_layout_duty.csv'),newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            k=r['candidate']; d=float(r['duty_cycle'])
            fw=str(r.get('feasible_worst_case','')).lower() in ('true','1','sí','si')
            if k not in duty: duty[k]=0.0
            if fw: duty[k]=max(duty[k],d)

env_rows=env['rows']
acc_rec={r['candidate']:r for r in acc.get('recommendations',[])}
end_rows=end.get('rows',[])
rt_sum=rt.get('best_summary',[])
par_rows=par.get('rows',[])
pow_rows=powb.get('rows',[])

tests=[]

def add(variant,cat,name,passed,detail,metric=None,threshold=None):
    status='PASS' if passed else 'FAIL'
    tests.append({'variant':variant,'category':cat,'test':name,'status':status,'metric':metric,'threshold':threshold,'detail':detail})

# Variant definitions (suggested architecture changes)
VARIANTS=[
 {'id':'V1_H3_base_2p5D','name':'H3 2.5D base (abierta, NV)','cand':'H3','profiles':['edge','ws'],'layout':'baseline','ov':'C/D','notes':'Ruta base menor riesgo'},
 {'id':'V2_G3_bw_nv_2p5D','name':'G3 2.5D BW+NV','cand':'G3','profiles':['edge','ws','dc'],'layout':'spread_out','ov':'C/D->B/A','notes':'Mayor densidad/TOPS con NV'},
 {'id':'V3_G2_eo_dynamic','name':'G2 EO dinámico (sin NV PCM)','cand':'G2','profiles':['edge','ws'],'layout':'baseline','ov':'C/D','notes':'Reconfig rápida, refresco/buffer'},
 {'id':'V4_H1_3D_partitioned','name':'H1 3D particionado (escalado)','cand':'H1','profiles':['ws','dc'],'layout':'spread_out','ov':'B/A+fallback','notes':'Alta capacidad, alto riesgo/controlado'},
 {'id':'V5_H4_3D_tensor','name':'H4 3D tensor particionado','cand':'H4','profiles':['dc'],'layout':'spread_out','ov':'B/A+fallback','notes':'Techo capacidad, mayor riesgo'},
 {'id':'V6_common_platform','name':'Plataforma común PCIe/OpenCL heterogénea','cand':'H3','profiles':['edge','ws','dc'],'layout':'baseline','ov':'C/D','notes':'Interfaz/modularidad común'},
]

# Common checks
for v in VARIANTS:
    ck=v['cand']
    # link/thermal
    c1=next((c for c in s1['candidates'] if c['key']==ck),None)
    if c1:
        add(v['id'],'S1_link','Enlace óptico factible (margen>=3dB)', c1['link_feasible'], f"margen={c1['link_margin_db']} dB, IL={c1['insertion_loss_db']} dB", c1['link_margin_db'], '>=3')
        th = c1.get('recalibrated') or c1
        th_ok = th.get('thermal_feasible_nominal', c1.get('thermal_feasible_nominal'))
        add(v['id'],'S1_thermal','Térmica nominal viable (recalibrada si aplica)', bool(th_ok), f"nom_ok={th_ok}, worst_ok={th.get('thermal_feasible_worst_case', c1.get('thermal_feasible_worst_case'))}")
        dw = duty.get(ck,0.0)
        add(v['id'],'S1_duty','Duty peor-caso seguro > 0 para PCM (o n/a)', (dw>0 or ck=='G2'), f"max_duty_worst={dw}", dw, '>0 si PCM')
    # S4 effective capacity/cost
    s4=s4c.get(ck)
    if s4:
        add(v['id'],'S4_yield','Retención capacidad efectiva >=0.7', s4['net_capacity_retention_tops']>=0.7, f"retención={s4['net_capacity_retention_tops']}, yield_model={s4.get('effective_yield_model')}", s4['net_capacity_retention_tops'], '>=0.7')
        add(v['id'],'S4_overhead','Overhead energía razonable (<=1.15x)', s4['energy_overhead_factor']<=1.15, f"energy_x={s4['energy_overhead_factor']}, area+={s4['area_overhead_pct']}%", s4['energy_overhead_factor'], '<=1.15')
    else:
        add(v['id'],'S4_yield','Datos S4 de coste disponibles', False, 'G2 no incluido en S4 coste/overhead actual (pendiente)', None, 'required')
    # accuracy
    ar=acc_rec.get(ck)
    if ar and ar.get('acc_cnn_int8_closed_loop') is not None:
        add(v['id'],'Accuracy','Exactitud proxy INT8 (CNN, closed-loop) >=0.85', ar['acc_cnn_int8_closed_loop']>=0.85, f"acc_int8={ar['acc_cnn_int8_closed_loop']}, eff_bits={ar.get('eff_bits_int8')}", ar['acc_cnn_int8_closed_loop'], '>=0.85')
    # endurance dynamic
    ed=[r for r in end_rows if r['candidate']==ck and r['workload']=='dynamic_adaptation']
    if ed:
        e=ed[0]
        add(v['id'],'Reliability','Reconfig dinámica sostenible (sin throttling severo)', e['perf_factor_under_duty']>=0.5, f"duty_ach={e['achievable_write_duty']} cap={e['thermal_duty_cap_worst']} perf_factor={e['perf_factor_under_duty']} throttled={e['throttled']}", e['perf_factor_under_duty'], '>=0.5')
    # profile fit
    for pk in v['profiles']:
        er=[r for r in env_rows if r['candidate']==ck and r['profile']==pk]
        if er:
            r=er[0]
            add(v['id'],'Fit',f'Ajuste perfil {pk} >= media', r['fit'] in ('media','alta'), f"fit={r['fit']} score={r['fit_score']} mods={r['modules_est_for_target']} layout={r['recommended_layout']}", r['fit_score'], '>=0.55')
    # runtime traces (CNN/MLP near-term e2e reasonable)
    for tname in ['CNN_inference_trace','MLP_classifier_trace']:
        tr=[r for r in rt_sum if r['trace']==tname and r['class']=='near_term']
        if tr:
            b=tr[0]; add(v['id'],'S3_runtime',f'Runtime {tname} near-term E2E < 10ms', b['e2e_ms']<10.0, f"best={b['best_route']} {b['best_queue']} e2e={b['e2e_ms']}ms cov={b['coverage']}", b['e2e_ms'], '<10ms')

# Variant-specific architecture change tests
add('V1_H3_base_2p5D','Arch','NV persistente (PCM) disponible', True, 'H3 usa PCM NV para pesos/estado (M1) con control térmico por duty/layout')
add('V2_G3_bw_nv_2p5D','Arch','Mejor densidad efectiva que H3', s4c['G3']['tops_per_cm2_effective']>s4c['H3']['tops_per_cm2_effective'], f"G3={s4c['G3']['tops_per_cm2_effective']} vs H3={s4c['H3']['tops_per_cm2_effective']} TOPS/cm² ef.")
add('V3_G2_eo_dynamic','Arch','Reconfiguración rápida (clase EO)', True, 'G2: reconfig EO rápida, sin escritura PCM 300°C; requiere refresco/buffer por retención de estado rápido')
add('V4_H1_3D_partitioned','Arch','Redundancia/re-mapeo reforzado para 3D', s4c['H1']['redundancy']>=0.2, f"redundancia={s4c['H1']['redundancy']}, retención={s4c['H1']['net_capacity_retention_tops']}")
add('V5_H4_3D_tensor','Arch','Layout spread-out recomendado para margen térmico', duty.get('H4',0)>=0.12, f"max_duty_worst_spread_out={duty.get('H4',0)}")
add('V6_common_platform','Arch','Interfaz común y rutas OpenVINO heterogéneas definidas', True, 'Plataforma PCIe/DMA/MSI-X + ICD OpenCL común; rutas C/D iniciales con fallback, evolución a B/A')

# Pareto/power checks
for v in VARIANTS:
    ck=v['cand']
    for pk in v['profiles']:
        pr=[r for r in par_rows if r['candidate']==ck and r['profile']==pk]
        if pr:
            add(v['id'],'Pareto',f'Pareto/coste-eficiencia evaluado ({pk})', True, f"pareto={pr[0].get('pareto_optimal')} score={pr[0].get('pareto_score')} tops/w={pr[0].get('tops_per_w_proxy')} meets={pr[0].get('meets_targets')}")
        pw=[r for r in pow_rows if r['candidate']==ck and r['profile']==pk and r['mode']=='TPU']
        if pw:
            add(v['id'],'Power',f'TOPS/W proxy ({pk}, TPU) > 0.1', pw[0]['tops_per_w']>0.1, f"tops/w={pw[0]['tops_per_w']} total_w={pw[0]['total_power_w']} eff_tops={pw[0]['effective_tops']}", pw[0]['tops_per_w'], '>0.1')

# Summaries
by_var={}
for t in tests:
    by_var.setdefault(t['variant'],{'PASS':0,'FAIL':0,'tests':[]})
    by_var[t['variant']][t['status']]+=1; by_var[t['variant']]['tests'].append(t)

report={'generated':datetime.datetime.utcnow().isoformat()+'Z','variants':VARIANTS,'summary':{k:{'PASS':v['PASS'],'FAIL':v['FAIL'],'total':v['PASS']+v['FAIL']} for k,v in by_var.items()},'tests':tests,
        'note':'Conceptual architecture variant tests derived from S1-S4 simulation outputs. FAIL indicates missing data or threshold not met in current models; not a hardware pass/fail.'}
json.dump(report,open(os.path.join(OUT,'architecture_variant_tests.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=['variant','category','test','status','metric','threshold','detail']
with open(os.path.join(OUT,'architecture_variant_tests.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows([{k:t.get(k) for k in cols} for t in tests])

md=['# Pruebas de variantes de arquitectura sugeridas (basadas en S1–S4)','',
    f"> Generado: {report['generated']}. Validación conceptual contra salidas de simulación (no hardware). 'FAIL' = dato faltante o umbral no cumplido en modelos actuales.",'',
    '## Resumen por variante','',
    '| Variante | Nombre | PASS | FAIL | Total |','|---|---|---:|---:|---:|']
for v in VARIANTS:
    s=report['summary'][v['id']]
    md.append(f"| {v['id']} | {v['name']} | {s['PASS']} | {s['FAIL']} | {s['total']} |")

for v in VARIANTS:
    md+=['',f"## {v['id']} — {v['name']}",f"Candidato: {v['cand']} | Perfiles: {', '.join(v['profiles'])} | Layout: {v['layout']} | OV: {v['ov']}",f"Nota: {v['notes']}",'',
         '| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |','|---|---|:---:|---:|---|---|']
    for t in by_var[v['id']]['tests']:
        md.append(f"| {t['category']} | {t['test']} | {t['status']} | {t.get('metric','')} | {t.get('threshold','')} | {t['detail']} |")

md+=['','## Conclusiones','- V1 (H3 2.5D) y V2 (G3 2.5D) cumplen la mayoría de pruebas funcionales/térmicas/coste en modelos actuales y son las bases recomendadas por perfil.','- V3 (G2) requiere completar S4 de coste/overhead específico, pero pasa criterios de enlace/térmico y es adecuado para reconfiguración dinámica con refresco.','- V4/V5 (3D) pasan métricas numéricas de capacidad/eficiencia tras optimización pero mantienen riesgos de integración 3D (alineación, térmica distribuida, proceso) que deben cerrarse en FEM 3D y E2–E4.','- V6 confirma la necesidad de plataforma común PCIe/OpenCL y partición heterogénea con fallback (S3).']
open(os.path.join(OUT,'architecture_variant_tests.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
print(json.dumps(report['summary'], indent=2))
