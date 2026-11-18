#!/usr/bin/env python3
"""Thermal drift temporal model and resonance stability (conceptual, reference-informed).
Uses ring thermo-optic sensitivity (~80 pm/K) and PCM thermal loads to estimate detuning,
control overhead and stability windows.
"""
from __future__ import annotations
import csv,json,os,math,random
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
random.seed(21)
ref=json.load(open(os.path.join('data','reference_params_supplement.json'),encoding='utf-8')) if os.path.exists(os.path.join('data','reference_params_supplement.json')) else {}
RING=ref.get('microring_thermal',{})
DRIFT_PM_K=RING.get('wavelength_drift_pm_per_K_typical',80)
TUNE_NM_MW=RING.get('thermal_tuning_efficiency_nm_per_mW_typical',0.08)
FSR_NM=RING.get('fsr_nm_typical',5.0)
Q=RING.get('q_factor_typical',1e4)

# candidate thermal environments (ambient/control + self-heating deltaT over time windows)
CANDS={
 'H3': {'pcm_writes':True,'rings':True,'eo':False,'base_dT_C':(2,8),'write_pulse_dT_C':(15,35),'thermal_mass':'medium'},
 'G3': {'pcm_writes':True,'rings':True,'eo':True,'base_dT_C':(3,10),'write_pulse_dT_C':(12,30),'thermal_mass':'medium'},
 'G2': {'pcm_writes':False,'rings':True,'eo':True,'base_dT_C':(3,12),'write_pulse_dT_C':(0,0),'thermal_mass':'low'},
 'H1': {'pcm_writes':True,'rings':True,'eo':True,'base_dT_C':(4,12),'write_pulse_dT_C':(18,40),'thermal_mass':'high'},
 'H4': {'pcm_writes':True,'rings':True,'eo':True,'base_dT_C':(5,14),'write_pulse_dT_C':(20,45),'thermal_mass':'high'},
}
CONTROLS=[('open_loop',0.0,0.0),('static_calibration',0.5,0.2),('closed_loop_a',0.8,0.6),('closed_loop_b_fast',0.92,1.0)] # (name, drift_suppression, power_overhead_factor_rel)

rows=[]
dt=0.001 # s
T=0.2 # 200 ms window
steps=int(T/dt)
for ck,c in CANDS.items():
    for ctrl, sup, ctrl_pow in CONTROLS:
        # simulate temperature over time: base + slow drift + write pulses (if PCM) + noise
        temp=25.0 + c['base_dT_C'][0]
        slow_rate=(c['base_dT_C'][1]-c['base_dT_C'][0])/(T*2)
        detunings=[]; tune_powers=[]; stable=0
        # resonance linewidth approx lambda/Q at 1550nm
        linewidth_nm = 1550e-9/Q*1e9
        tol_nm = linewidth_nm*0.25 # stability tolerance fraction
        for i in range(steps):
            t=i*dt
            # ambient/slow drift
            temp += slow_rate*dt + random.gauss(0,0.002)
            pulse=0.0
            if c['pcm_writes'] and (i%20000<50): # occasional write burst
                pulse = random.uniform(*c['write_pulse_dT_C'])*math.exp(-((i%20000)/30.0))
            dT = (temp-25.0) + pulse*0.15 # coupled fraction to rings
            drift_nm = (DRIFT_PM_K * dT)/1000.0
            resid = drift_nm*(1-sup)
            # tuning power to correct residual (if control active)
            p_mw = max(0.0, (abs(resid)/TUNE_NM_MW)*1000.0) if TUNE_NM_MW>0 else 0.0
            p_mw *= ctrl_pow
            detunings.append(abs(resid)); tune_powers.append(p_mw)
            if abs(resid)<=tol_nm: stable+=1
        avg_det=sum(detunings)/len(detunings); p95=sorted(detunings)[int(0.95*len(detunings))]
        avg_p=sum(tune_powers)/len(tune_powers); p95p=sorted(tune_powers)[int(0.95*len(tune_powers))]
        stab_frac=stable/len(detunings)
        rows.append({'candidate':ck,'control':ctrl,'drift_pm_per_K_ref':DRIFT_PM_K,'tuning_nm_per_mW_ref':TUNE_NM_MW,
                     'linewidth_nm':round(linewidth_nm,5),'tolerance_nm':round(tol_nm,5),
                     'avg_detuning_nm':round(avg_det,5),'p95_detuning_nm':round(p95,5),
                     'avg_tuning_power_mw':round(avg_p,4),'p95_tuning_power_mw':round(p95p,4),
                     'stability_fraction':round(stab_frac,4),'stable':stab_frac>=0.95})

out={'rows':rows,'refs':RING,'note':'Conceptual transient drift model (simplified RC-like/pulse coupling). Calibrate with measured thermo-optic response, heater efficiency and control loop bandwidth.'}
json.dump(out,open(os.path.join(OUT,'thermal_drift_stability.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'thermal_drift_stability.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Deriva térmica temporal y estabilidad de resonancias (conceptual, informado por referencia)','',
    f"> Sensibilidad de referencia: {DRIFT_PM_K} pm/K, tuning ~{TUNE_NM_MW} nm/mW (Si ring típico). Modelo transitorio simplificado; calibrar con respuesta medida y lazo de control.",'',
    '## Resumen','',
    '| Candidato | Control | Detuning medio (nm) | Detuning p95 (nm) | Potencia tuning media (mW) | Potencia tuning p95 (mW) | Fracción estable | Estable (>=95%) |','|---|---|---:|---:|---:|---:|---:|:---:|']
for r in rows:
    md.append(f"| {r['candidate']} | {r['control']} | {r['avg_detuning_nm']} | {r['p95_detuning_nm']} | {r['avg_tuning_power_mw']} | {r['p95_tuning_power_mw']} | {r['stability_fraction']} | {'sí' if r['stable'] else 'no'} |")
md+=['','## Lectura','- Sin control en lazo cerrado, los candidatos con escritura PCM/anillos muestran mayor detuning transitorio; lazos cerrados (A/B) recuperan estabilidad a costa de potencia de control.','- G2 (sin escrituras PCM 300°C) reduce pulsos térmicos pero sigue requiriendo estabilización EO/anillos.','- H1/H4 concentran mayor carga térmica; necesitan aislamiento, secuenciado y control rápido para mantener resonancias dentro de tolerancia.']
open(os.path.join(OUT,'thermal_drift_stability.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    cands=list(CANDS.keys()); ctrls=[c[0] for c in CONTROLS]; x=range(len(cands)); w=0.18
    fig,ax=plt.subplots(figsize=(8.5,4))
    for i,ct in enumerate(ctrls):
        vals=[next(r['stability_fraction'] for r in rows if r['candidate']==c and r['control']==ct) for c in cands]
        ax.bar([xi+(i-1.5)*w for xi in x], vals, w, label=ct)
    ax.set_xticks(list(x)); ax.set_xticklabels(cands); ax.set_ylim(0,1.05); ax.axhline(0.95,color='k',ls='--',lw=1)
    ax.set_ylabel('Fracción estable'); ax.set_title('Estabilidad de resonancia vs control térmico (conceptual)'); ax.legend(fontsize=7,ncol=2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG,'thermal_drift_stability.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/thermal_drift_stability.*'}))
