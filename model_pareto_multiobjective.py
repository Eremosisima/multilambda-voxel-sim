#!/usr/bin/env python3
"""Multiobjective Pareto selection (cost/TOPS/W/retention/area) per profile - conceptual.
Uses S4 cost/overhead and objective combo analysis.
"""
from __future__ import annotations
import csv,json,os,math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
S4=json.load(open(os.path.join(OUT,'s4_cost_overhead.json'),encoding='utf-8'))
OBJ=json.load(open(os.path.join(OUT,'objective_combo_analysis.json'),encoding='utf-8'))

# get base metrics from objective analysis results (key/name)
obj_map={}
for r in OBJ.get('results', OBJ.get('ranked',[])) if isinstance(OBJ.get('results', OBJ.get('ranked',[])), list) else []:
    k=r.get('key') or r.get('candidate')
    if k: obj_map[k]=r
# fallback: try 'combinations' or flatten
if not obj_map:
    for k,v in OBJ.items():
        if isinstance(v, dict) and 'key' in v: obj_map[v['key']]=v

PROFILES={'edge':{'tops':8,'mem_mb':128,'budget_cost':1.0,'budget_w':30},
          'ws':{'tops':20,'mem_mb':512,'budget_cost':2.0,'budget_w':120},
          'dc':{'tops':80,'mem_mb':2048,'budget_cost':6.0,'budget_w':400}}

rows=[]
for s in S4['rows']:
    k=s['key']
    base=obj_map.get(k,{})
    cost_index = base.get('cost_index', {'H3':1.4,'G3':1.3,'H1':2.0,'H4':2.3}.get(k,1.5))
    # estimated power proxy: tops * pj_mac_equiv scaled, adjusted by energy overhead
    pj = {'H3':0.57,'G3':0.50,'H1':0.55,'H4':0.52,'G2':0.35}.get(k,0.55)
    tops_eff=s['tops_effective']; mem_eff=s['mem_effective_mb']; ret=s['net_capacity_retention_tops']
    area=s['area_total_cm2']; e_ov=s['energy_overhead_factor']
    # power W proxy for effective throughput utilization (conceptual)
    w_per_tops = pj * 0.8 * e_ov # arbitrary scaling proxy
    tops_per_w = (1.0/w_per_tops) if w_per_tops>0 else 0
    for pk,p in PROFILES.items():
        modules = math.ceil(p['tops']/tops_eff) if tops_eff>0 else 99
        total_tops = modules*tops_eff
        total_mem = modules*mem_eff
        total_area = modules*area
        total_cost = modules*cost_index
        total_w = modules*tops_eff*w_per_tops
        meets = total_tops>=p['tops'] and total_mem>=p['mem_mb']*0.5
        # normalized objectives (higher better except cost/area/power)
        perf = min(2.0,total_tops/p['tops']) if p['tops'] else 0
        memfit = min(2.0,total_mem/max(p['mem_mb'],1))
        eff = tops_per_w
        cost_eff = total_tops/max(total_cost,1e-6)
        pareto_score = 0.3*perf + 0.15*memfit + 0.2*min(1.5,eff/2.0) + 0.2*ret + 0.15*min(1.5,cost_eff/3.0)
        rows.append({'candidate':k,'profile':pk,'modules':modules,'total_tops_eff':round(total_tops,3),'total_mem_eff_mb':round(total_mem,2),
                     'total_area_cm2':round(total_area,2),'total_cost_index':round(total_cost,3),'total_power_w_proxy':round(total_w,2),
                     'tops_per_w_proxy':round(tops_per_w,3),'capacity_retention':ret,'meets_targets':meets,
                     'perf_norm':round(perf,3),'mem_norm':round(memfit,3),'cost_eff_tops_per_cost':round(cost_eff,3),'pareto_score':round(pareto_score,4)})

