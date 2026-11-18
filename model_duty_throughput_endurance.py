#!/usr/bin/env python3
"""Co-optimization: duty cycle <-> throughput <-> endurance by profile (conceptual).
Integrates S1 duty limits, S2 targets, and endurance/write constraints to find operating points.
Includes weight-stationary mapping (rewrite fraction) to avoid overestimating PCM writes.
"""
from __future__ import annotations
import csv,json,os,math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
S1=json.load(open(os.path.join(OUT,'s1_link_thermal.json'),encoding='utf-8'))
S2=json.load(open(os.path.join(OUT,'s2_system_profiles.json'),encoding='utf-8'))
# duty limits worst
max_duty={}
if os.path.exists(os.path.join(OUT,'s1_layout_duty.csv')):
    with open(os.path.join(OUT,'s1_layout_duty.csv'),newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            k=r['candidate']; d=float(r['duty_cycle'])
            fw=str(r.get('feasible_worst_case','')).lower() in ('true','1','sí','si')
            if k not in max_duty: max_duty[k]=0.0
            if fw: max_duty[k]=max(max_duty[k],d)
TECH={'H3':{'end':1e8,'write_us':1.0,'nv':True},'G3':{'end':1e8,'write_us':0.5,'nv':True},'G2':{'end':1e15,'write_us':0.001,'nv':False},'H1':{'end':5e7,'write_us':1.0,'nv':True},'H4':{'end':5e7,'write_us':0.8,'nv':True}}
PROFILES=S2.get('profiles',{})
# workload patterns: (name, desired_reconfig_duty, throughput_factor, rewrite_fraction_of_cells_per_event, events_per_s_equiv)
# rewrite_fraction models weight-stationary mapping: only a subset of cells rewritten on updates
PATTERNS=[
 ('weight_stationary_inference', 0.0001, 1.0, 0.0005, 0.01),  # rare weight refresh/calibration
 ('inference_static', 0.001, 1.0, 0.002, 0.05),
 ('periodic_update', 0.02, 0.95, 0.02, 0.5),
 ('adaptive', 0.08, 0.85, 0.08, 2.0),
 ('continuous_learning', 0.2, 0.7, 0.25, 5.0),
]

rows=[]
for ck in ['H3','G3','G2','H1','H4']:
    lim=max_duty.get(ck,0.05 if ck!='G2' else 1.0)
    t=TECH[ck]
    for pk,pv in PROFILES.items():
        tgt=pv.get('targets',{}).get('tops',0)
        for pn,desired,th_factor,rewrite_frac,events_s in PATTERNS:
            cap=lim if t['nv'] and ck!='G2' else 1.0
            ach=min(desired,cap)
            throttle=desired>ach+1e-9
            perf=th_factor*(ach/desired if desired>0 else 1.0)
            eff_tops=tgt*perf
            # endurance: cell-write events = events * rewrite_fraction * duty utilization factor (conceptual)
            # write_us gives time per cell; but effective rewritten cells limited by mapping
            effective_write_activity = ach * rewrite_frac * events_s
            writes_s = effective_write_activity * 1e3  # scaled conceptual cell-updates/s
            w5y=writes_s*3600*24*365*5
            life_margin = (t['end']*0.5)/w5y if w5y>0 else float('inf')
            end_ok=life_margin>=1.0
            score=0.4*min(1.0,perf)+0.3*(1.0 if not throttle else 0.5)+0.3*(1.0 if end_ok else 0.3)
            rec='ok' if (not throttle and end_ok) else ('throttle' if throttle and end_ok else 'wear-level/re-mapping required')
            rows.append({'candidate':ck,'profile':pk,'pattern':pn,'desired_duty':desired,'duty_cap_worst':cap,'achievable_duty':round(ach,4),
                         'rewrite_fraction':rewrite_frac,'events_per_s_equiv':events_s,
                         'throttled':throttle,'throughput_factor':round(th_factor,3),'perf_factor':round(perf,4),'target_tops':tgt,'effective_tops_proxy':round(eff_tops,3),
                         'writes_5y_est':float(f'{w5y:.3e}'),'endurance_cycles':t['end'],'endurance_life_margin_x':round(life_margin,4) if life_margin!=float('inf') else 'inf',
                         'endurance_ok_5y':end_ok,'coopt_score':round(score,4),'recommendation':rec})

# best operating point per cand/profile (max score, prefer no throttle)
best=[]
for ck in ['H3','G3','G2','H1','H4']:
    for pk in PROFILES.keys():
        sub=[r for r in rows if r['candidate']==ck and r['profile']==pk]
        b=sorted(sub,key=lambda r:(0 if r['throttled'] else 1, r['endurance_ok_5y'], r['coopt_score']), reverse=True)[0]
        best.append({'candidate':ck,'profile':pk,'best_pattern':b['pattern'],'achievable_duty':b['achievable_duty'],'rewrite_fraction':b['rewrite_fraction'],'perf_factor':b['perf_factor'],'endurance_ok_5y':b['endurance_ok_5y'],'recommendation':b['recommendation'],'coopt_score':b['coopt_score']})

out={'rows':rows,'best':best,'duty_caps':max_duty,'note':'Conceptual co-optimization with weight-stationary rewrite fractions. Endurance depends on mapping, wear-leveling, ECC and measured cycling/retention; validate with device stats.'}
json.dump(out,open(os.path.join(OUT,'duty_throughput_endurance.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'duty_throughput_endurance.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Co-optimización duty ↔ throughput ↔ endurance por perfil (conceptual, weight-stationary)','',
    '> Integra límites de duty térmico (S1), objetivos (S2) y endurance con fracción de celdas reescritas por evento (mapeo weight-stationary). Modelo simplificado.','',
    '## Puntos recomendados por candidato/perfil','',
    '| Candidato | Perfil | Patrón recomendado | Duty alcanzable | Fracción reescrita | Factor perf. | Endurance 5y OK | Score | Recomendación |','|---|---|---|---:|---:|---:|:---:|---:|---|']
for b in best:
    md.append(f"| {b['candidate']} | {b['profile']} | {b['best_pattern']} | {b['achievable_duty']} | {b['rewrite_fraction']} | {b['perf_factor']} | {'sí' if b['endurance_ok_5y'] else 'no'} | {b['coopt_score']} | {b['recommendation']} |")
md+=['','## Resumen por patrón (ejemplos)','',
     '| Candidato | Perfil | Patrón | Duty | Rewrites 5y | Margen vida | Endurance OK |','|---|---|---|---:|---:|---:|:---:|']
for r in rows:
    if r['profile']=='ws' and r['pattern'] in ('weight_stationary_inference','periodic_update','continuous_learning'):
        lm=r['endurance_life_margin_x']
        md.append(f"| {r['candidate']} | {r['profile']} | {r['pattern']} | {r['achievable_duty']} | {r['writes_5y_est']} | {lm} | {'sí' if r['endurance_ok_5y'] else 'no'} |")
md+=['','## Lectura','- Con mapeo **weight-stationary** (baja fracción de reescritura), inferencia y actualizaciones periódicas son compatibles con endurance PCM en este modelo; cargas de aprendizaje continuo/adaptativas agresivas requieren wear-leveling, particionado térmico y/o reducción de rewrites.','- G2 favorece reconfiguración frecuente (alta endurance EO) pero necesita refresco/buffer por retención; candidatos PCM exigen minimizar escrituras en hot-cells (OMCC).','- Validar con estadísticas reales de ciclado/retención y patrones de actualización de pesos por aplicación.']
open(os.path.join(OUT,'duty_throughput_endurance.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    pats=[p[0] for p in PATTERNS]; cands=['H3','G3','G2','H1','H4']; x=range(len(pats)); w=0.15
    fig,ax=plt.subplots(figsize=(10,4))
    for i,c in enumerate(cands):
        vals=[next(r['coopt_score'] for r in rows if r['candidate']==c and r['profile']=='ws' and r['pattern']==p) for p in pats]
        ax.bar([xi+(i-2)*w for xi in x], vals, w, label=c)
    ax.set_xticks(list(x)); ax.set_xticklabels(pats, rotation=15); ax.set_ylim(0,1.1)
    ax.set_ylabel('Score co-optimización'); ax.set_title('Duty-throughput-endurance weight-stationary (perfil ws, conceptual)'); ax.legend(ncol=5,fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(FIG,'duty_throughput_endurance.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'best':len(best),'out':'outputs/duty_throughput_endurance.*'}))
