#!/usr/bin/env python3
"""Integrated architecture operating envelope and recommendations (conceptual).
Combines S1 (link/thermal duty-layout), S2 (profiles), S3 (OpenVINO partition/queues),
and S4 (yield/cost overhead) to suggest architecture choices by candidate/profile.
No measurements; for planning only.
"""
from __future__ import annotations
import csv, json, os, math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)

def load_json(p):
    with open(p,encoding='utf-8') as f: return json.load(f)

def max_duty_from_sweep(path):
    # returns {(cand,layout): {'nom':x,'worst':y}}
    res={}
    with open(path,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            k=(r['candidate'], r['layout']); d=float(r['duty_cycle'])
            fn = str(r.get('feasible_nominal','')).lower() in ('true','1','sí','si')
            fw = str(r.get('feasible_worst_case','')).lower() in ('true','1','sí','si')
            if k not in res: res[k]={'nom':0.0,'worst':0.0}
            if fn: res[k]['nom']=max(res[k]['nom'], d)
            if fw: res[k]['worst']=max(res[k]['worst'], d)
    return res

S1 = load_json(os.path.join(OUT,'s1_link_thermal.json'))
S2 = load_json(os.path.join(OUT,'s2_system_profiles.json'))
S3 = load_json(os.path.join(OUT,'s3_pcie_openvino.json'))
S4 = load_json(os.path.join(OUT,'s4_cost_overhead.json'))
duty = max_duty_from_sweep(os.path.join(OUT,'s1_layout_duty.csv')) if os.path.exists(os.path.join(OUT,'s1_layout_duty.csv')) else {}

# S3 partition summary: best recommended coverage per graph among C/D (near-term) and A (target)
part = S3.get('openvino_partition_results', [])
def part_pick(graph, routes):
    rows=[r for r in part if r['graph']==graph and r['route'] in routes]
    if not rows: return None
    return max(rows, key=lambda r: r['offload_coverage'])
graphs=['CNN_inference','Transformer_encoder_block','MLP_classifier']

CANDS = {r['key']: r for r in S1.get('candidates',[])}
S4rows = {r['key']: r for r in S4.get('rows',[])}

# reference reconfig capability proxy from candidate type (conceptual)
RECONFIG = {
    'H3': {'class':'PCM NV (slow write)','reconfig_s':2e-5,'nv':True},
    'G2': {'class':'EO-tuned fast','reconfig_s':1e-10,'nv':False},
    'G3': {'class':'PCM+EO hybrid','reconfig_s':5e-10,'nv':True},
    'H1': {'class':'3D NV (PCM/VO2)','reconfig_s':1e-9,'nv':True},
    'H4': {'class':'3D tensor (mixed)','reconfig_s':5e-10,'nv':True},
}

profiles = S2.get('profiles',{})
# base per-tile effective capacity proxy (from S4 tops_effective for a module class) scaled to profile needs
# use S4 effective tops as module-level reference and compare to S2 targets
rows=[]
for ck in ['H3','G2','G3','H1','H4']:
    s4 = S4rows.get(ck,{})
    s1 = CANDS.get(ck,{})
    link_ok = s1.get('link_feasible', False)
    link_margin = s1.get('link_margin_db')
    recal = s1.get('recalibrated') or {}
    therm_nom = recal.get('thermal_feasible_nominal', s1.get('thermal_feasible_nominal'))
    therm_worst = recal.get('thermal_feasible_worst_case', s1.get('thermal_feasible_worst_case'))
    tops_eff = s4.get('tops_effective', 0)
    mem_eff = s4.get('mem_effective_mb', 0)
    ret = s4.get('net_capacity_retention_tops', 0)
    e_over = s4.get('energy_overhead_factor', 1.0)
    l_over = s4.get('latency_overhead_factor', 1.0)
    # layout recommendation
    best_layout='baseline'; best_dw=0.0
    for lay in ['spread_out','baseline','compact']:
        dk = duty.get((ck,lay))
        if dk and dk['worst']>=best_dw:
            best_dw=dk['worst']; best_layout=lay
    max_dn = duty.get((ck,best_layout),{}).get('nom', 0.0)
    max_dw = duty.get((ck,best_layout),{}).get('worst', 0.0)
    # reconfig/write budget proxy (higher duty allowed => more write/reconfig scheduling headroom for PCM)
    write_budget = 'high' if max_dw>=0.12 else ('medium' if max_dw>=0.08 else ('low' if max_dw>0 else 'n/a'))
    for pk, pv in profiles.items():
        tgt_tops = (pv.get('targets') or {}).get('tops', 0)
        tgt_lat = (pv.get('targets') or {}).get('latency_ms', 0)
        # modules needed (rough) to meet profile target tops with effective module tops
        mods = math.ceil(tgt_tops / tops_eff) if tops_eff>0 else None
        tops_fit = (tops_eff >= tgt_tops) or (mods is not None and mods <= (1 if pk=='edge' else (4 if pk=='ws' else 16)))
        # profile fit heuristic
        score = 0.0
        if link_ok: score += 0.2
        if therm_nom: score += 0.2
        elif max_dn>0: score += 0.1
        if therm_worst or max_dw>=0.08: score += 0.15
        elif max_dw>0: score += 0.08
        # performance fit
        if tops_fit: score += 0.2
        elif tops_eff>=0.5*tgt_tops: score += 0.1
        # memory/persistence fit
        if RECONFIG[ck]['nv']: score += 0.1
        if pk=='edge' and ck in ('H3','G3','G2'): score += 0.05
        if pk=='ws' and ck in ('H3','G3','G2','H1'): score += 0.03
        if pk=='dc' and ck in ('H1','H4','G3'): score += 0.05
        # yield/cost simplicity
        score += 0.1 * min(1.0, ret/0.9)
        fit = 'alta' if score>=0.75 else ('media' if score>=0.55 else 'baja')
        # OV route suggestion
        if pk=='edge': ov='C/D (heterogéneo/compilado)'
        elif pk=='ws': ov='C/D inicial → B/A con madurez'
        else: ov='B/A objetivo (con fallback C en subgrafos mixtos)'
        # architecture suggestion
        if ck in ('H3','G3'):
            arch='2.5D modular (tiles WDM/membrana), OMCC secuenciado, PCIe+OpenCL ICD; pesos NV en PCM, control térmico por duty/layout'
        elif ck=='G2':
            arch='2.5D EO de alta velocidad (menor NV), buffers M2/M3 y refresh; ideal reconfig dinámica con gestión térmica EO'
        else:
            arch='3D particionado jerárquico, spread-out + manifold/vías térmicas, redundancia/re-mapeo OMCC, integración gradual desde 2.5D'
        rows.append({
            'candidate': ck, 'profile': pk, 'fit': fit, 'fit_score': round(score,3),
            'link_feasible': link_ok, 'link_margin_db': link_margin,
            'thermal_nominal': bool(therm_nom), 'thermal_worst_case': bool(therm_worst),
            'recommended_layout': best_layout, 'max_duty_nominal': max_dn, 'max_duty_worst': max_dw,
            'write_reconfig_budget': write_budget,
            'module_tops_effective': tops_eff, 'module_mem_effective_mb': mem_eff,
            'profile_target_tops': tgt_tops, 'modules_est_for_target': mods,
            'capacity_retention': ret, 'energy_overhead_x': e_over, 'latency_overhead_x': l_over,
            'reconfig_class': RECONFIG[ck]['class'], 'nonvolatile': RECONFIG[ck]['nv'],
            'suggested_openvino_route': ov, 'architecture_recommendation': arch,
        })

# OV coverage summary for report
ov_summary=[]
for g in graphs:
    a=part_pick(g,['A_native']); c=part_pick(g,['C_hetero']); d=part_pick(g,['D_compiled'])
    ov_summary.append({'graph':g,'A':a and a['offload_coverage'],'C':c and c['offload_coverage'],'D':d and d['offload_coverage']})

out={'rows':rows,'openvino_graph_coverage':ov_summary,
     'disclaimer':'Conceptual integrated envelope from S1-S4 outputs (no measurements). Scores/fit are planning heuristics, not signoff.'}
with open(os.path.join(OUT,'architecture_operating_envelope.json'),'w',encoding='utf-8') as f: json.dump(out,f,indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'architecture_operating_envelope.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)

# markdown report
md=['# Envolvente operativa integrada y sugerencias de arquitectura (S1–S4, conceptual)','',
    '> Combina S1 (enlace/térmico, duty/layout), S2 (perfiles), S3 (colas/partición OpenVINO) y S4 (yield/coste). Planificación, no mediciones ni signoff.','',
    '## Resumen por candidato y perfil','',
    '| Candidato | Perfil | Ajuste | Score | Layout | Duty máx nom | Duty máx peor | TOPS ef. módulo | Obj. TOPS | Módulos est. | Retención | Presupuesto write/reconfig | Ruta OpenVINO |',
    '|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|']
for r in rows:
    md.append(f"| {r['candidate']} | {r['profile']} | {r['fit']} | {r['fit_score']} | {r['recommended_layout']} | {r['max_duty_nominal']} | {r['max_duty_worst']} | {r['module_tops_effective']} | {r['profile_target_tops']} | {r['modules_est_for_target']} | {r['capacity_retention']} | {r['write_reconfig_budget']} | {r['suggested_openvino_route']} |")

md+=['','## Cobertura OpenVINO por grafo (rutas clave, S3)','',
     '| Grafo | A (nativo, objetivo) | C (heterogéneo, corto plazo) | D (compilado, corto plazo) |',
     '|---|---:|---:|---:|']
for o in ov_summary:
    md.append(f"| {o['graph']} | {o['A']} | {o['C']} | {o['D']} |")

# recommendations
md+=['','## Sugerencias de arquitectura basadas en cálculos','']
recs=[
 ('**Base recomendada (menor riesgo, abierta): H3 2.5D (A1+G1+B3)**','Edge/workstation: 1 módulo clase H3 (3.01 TOPS ef., 138 MB ef.) cubre objetivos S2 con margen; usar layout baseline/spread-out y OMCC con duty de escritura ≤0.12 (peor caso seguro)–0.18 (nominal) para respetar VO₂. Persistencia NV en PCM + pasivos G1 favorecen acceso abierto y estabilidad; ruta OpenVINO C/D inicial.'),
 ('**Rendimiento/BW con equilibrio NV: G3 2.5D (PCM+EO)**','Cuando se requiera mayor BW/TOPS (workstation/datacenter) con NV: G3 ofrece 4.45 TOPS ef. y mejor densidad (0.125 TOPS/cm² ef.) con overhead bajo; requiere co-gestión térmica PCM/EO y layout spread-out para headroom de duty. Evolucionar a rutas B/A.'),
 ('**Reconfiguración rápida (sin NV fuerte): G2 EO**','Para cargas dinámicas donde prima velocidad de reconfiguración sobre persistencia, usar G2 con buffers/refresco M2–M3 y partición heterogénea (fallback para estado persistente si aplica).'),
 ('**Capacidad/escalado (alto riesgo controlado): H1/H4 3D**','Para datacenter/capacidad: H1/H4 alcanzan mayor TOPS/Mem efectivos por módulo tras optimización pero exigen particionado jerárquico, layout spread-out, manifold/vías térmicas, redundancia 22–26% y re-mapeo OMCC. Introducir gradualmente sobre base 2.5D validada (E2→E4).'),
 ('**Plataforma común y software**','Mantener interfaz PCIe/DMA/MSI-X + ICD OpenCL común; particionar grafos (CNN/MLP favorables en C/D, transformer con más fallback hasta madurar A/B). Usar colas profundas, batching y coalescing para sostener throughput (S3).'),
 ('**Térmica/fiabilidad (condición habilitante)**','Secuenciado OMCC y límites de duty por layout son obligatorios en candidatos PCM; co-optimizar redundancia con retención efectiva (S4) y calibración en lazo cerrado.'),
]
for t,b in recs:
    md.append(f"### {t}")
    md.append(b); md.append('')

md+=['## Simulaciones adicionales factibles (sin mediciones nuevas)','',
     '- **FEM térmico 3D transitorio** (herramienta externa) calibrado con layout real: cerrar márgenes VO₂/rings y densidad de escritura.',
     '- **Modelo de ruido/E/O-O/E y cuantización** acoplado a márgenes S1: estimar exactitud efectiva vs bit-depth y potencia óptica.',
     '- **Simulador funcional de runtime OpenCL/ICD + partición de grafos reales** (trazas): validar fallback, latencia de colas y BW efectivo (extiende S3).',
     '- **Barrido de fiabilidad temporal/endurance** con tasas de refresco M2 y write-rate limitados por duty térmico (extiende P2/S4).',
     '- **Optimización multiobjetivo (Pareto costo/TOPS/W/retención)** usando `objective_combo_analysis` + S4 coste para selección de configuración por perfil.','']

with open(os.path.join(OUT,'architecture_operating_envelope.md'),'w',encoding='utf-8') as f: f.write('\n'.join(md)+'\n')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cands=['H3','G2','G3','H1','H4']; profs=['edge','ws','dc']
    fig,ax=plt.subplots(figsize=(7.5,3.8))
    for pk,marker in [('edge','o'),('ws','s'),('dc','^')]:
        xs=[next(r['capacity_retention'] for r in rows if r['candidate']==c and r['profile']==pk) for c in cands]
        ys=[next(r['fit_score'] for r in rows if r['candidate']==c and r['profile']==pk) for c in cands]
        ax.scatter(xs,ys,label=pk,marker=marker)
        for i,c in enumerate(cands): ax.annotate(c,(xs[i],ys[i]),fontsize=7,xytext=(3,3),textcoords='offset points')
    ax.set_xlabel('Retención de capacidad efectiva (S4)'); ax.set_ylabel('Score de ajuste integrado (S1–S4)')
    ax.set_title('Envolvente integrada: ajuste por candidato/perfil (conceptual)'); ax.legend(); ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG,'architecture_operating_envelope.png'),dpi=150); plt.close(fig)
except Exception as e:
    print('figure_warning',e)

print(json.dumps({'rows':len(rows),'out':'outputs/architecture_operating_envelope.*'}))
