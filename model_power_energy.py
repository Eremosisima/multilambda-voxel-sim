#!/usr/bin/env python3
"""Power/energy budget per profile and mode (NPU/TPU) - conceptual proxy.
Combines pJ/MAC, S4 overheads, E/O-O/E and control/PCIe shares.
"""
from __future__ import annotations
import csv,json,os,math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
S4={r['key']:r for r in json.load(open(os.path.join(OUT,'s4_cost_overhead.json'),encoding='utf-8'))['rows']}
S2=json.load(open(os.path.join(OUT,'s2_system_profiles.json'),encoding='utf-8'))

BASE_PJ={'H3':0.57,'G3':0.50,'G2':0.35,'H1':0.55,'H4':0.52}
# fixed overhead components (W proxy at module scale) conceptual
OH={'pcie_ctrl_w':3.0,'e_o_o_e_w':2.5,'laser_w':1.5,'cooling_ctrl_w':2.0,'omcc_w':1.0}
MODES={'NPU':{'util':0.65,'ctrl_factor':1.0},'TPU':{'util':0.75,'ctrl_factor':1.05},'GPU':{'util':0.55,'ctrl_factor':1.1}}
PROFILES=S2.get('profiles',{})

rows=[]
for ck in ['H3','G3','G2','H1','H4']:
    s4=S4.get(ck)
    if not s4:
        # G2 fallback approx
        tops_eff=5.42*0.95; mem_eff=192*0.95; e_ov=1.04; l_ov=1.03; ret=0.95
    else:
        tops_eff=s4['tops_effective']; mem_eff=s4['mem_effective_mb']; e_ov=s4['energy_overhead_factor']; l_ov=s4['latency_overhead_factor']; ret=s4['net_capacity_retention_tops']
    pj=BASE_PJ[ck]*e_ov
    for pk,pv in PROFILES.items():
        tgt=(pv.get('targets') or {}).get('tops',8)
        modules=max(1, math.ceil(tgt/tops_eff)) if tops_eff>0 else 1
        for mode,m in MODES.items():
            dyn_w = tops_eff * 1e12 * pj * 1e-12 * m['util'] # TOPS * pJ/MAC scaled (proxy) => W
            fixed = (OH['pcie_ctrl_w']+OH['e_o_o_e_w']+OH['laser_w']+OH['cooling_ctrl_w']+OH['omcc_w'])*m['ctrl_factor']
            mod_w = dyn_w + fixed
            total_w = modules*mod_w
            eff_tops = modules*tops_eff*m['util']
            tops_per_w = eff_tops/total_w if total_w>0 else 0
            rows.append({'candidate':ck,'profile':pk,'mode':mode,'modules':modules,'tops_effective_module':round(tops_eff,3),
                         'utilization':m['util'],'dynamic_w_per_module':round(dyn_w,3),'fixed_w_per_module':round(fixed,3),
                         'total_power_w':round(total_w,3),'effective_tops':round(eff_tops,3),'tops_per_w':round(tops_per_w,4),
                         'pj_mac_eff':round(pj,4),'capacity_retention':ret})

out={'rows':rows,'assumptions':{'base_pj_mac':BASE_PJ,'overheads_w':OH,'note':'Highly approximate power proxy (not measured). Dynamic term scaled from TOPS*pJ/MAC*utilization; fixed includes PCIe/control/E-O/laser/cooling/OMCC.'}}
json.dump(out,open(os.path.join(OUT,'power_energy_budget.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'power_energy_budget.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
# summary best per profile/mode
md=['# Presupuesto de potencia/energía por perfil y modo (proxy, conceptual)','',
    '> Estimación aproximada (no mediciones). Dinámico ~ TOPS·pJ/MAC·utilización + fijos (PCIe/control, E/O-O/E, láser, refrigeración, OMCC) con overheads S4.','',
    '## Resumen (TPU, utilización objetivo)','',
    '| Candidato | Perfil | Módulos | Potencia total (W) | TOPS efectivos | TOPS/W | pJ/MAC ef. |','|---|---|---:|---:|---:|---:|---:|']
for r in rows:
    if r['mode']=='TPU':
        md.append(f"| {r['candidate']} | {r['profile']} | {r['modules']} | {r['total_power_w']} | {r['effective_tops']} | {r['tops_per_w']} | {r['pj_mac_eff']} |")
md+=['','## Lectura','- G2/G3 muestran mejor TOPS/W proxy por menor pJ/MAC base; H3 mantiene buen balance con mayor apertura/NV; H1/H4 pagan overheads de escala/redundancia.','- Los fijos (E/O-O/E, láser, control, refrigeración) dominan en configuraciones pequeñas (edge) y deben medirse; el dinámico escala con utilización/modos.','- Usar para comparar tendencias relativas, no para especificación de producto.']
open(os.path.join(OUT,'power_energy_budget.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    for pk in PROFILES:
        sub=[r for r in rows if r['profile']==pk and r['mode']=='TPU']
        fig,ax=plt.subplots(figsize=(6.5,3.8))
        ax.bar([r['candidate'] for r in sub],[r['tops_per_w'] for r in sub], color='#4c78a8')
        ax.set_ylabel('TOPS/W (proxy)'); ax.set_title(f'Eficiencia energética proxy por candidato ({pk}, TPU)')
        fig.tight_layout(); fig.savefig(os.path.join(FIG,f'power_{pk}.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/power_energy_budget.*'}))
