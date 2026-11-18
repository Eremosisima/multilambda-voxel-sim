#!/usr/bin/env python3
"""Analog noise + E/O-O/E + quantization accuracy proxy (conceptual).
Combines S1 link margins and S4 phase/IL/error stats to estimate effective accuracy vs bit-depth.
No measured models.
"""
from __future__ import annotations
import csv,json,os,math,random
OUT='outputs'; FIG='figures'; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
random.seed(11)
S1=json.load(open(os.path.join(OUT,'s1_link_thermal.json'),encoding='utf-8'))
S4=json.load(open(os.path.join(OUT,'s4_variability_yield.json'),encoding='utf-8'))

# pick optimized+improved_process results for candidates as representative
def s4_best(key):
    rs=[r for r in S4.get('results',[]) if r.get('key')==key and r.get('variant')=='optimized']
    if rs:
        return max(rs, key=lambda r: r['effective_yield_after_redundancy'])
    # fallback conceptual for candidates without S4 variability data (e.g. G2 EO)
    fallbacks={
        'G2': {'snr_db':{'mean':16.5}, 'phase_error':{'mean':0.035}, 'insertion_loss_db':{'mean':8.5}},
    }
    return fallbacks.get(key, {'snr_db':{'mean':12.0}, 'phase_error':{'mean':0.06}, 'insertion_loss_db':{'mean':12.0}})

BIT_DEPTHS=[4,6,8]
CALIB=['none','static','closed_loop']
WORKLOADS=[('CNN_inference','conv-heavy',0.8),('MLP_classifier','gemm-heavy',0.9),('Transformer_encoder_block','mixed-attn',0.7)]

rows=[]
for c in S1['candidates']:
    k=c['key']; link_m=c['link_margin_db']; il=c['insertion_loss_db']
    s=s4_best(k); snr=s['snr_db']['mean']; pe=s['phase_error']['mean']; ilv=s['insertion_loss_db']['mean']
    # noise sigma proxy (normalized) from SNR and phase error
    sigma_analog = max(0.002, 0.06/(10**(snr/20.0)) + 0.25*pe + 0.005*max(0, ilv-10))
    for bits in BIT_DEPTHS:
        q_step = 2.0/(2**bits)
        sigma_q = q_step/math.sqrt(12)
        for calib in CALIB:
            cal_factor = 1.0 if calib=='none' else (0.7 if calib=='static' else 0.45)
            drift = 0.03 if calib=='none' else (0.015 if calib=='static' else 0.006)
            sigma_total = math.sqrt((sigma_analog*cal_factor + drift)**2 + sigma_q**2)
            # map to proxy accuracy penalty per workload sensitivity
            for wname,wtype,sens in WORKLOADS:
                pen = min(0.35, sens * sigma_total * 1.8)
                acc = max(0.5, 1.0 - pen)
                # effective bit-equivalent
                eff_bits = max(1.0, -math.log2(max(sigma_total,1e-6)) - 0.5)
                rows.append({'candidate':k,'bit_depth':bits,'calibration':calib,'workload':wname,'workload_type':wtype,
                             'link_margin_db':link_m,'snr_db_mean':snr,'phase_error_mean':pe,
                             'sigma_analog':round(sigma_analog,5),'sigma_quant':round(sigma_q,5),'sigma_total':round(sigma_total,5),
                             'accuracy_proxy':round(acc,4),'accuracy_penalty':round(pen,4),'effective_bits_equiv':round(eff_bits,2)})

# summary recommended operating points
recs=[]
for k in ['H3','G3','H1','H4','G2']:
    sub=[r for r in rows if r['candidate']==k and r['calibration']=='closed_loop' and r['workload']=='CNN_inference']
    if not sub: continue
    b8=next((r for r in sub if r['bit_depth']==8), None); b6=next((r for r in sub if r['bit_depth']==6), None)
    recs.append({'candidate':k,'acc_cnn_int8_closed_loop':b8['accuracy_proxy'] if b8 else None,'acc_cnn_int6_closed_loop':b6['accuracy_proxy'] if b6 else None,'eff_bits_int8':b8['effective_bits_equiv'] if b8 else None})

out={'rows':rows,'recommendations':recs,'note':'Proxy model (not a trained-accuracy result). Maps S1/S4 margins to quantization+analog noise penalty; calibrate with measured ADC/DAC/E-O noise and real inference accuracy.'}
json.dump(out,open(os.path.join(OUT,'accuracy_quantization.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
cols=list(rows[0].keys())
with open(os.path.join(OUT,'accuracy_quantization.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
md=['# Precisión analógica y cuantización (proxy, conceptual)','',
    '> Combina márgenes S1 (enlace/IL) y estadísticas S4 (SNR, error de fase, IL) con ruido de cuantización para estimar exactitud relativa y bits efectivos. No son resultados de inferencia real.','',
    '## Puntos recomendados (calibración en lazo cerrado, CNN)','',
    '| Candidato | Acc. proxy INT8 | Acc. proxy INT6 | Bits efectivos (INT8) |','|---|---:|---:|---:|']
for r in recs:
    md.append(f"| {r['candidate']} | {r['acc_cnn_int8_closed_loop']} | {r['acc_cnn_int6_closed_loop']} | {r['eff_bits_int8']} |")
md+=['','## Lectura','- INT8 con calibración en lazo cerrado ofrece el mejor compromiso para H3/G3; INT6 es viable con mayor sensibilidad en cargas mixtas/Transformer.','- H1/H4 requieren mejor control de fase/IL y calibración para sostener bits efectivos altos debido a mayor varianza (S4).','- Calibrar con mediciones E/O-O/E, ruido de fotodetección/ADC/DAC y exactitud de inferencia por modelo.']
open(os.path.join(OUT,'accuracy_quantization.md'),'w',encoding='utf-8').write('\n'.join(md)+'\n')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    for wname in ['CNN_inference','Transformer_encoder_block']:
        fig,ax=plt.subplots(figsize=(6.5,3.6))
        for calib,ls in [('none','--'),('closed_loop','-')]:
            for bits,m in [(4,'o'),(8,'s')]:
                xs=[]; ys=[]
                for k in ['H3','G3','H1','H4','G2']:
                    r=next((x for x in rows if x['candidate']==k and x['bit_depth']==bits and x['calibration']==calib and x['workload']==wname),None)
                    if r: xs.append(k); ys.append(r['accuracy_proxy'])
                if xs: ax.plot(xs,ys,marker=m,ls=ls,label=f'{bits}b {calib}')
        ax.set_ylim(0.5,1.02); ax.set_ylabel('Accuracy proxy'); ax.set_title(f'Exactitud proxy vs cuantización/calibración ({wname})')
        ax.legend(fontsize=7,ncol=2); fig.tight_layout(); fig.savefig(os.path.join(FIG,f'accuracy_quant_{wname}.png'),dpi=150); plt.close(fig)
except Exception as e: print('figure_warning',e)
print(json.dumps({'rows':len(rows),'out':'outputs/accuracy_quantization.*'}))