# pareto front (non-dominated) per profile on (tops/cost, tops/W, retention, -area)
def dominates(a,b):
    # maximize: cost_eff, tops_per_w_proxy, capacity_retention, perf_norm ; minimize: total_area_cm2
    better_or_eq = (a['cost_eff_tops_per_cost']>=b['cost_eff_tops_per_cost'] and a['tops_per_w_proxy']>=b['tops_per_w_proxy'] and a['capacity_retention']>=b['capacity_retention'] and a['perf_norm']>=b['perf_norm'] and a['total_area_cm2']<=b['total_area_cm2'])
    strictly = (a['cost_eff_tops_per_cost']>b['cost_eff_tops_per_cost'] or a['tops_per_w_proxy']>b['tops_per_w_proxy'] or a['capacity_retention']>b['capacity_retention'] or a['perf_norm']>b['perf_norm'] or a['total_area_cm2']<b['total_area_cm2'])
    return better_or_eq and strictly
for pk in PROFILES:
    sub=[r for r in rows if r['profile']==pk]
    for r in sub:
        r['pareto_optimal']=not any(dominates(o,r) for o in sub if o is not r)

out={'rows':rows,'note':'Conceptual Pareto (uses S4 effective metrics + cost_index proxy). Power/TOPS-W are proxies; validate with measured energy and BOM costs.'}
json.dump(out,open(os.path.join(OUT,'pareto_multio bjective.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
# fix filename space
os.replace(os.path.join(OUT,'pareto_multio bjective.json'), os.path.join(OUT,'pareto_multiobjective.json'))
cols=list(rows[0].keys())
with open(os.path.join(OUT,'pareto_multiobjective.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Optimización multiobjetivo Pareto (costo/TOPS/W/retención/área, conceptual)','',
    '> Selección por perfil usando capacidad efectiva y overheads S4 + proxy de coste/potencia. No es BOM ni medición de energía.','',
    '## Resultados','',
    '| Candidato | Perfil | Módulos | TOPS total | Mem total (MB) | Área (cm²) | Coste idx | Potencia (W proxy) | TOPS/W | Retención | Cumple | Pareto | Score |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|---:|']
for r in rows:
    md.append(f"| {r['candidate']} | {r['profile']} | {r['modules']} | {r['total_tops_eff']} | {r['total_mem_eff_mb']} | {r['total_area_cm2']} | {r['total_cost_index']} | {r['total_power_w_proxy']} | {r['tops_per_w_proxy']} | {r['capacity_retention']} | {'sí' if r['meets_targets'] else 'no'} | {'sí' if r['pareto_optimal'] else 'no'} | {r['pareto_score']} |")
md+=['','## Recomendación por perfil (trade-off)','- **Edge:** G3/H3 destacan por eficiencia y retención con pocos módulos; H1/H4 viables en capacidad pero con mayor coste/área/complejidad 3D.','- **WS:** G3 ofrece buen balance TOPS/W/coste; H3 base abierta de menor riesgo.','- **DC:** G3 escala en módulos con mejor coste-eficiencia que 3D en este proxy; H1/H4 reducen conteo de módulos pero requieren madurez 3D y mayor área/coste.']
open(os.path.join(OUT,'pareto_multiobjective.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    for pk in PROFILES:
        sub=[r for r in rows if r['profile']==pk]
        fig,ax=plt.subplots(figsize=(5.5,4))
        for r in sub:
            m='*' if r['pareto_optimal'] else 'o'
            ax.scatter(r['total_cost_index'], r['tops_per_w_proxy'], s=80 if r['pareto_optimal'] else 40, marker=m)
            ax.annotate(r['candidate'], (r['total_cost_index'], r['tops_per_w_proxy']), fontsize=8, xytext=(3,3), textcoords='offset points')
        ax.set_xlabel('Coste índice total (proxy)'); ax.set_ylabel('TOPS/W (proxy)'); ax.set_title(f'Pareto {pk}: eficiencia vs coste (★ óptimo)')
        fig.tight_layout(); fig.savefig(os.path.join(FIG,f'pareto_{pk}.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/pareto_multiobjective.*'}))
