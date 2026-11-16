# Lista de compuestos candidatos para memoria óptica multiplexada (y espectros a obtener)

> **Objetivo:** seleccionar 4+ fotoswitches con bandas de activación/escritura/borrado/lectura lo más ortogonales posible, buen `Δn`, estabilidad adecuada y respuesta caracterizable. Los rangos indicados son **típicos/orientativos** (varían con sustituyentes y matriz); para el modelo Beer-Lambert y de fase se requieren **espectros medidos/citados** de cada estado/conformero en las condiciones de uso.

## 1. Candidatos prioritarios (familias y ejemplos)

| # | Familia | Ejemplos concretos (punto de partida) | Estado A (conformero 1) – absorción típica | Estado B (conformero 2) – absorción típica | Ventajas para este fin | Retos / qué vigilar | Espectros/datos a conseguir (por estado) |
|---|---|---|---|---|---|---|---|
| M1 | **Diariletenos (DAE/DTE)** (tipo P, térmicamente estables) | 1,2-bis(2,4-dimethyl-5-phenyl-3-thienyl)perfluorocyclopentene; 1,2-bis(2-methyl-5-phenyl-3-thienyl)perfluorocyclopentene; derivados sustituidos para desplazar λ | Anillo abierto: UV fuerte (≈250–330 nm), baja absorción en visible | Anillo cerrado: visible (≈450–650 nm según derivado), distinto perfil UV | Alta estabilidad térmica de ambos estados (en muchos derivados), buena fatiga, `Δn` relevante en polímeros/cristales, respuesta bien estudiada | Saturación/no linealidad posible, solapamiento de colas, dependencia de matriz; Φ y λ dependen del derivado | `ε_A(λ)`, `ε_B(λ)` 250–1700 nm; Φ_ciclación/Φ_apertura(λ); `Δn(λ,c)`; fatiga; (T) |
| M2 | **Azobencenos** (tipo T, retorno térmico) | Azobenceno; 4-(dimethylamino)azobenceno; azobencenos "push-pull" o heteroarílicos (p. ej. arilazopirazoles) para ajustar vida media | trans: banda π–π* intensa (≈320–380 nm, desplazable) y n–π* débil (≈440 nm) | cis: π–π* reducida/desplazada (≈280–320 nm) y n–π* más intensa (≈430–450 nm) | Gran catálogo, síntesis accesible, cambios geométricos/índice, sintonizable por sustitución | Retorno térmico (vida media sensible a T/sustituyente/matriz), posible menor retención; linealidad y Δn dependen del sistema | `ε_trans(λ)`, `ε_cis(λ)`; Φ_t→c, Φ_c→t(λ); `t1/2(T)` y Ea; `Δn(λ,c)` en matriz; fotoestacionario |
| M3 | **Espiropirano / Merocianina (SP/MC)** | 1',3',3'-trimethyl-6-nitrospiro[chromene-2,2'-indoline] (6-nitroBIPS); derivados con sustituyentes para estabilidad espectral | SP (cerrado): UV (≈260–380 nm), casi incoloro en visible | MC (abierto, zwitterión): visible intenso (≈500–620 nm, muy dependiente de polaridad) | Gran contraste espectral entre conformeros, `Δn`/polaridad altos potenciales | Retorno térmico MC→SP (dependiente de T/matriz), fatiga/solvatocromismo, acumulación de subestados | `ε_SP(λ)`, `ε_MC(λ)` (y conformeros MC si aplica); `t1/2(T)`, Ea; Φ; `Δn(λ,c)`; efecto de matriz |
| M4 | **DASA** (Donor–Acceptor Stenhouse Adducts) | DASA de 1ª/2ª/3ª generación (p. ej. basados en Meldrum/barbitúrico e indolina/anilina; derivados recientes de mayor estabilidad) | Forma coloreada extendida (trieno): visible/NIR cercano (≈450–700 nm según generación) | Forma ciclada/incolora: UV/violeta (≈300–360 nm), bleached en visible | Activación en visible, alto contraste visible, separación potencial respecto a UV-switches | Fuerte dependencia de solvente/matriz y T, retorno térmico, generaciones tempranas con fatiga; requiere selección cuidadosa | `ε_coloreada(λ)`, `ε_ciclada(λ)`; `t1/2(T)`, Ea; Φ(λ); estabilidad en película sólida; `Δn` si disponible |
| M5 | **Fulgidas / Fulgimidas** (tipo P) | Aberchrome 670 (fulgida clásica); fulgimidas N-sustituidas (mejor estabilidad/fatiga) | Forma abierta (E/Z): UV (≈300–400 nm) | Forma cerrada (C): visible (≈450–550 nm) | Térmicamente estables en muchas variantes, buena fatiga (fulgimidas), alternativa sólida a DAE | Solapamiento en UV posible, rendimientos cuánticos variables; disponibilidad comercial según derivado | `ε_E/Z(λ)`, `ε_C(λ)`; Φ; `Δn(λ,c)`; estabilidad térmica/fotoquímica |
| M6 | **Dihidropirenos (DHP) / Ciclofano-dienos (CPD)** (negativo) | Derivados de dihidropireno (p. ej. DHP sustituido) | DHP (coloreado): visible amplio (≈400–700 nm) | CPD (incoloro): UV (≈280–350 nm) | Grandes cambios de conjugación/espectro, algunos con buena estabilidad térmica | Síntesis más especializada, cinética/Φ dependientes de sustitución | `ε_DHP(λ)`, `ε_CPD(λ)`; Φ; `t1/2(T)`; `Δn` |
| M7 | **Oxazinas / Oxazolidinas** foto/termo-crómicas | Oxazinas espiro (p. ej. nitrospiropirano-oxazina) y sistemas indolino-oxazina | Cerrado: UV (≈300–380 nm) | Abierto coloreado: visible (≈550–650 nm), a menudo con retorno rápido | Conmutación rápida, contraste visible | Frecuente retorno térmico rápido (retención corta), fatiga en algunos sistemas | `ε_cerrado(λ)`, `ε_abierto(λ)`; `t1/2(T)` muy relevante; Φ |
| M8 | **Naftopiranos / Cromen os** | 3H-naftopiranos (familia de lentes fotocromáticas), derivados con distintos λ | Cerrado: UV (≈320–380 nm) | Abierto (merocianinas): visible (≈420–620 nm, a veces múltiples isómeros) | Comercialmente disponibles, buena respuesta a UV | Múltiples isómeros abiertos con cinéticas distintas, retorno térmico, solapamiento | `ε_cerrado(λ)`, `ε_abiertos(λ)`; cinética multi-componente `t1/2(T)`; Φ |
| M9 | **Estilbenos / Indigos / Hemitioindigos / Heteroaril-etenos** (según caso) | Estilbeno, stiff-stilbene, hemithioindigo (HTI) | trans/E: UV (≈280–340 nm típico) | cis/Z: UV desplazado (≈240–300 nm, menor ε) | HTI y derivados modernos mejoran en visible/estabilidad | Estilbeno simple: solapamiento y fotoquímica secundaria; HTI más prometedor pero requiere selección | Espectros E/Z, Φ, `t1/2(T)`, `Δn` en matriz |

