# Artículo B (borrador, ES): Simulación paramétrica de lectura interferométrica por fase y presupuesto de SNR para memoria óptica multinivel

**Tipo:** simulación de dispositivo/lectura (modelo de primer orden, sin prototipo).  
**Contribución propia:** análisis paramétrico de `Δφ`, márgenes de cuantización y presupuesto simplificado de ruido de fase bajo distintos regímenes de potencia/ancho de banda y geometría efectiva.

## Resumen
Se estudia mediante simulación la lectura por fase en un esquema interferométrico equivalente, donde el cambio de fase efectivo se modela como `Δφ = (2π/λ)·Γ·Δn·L`. Para un conjunto de canales de lectura y niveles discretos, se evalúan los pasos de fase por nivel, la robustez frente a ruido aditivo y desajuste de calibración, y un presupuesto de SNR simplificado (ruido de disparo y deriva termo-óptica) en función de potencia óptica y ancho de banda. Los resultados delimitan márgenes operativos en escenarios paramétricos y destacan la necesidad de presupuestos físicos completos para predicciones de sistema.

## 1. Introducción
- Lectura de fase en interferómetros integrados como mecanismo de transducción de cambios de índice efectivos.
- Alcance: simulación paramétrica; no se reportan mediciones.

## 2. Modelo de fase y lectura
- `Δφ_i(λ_j,L,Γ,Δn_i) = (2π/λ_j)·Γ·Δn_i·L` (aproximación efectiva).
- Paso por nivel: `Δφ_i/(L-1)` para `L` niveles; margen de cuantización ≈ medio paso.
- Matriz de lectura y decodificación (resumen) con términos de fuga efectivos.

## 3. Métodos
- Barridos de L, Γ, escala de Δn y crosstalk efectivo.
- Monte Carlo para ruido gaussiano en fase y error relativo de calibración.
- Presupuesto SNR: `σ_shot ≈ 1/sqrt(N_ph)` (simplificado), deriva termo-óptica `σ_th ~ (2π/λ)·Γ·(dn/dT)·ΔT·L`, `σ_total = sqrt(σ_shot^2 + σ_th^2)`.
- Código/datos: `../../mzi_sim.py`, `../../sensitivity.py`, `../../snr_budget.py`, `../../outputs/mzi_*`, `../../outputs/sensitivity_*`, `../../outputs/snr_budget.*`, `../../figures/*.png`.

## 4. Resultados
- Caso base (L=100 µm, Γ=0.35, supuestos de Δn): pasos ~2.6–3.0 rad/nivel por canal.
- Sensibilidad: el paso medio varía ~0.20–12.02 rad en el barrido de diseño; los márgenes de decodificación dependen críticamente de estos parámetros.
- Presupuesto SNR (modelo simplificado): 48 escenarios evaluados; viabilidad condicionada a supuestos de visibilidad, RIN, NEP y control térmico no incluidos.

## 5. Discusión
- Diferencia entre márgenes de fase ideales y limitaciones prácticas (pérdidas, visibilidad, ruido 1/f, cuantización electrónica, deriva).
- Requisitos para futura validación: simulación electromagnética y caracterización experimental.

## 6. Conclusiones
- La lectura por fase puede ofrecer márgenes amplios en ciertos regímenes paramétricos, pero la factibilidad de sistema requiere modelos de ruido y fabricación más completos.

## Disponibilidad y declaraciones
- Ver `../../README.md`, `../../CITATION.cff`. Declarar conflictos, financiamiento y uso de herramientas según política editorial.
