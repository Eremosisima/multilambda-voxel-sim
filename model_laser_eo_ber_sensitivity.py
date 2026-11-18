#!/usr/bin/env python3
"""Laser/E-O power sensitivity sweeps coupled to BER/accuracy proxy (conceptual).
Explores optical power, modulator ER/bias, and noise to estimate BER/accuracy operating window.
"""
from __future__ import annotations
import csv,json,os,math
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
S1={r['key']:r for r in json.load(open(os.path.join(OUT,'s1_link_thermal.json'),encoding='utf-8'))['candidates']}

def qfunc(x):
    # approx erfc(x/sqrt(2))/2
    return 0.5*math.erfc(x/math.sqrt(2))

LASER_DBM=[-2,0,2,4,6,8]
ER_DB=[4,6,8,10]
BIAS_OFFSET=[-0.15,-0.05,0.0,0.05,0.15] # relative bias error
RIN_DBHZ=-145
BW_GHZ=10
NOISE_FLOOR_DBM=-28

rows=[]
for ck,c in S1.items():
    il=c['insertion_loss_db']; base_margin=c['link_margin_db']
    for p in LASER_DBM:
        for er in ER_DB:
            # extinction ratio penalty and signal swing
            er_lin=10**(er/10.0)
            swing_factor=(er_lin-1)/(er_lin+1)
            for b in BIAS_OFFSET:
                bias_pen=1.0 - 2.0*abs(b)
                rx = p - il + 10*math.log10(max(swing_factor*bias_pen,1e-3)**2)
                snr_db = rx - NOISE_FLOOR_DBM + 0.1*(p) # crude
                # BER proxy for OOK-like equivalent
                q = 10**(snr_db/20.0)/2.5
                ber=max(1e-15, min(0.5, qfunc(max(0,q))))
                # map to inference accuracy proxy (system-level)
                acc = max(0.5, 1.0 - 0.02*max(0, 12-snr_db) - 0.15*max(0,0.2-abs(bias_pen-1))*0)
                acc = max(0.5, 1.0 - 0.015*max(0, 14-snr_db) - 0.08*abs(b))
                ok = (ber<=1e-9 and acc>=0.9)
                rows.append({'candidate':ck,'laser_dbm':p,'er_db':er,'bias_offset':b,
                             'rx_dbm_proxy':round(rx,3),'snr_db_proxy':round(snr_db,3),'ber_proxy':f'{ber:.3e}',
                             'accuracy_proxy':round(acc,4),'operating_point_ok':ok,'il_db':il})

# best operating points
best=[]
for ck in S1.keys():
    okrows=[r for r in rows if r['candidate']==ck and r['operating_point_ok']]
    if okrows:
        b=min(okrows,key=lambda r:(r['laser_dbm'], -r['snr_db_proxy']))
        best.append({'candidate':ck,'min_laser_dbm_ok':b['laser_dbm'],'er_db':b['er_db'],'bias_offset':b['bias_offset'],'snr_db':b['snr_db_proxy'],'accuracy':b['accuracy_proxy']})
    else:
        b=max([r for r in rows if r['candidate']==ck], key=lambda r:r['snr_db_proxy'])
        best.append({'candidate':ck,'min_laser_dbm_ok':None,'er_db':b['er_db'],'bias_offset':b['bias_offset'],'snr_db':b['snr_db_proxy'],'accuracy':b['accuracy_proxy'],'note':'no point met BER/acc threshold'})

out={'rows':rows,'best_points':best,'note':'Conceptual laser/modulator/noise sweep to BER/accuracy proxy. Replace with measured RIN, PD noise, ER, DAC/driver linearity and link BER.'}
json.dump(out,open(os.path.join(OUT,'laser_eo_ber_sensitivity.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'laser_eo_ber_sensitivity.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Sensibilidad láser/E-O acoplada a BER/exactitud (proxy, conceptual)','',
    '> Barrido de potencia láser, ER y sesgo con ruido equivalente para estimar ventana operativa (BER/accuracy proxy).','',
    '## Mejores puntos operativos (umbral BER<=1e-9 y acc>=0.9)','',
    '| Candidato | Láser mín. OK (dBm) | ER (dB) | Sesgo | SNR proxy (dB) | Accuracy proxy |','|---|---:|---:|---:|---:|---:|']
for b in best:
    md.append(f"| {b['candidate']} | {b.get('min_laser_dbm_ok')} | {b['er_db']} | {b['bias_offset']} | {b['snr_db']} | {b['accuracy']} |")
md+=['','## Lectura','- Mayor IL (H1/H4) exige más potencia láser y mejor ER/sesgo para mantener margen de SNR; H3/G3/G2 operan con menor potencia relativa.','- La calibración de sesgo y ER efectivo es crítica para exactitud analógica; integrar con control en lazo cerrado y cuantización (modelo de accuracy).','- Validar con mediciones de RIN, responsividad/ruido de PD, linealidad E/O y BER/enlace real.']
open(os.path.join(OUT,'laser_eo_ber_sensitivity.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    # heat-like lines: acc vs laser for ER=8,bias=0
    fig,ax=plt.subplots(figsize=(7,4))
    for ck in S1.keys():
        sub=[r for r in rows if r['candidate']==ck and r['er_db']==8 and r['bias_offset']==0.0]
        sub=sorted(sub,key=lambda x:x['laser_dbm'])
        ax.plot([r['laser_dbm'] for r in sub],[r['accuracy_proxy'] for r in sub], marker='o', label=ck)
    ax.axhline(0.9,color='k',ls='--',lw=1); ax.set_xlabel('Potencia láser (dBm)'); ax.set_ylabel('Accuracy proxy')
    ax.set_title('Sensibilidad potencia láser (ER=8dB, sesgo=0)'); ax.legend(); fig.tight_layout()
    fig.savefig(os.path.join(FIG,'laser_eo_sensitivity.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'best':len(best),'out':'outputs/laser_eo_ber_sensitivity.*'}))