## 2. Criterios de selección para un set de 4 (ortogonalidad práctica)

- **Separación espectral:** maximizar distancia entre bandas de **escritura** de cada material y entre escritura/borrado, minimizando solapamiento de colas en las λ de los demás (evaluar con `A(λ)=l Σ ε_{i,s}C_{i,s}`).
- **Lectura no destructiva:** elegir λ de lectura en región de baja `ε` para todos los estados/conformeros presentes (NIR/telecom suele ayudar, p. ej. 850/980/1310/1550 nm, si los materiales no absorben ahí).
- **Retención:** preferir al menos 1–2 componentes tipo P (p. ej. DAE, fulgimida) para estabilidad; si se usan tipo T (azo, SP, DASA), caracterizar `t1/2(T)` y compensar.
- **Δn y linealidad:** priorizar familias con `Δn` reportado en la matriz objetivo y caracterizar `Δn(c,λ,T)` para calibración multinivel.
- **Matriz/compatibilidad:** usar la misma matriz sólida o capas compatibles; espectros y cinética cambian en solución vs película.

## 3. Ejemplo de set ortogonal (hipótesis a validar con espectros)

| Rol | Familia sugerida | Escritura (aprox.) | Borrado (aprox.) | Lectura candidata | Comentario |
|---|---|---:|---:|---:|---|
| M1 | DTE (cerrado visible específico) | ~313 nm (UV) | ~530 nm | 1550 nm | Tipo P, buena base de estabilidad |
| M2 | Azobenceno (derivado elegido) | ~365 nm | ~450 nm | 1310 nm | Verificar `t1/2(T)` |
| M3 | Espiropirano/MC | ~365–405 nm (según derivado) | ~560–590 nm | 980 nm | Ajustar para no solapar con M1/M2 |
| M4 | DASA o Fulgimida (según espectro) | ~600–660 nm | térmico/λ específica | 850 nm | Elegir por mínima cola en lecturas |

> **Importante:** este set es ilustrativo (como el usado en simulaciones). La ortogonalidad debe confirmarse con espectros reales superpuestos de ambos estados/conformeros.

## 4. Qué entregar al modelo cuando tengas los espectros
- Archivos por especie: `data/spectra/<material>_<estado>.csv` con columnas `wavelength_nm` y `alpha_per_um` (o `alpha_per_cm` / `epsilon_L_mol_cm` + concentración), ver `data/spectra/README.md`.
- Cinética y fotoquímica: `data/kinetics_template.csv` (`Φ`, `t1/2(T)`, `Ea`).
- Índice/termo-óptica: `data/refractive_index_template.csv` (`Δn(λ,c)`, `dn/dT`).
- Con eso se recalculan: selectividad Beer-Lambert, matriz `A` efectiva, no linealidad, retención térmica y márgenes (ver `spectral_data_loader.py`, `DATA_ACQUISITION_PLAN.md`).

## 5. Referencias de partida (verificar en original)
- Irie et al., *Chem. Rev.* 2014, 114, 12174 (DAE) — DOI: 10.1021/cr500249p
- Bandara & Burdette, *Chem. Soc. Rev.* 2012, 41, 1809 (azobenceno) — DOI: 10.1039/C1CS15179G
- Klajn, *Chem. Soc. Rev.* 2014, 43, 148 (espiropirano) — DOI: 10.1039/C3CS60181A
- Helmy et al., *JACS* 2014, 136, 8169 (DASA) — DOI: 10.1021/ja503016b; Lerch et al., *Chem. Soc. Rev.* 2018, 47, 1910 — DOI: 10.1039/C7CS00772H
- Yokoyama, *Chem. Rev.* 2000, 100, 1717 (fulgidas) — DOI: 10.1021/cr980070c
- Ríos et al., *Nature Photonics* 2015, 9, 725 (contexto memoria fotónica multinivel) — DOI: 10.1038/nphoton.2015.182
