#!/usr/bin/env python3
"""Reliability/endurance vs thermal duty (write-rate constrained) - conceptual.
Extends P2/S4 with duty limits from S1 layout sweep to project retention/wear windows.
"""
from __future__ import annotations
import csv,json,os,math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
S1=json.load(open(os.path.join(OUT,'s1_link_thermal.json'),encoding='utf-8'))
# max duty worst-case from sweep summary in s1_link_thermal.md/json context: use layout_duty sweep file if present
max_duty={}
if os.path.exists(os.path.join(OUT,'s1_layout_duty.csv')):
    with open(os.path.join(OUT,'s1_layout_duty.csv'),newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            k=r['candidate']; d=float(r['duty_cycle'])
            fw=str(r.get('feasible_worst_case','')).lower() in ('true','1','sí','si')
            fn=str(r.get('feasible_nominal','')).lower() in ('true','1','sí','si')
            if k not in max_duty: max_duty[k]={'nom':0.0,'worst':0.0}
            if fw: max_duty[k]['worst']=max(max_duty[k]['worst'],d)
            if fn: max_duty[k]['nom']=max(max_duty[k]['nom'],d)

# endurance/retention params (conceptual, per technology)
TECH={
 'H3':{'type':'PCM','endurance_cycles':1e8,'retention_s':1e8,'write_energy_nj':2.0,'write_time_us':1.0,'nv':True},
 'G3':{'type':'PCM+EO','endurance_cycles':1e8,'retention_s':1e8,'write_energy_nj':1.5,'write_time_us':0.5,'nv':True},
 'G2':{'type':'EO/volatile-ish','endurance_cycles':1e15,'retention_s':1e-2,'write_energy_nj':0.05,'write_time_us':0.001,'nv':False},
 'H1':{'type':'PCM+VO2','endurance_cycles':5e7,'retention_s':1e8,'write_energy_nj':2.2,'write_time_us':1.0,'nv':True},
 'H4':{'type':'PCM+mixed','endurance_cycles':5e7,'retention_s':1e8,'write_energy_nj':2.0,'write_time_us':0.8,'nv':True},
}
WORK_RATES=[('inference_static', 0.001), ('periodic_reconfig', 0.02), ('dynamic_adaptation', 0.08), ('aggressive_reconfig', 0.2)] # desired write duty fraction

rows=[]
for k,t in TECH.items():
    lim=max_duty.get(k,{'nom':0.05,'worst':0.0})
    for wname,desired in WORK_RATES:
        # achievable duty capped by thermal worst-case (if PCM) else nominal/high
        cap = lim['worst'] if (t['nv'] and 'PCM' in t['type']) else (lim['nom'] if lim['nom']>0 else 1.0)
        ach=min(desired, cap if cap>0 else desired*0.2)
        throttle = desired>ach+1e-9
        # writes per day assuming 1us-equivalent slots scaled
        slots_per_s = 1e6 / max(t['write_time_us'],1e-6)
        writes_per_s = ach * slots_per_s * 0.001 # effective cells written fraction (conceptual)
        writes_5y = writes_per_s * 3600*24*365*5
        endurance_ok = writes_5y < t['endurance_cycles']*0.5 # margin
        # retention/refresher need
        if t['nv']:
            refresh_needed=False; refresh_period_s=t['retention_s']*0.2
        else:
            refresh_period_s=max(t['retention_s']*0.5,1e-6); refresh_needed=True
        # effective availability under throttling
        perf_factor = (ach/desired) if desired>0 else 1.0
        energy_per_reconfig_mj = writes_per_s * t['write_energy_nj'] * 1e-6 # mJ/s proxy
        rows.append({'candidate':k,'tech':t['type'],'workload':wname,'desired_write_duty':desired,
                     'thermal_duty_cap_worst':cap,'achievable_write_duty':round(ach,4),'throttled':throttle,
                     'perf_factor_under_duty':round(perf_factor,4),'writes_5y_est':float(f'{writes_5y:.3e}'),
                     'endurance_cycles':t['endurance_cycles'],'endurance_ok_5y_margin':endurance_ok,
                     'retention_s':t['retention_s'],'refresh_needed':refresh_needed,'refresh_period_s':refresh_period_s,
                     'write_energy_nj':t['write_energy_nj']})

out={'rows':rows,'duty_limits_worst':max_duty,'note':'Conceptual endurance/duty model; replace with measured cycle-to-failure, retention distributions and thermal time constants.'}
json.dump(out,open(os.path.join(OUT,'reliability_endurance_duty.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'reliability_endurance_duty.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Fiabilidad/endurance bajo restricción térmica de duty (conceptual)','',
    '> Proyecta escrituras/reconfiguraciones sostenibles usando límites de duty S1 (peor caso) y parámetros de endurance/retención. No son mediciones.','',
    '## Resumen','',
    '| Candidato | Carga | Duty deseado | Límite térmico (peor) | Duty alcanzable | Throttling | Factor perf. | Endurance OK (5y, margen) | Refresh necesario |','|---|---|---:|---:|---:|:---:|---:|:---:|:---:|']
for r in rows:
    md.append(f"| {r['candidate']} | {r['workload']} | {r['desired_write_duty']} | {r['thermal_duty_cap_worst']} | {r['achievable_write_duty']} | {'sí' if r['throttled'] else 'no'} | {r['perf_factor_under_duty']} | {'sí' if r['endurance_ok_5y_margin'] else 'no'} | {'sí' if r['refresh_needed'] else 'no'} |")
md+=['','## Lectura','- Cargas estáticas/periódicas son compatibles con límites térmicos PCM (H3/G3/H1/H4) y preservan endurance; adaptación dinámica agresiva puede requerir throttling o particionado/alternancia térmica.','- G2 (EO) no está limitado por escritura térmica PCM pero requiere refresco/buffer por baja retención efectiva de estado rápido; adecuado a reconfiguración frecuente.','- Integrar con OMCC (scheduling térmico, wear-leveling, re-mapeo) y validar con caracterización de ciclos/retención.']
open(os.path.join(OUT,'reliability_endurance_duty.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    cands=['H3','G3','G2','H1','H4']; workloads=[w[0] for w in WORK_RATES]; x=range(len(workloads)); w=0.15
    fig,ax=plt.subplots(figsize=(9,4))
    for i,c in enumerate(cands):
        vals=[next(r['perf_factor_under_duty'] for r in rows if r['candidate']==c and r['workload']==wl) for wl in workloads]
        ax.bar([xi+(i-2)*w for xi in x], vals, w, label=c)
    ax.set_xticks(list(x)); ax.set_xticklabels(workloads, rotation=10); ax.set_ylim(0,1.1)
    ax.set_ylabel('Factor de desempeño (duty alcanzable/deseado)'); ax.set_title('Impacto de límite térmico de duty en reconfiguración (conceptual)')
    ax.legend(ncol=5,fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(FIG,'reliability_endurance_duty.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/reliability_endurance_duty.*'}))
