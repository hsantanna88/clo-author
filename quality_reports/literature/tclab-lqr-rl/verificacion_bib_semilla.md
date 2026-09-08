# Verificación de los campos `% VERIFICAR` de `Bibliography_base.bib`

**Proyecto:** tclab-lqr-rl · **Fecha:** 2026-09-07 · **Revisado:** 2026-09-08 (ronda 1)
**Agente:** librarian
**Archivo auditado:** `/home/limerence/Documents/tesis-modalidad/Bibliography_base.bib` (19 entradas)

---

## 0. Cómo leer esta auditoría

`Bibliography_base.bib` contiene **8 comentarios `% VERIFICAR`** que cubren **13 campos
individuales** (la marca de `Park2020_tclab` cubre cuatro campos por sí sola). Los audito campo a
campo, no comentario a comentario.

### Escala de estado

| Estado | Significado |
|--------|-------------|
| **CONFIRMADO** | Verificado contra Crossref o contra la página oficial de actas/editor, **efectivamente abierta**. Alta confianza. |
| **CONFIRMADO (fuentes secundarias)** | Varias fuentes independientes coinciden, pero no consulté un registro editorial autoritativo. Confianza media-alta. |
| **NO CONFIRMADO** | No hallé fuente que lo respalde, o la fuente disponible no es suficiente. |
| **CORREGIDO** | El dato de la semilla era incorrecto o incompleto; se indica el correcto. |

### Fuentes consultadas efectivamente

- `api.crossref.org` — API de Crossref, consultada directamente por DOI y por consulta bibliográfica.
- `api.openalex.org` — API de OpenAlex, para el encadenamiento de citas *(ronda 1)*.
- `ojs.aaai.org` — páginas oficiales de actas AAAI.
- `arxiv.org/abs/...` — páginas de resumen de arXiv.
- Catálogos de librería y fichas bibliográficas secundarias (para los libros, que no están en
  Crossref).

**Criterio de grado de evidencia (endurecido en la ronda 1):** una página que *aparece* en los
resultados de una búsqueda **no cuenta como consultada**. Solo cuenta abrirla. Las entradas cuyos
campos provienen de síntesis de resultados llevan `% UNVERIFIED` en `references.bib`, aunque el dato
probablemente sea correcto.

---

## 1. Tabla resumen

| # | Entrada | Campo marcado | Estado | Dato confirmado |
|---|---------|---------------|--------|-----------------|
| 1 | `Kalman1960_contributions` | páginas exactas | **CONFIRMADO (fuentes secundarias)** | 102–119 |
| 2 | `Bertsekas_dynamic_programming` | edición | **CONFIRMADO** | 4.ª edición |
| 3 | `Bertsekas_dynamic_programming` | año | **CONFIRMADO con salvedad crítica** | 2017 **solo si es el Vol. I**; el Vol. II 4.ª ed. es 2012 |
| 4 | `Ogata_control_moderna` | año de la edición en español | **CONFIRMADO (fuentes secundarias)** | 2010 |
| 5 | `Bradtke1994_adaptive_lq` | volumen | **CONFIRMADO** | vol. 3 |
| 6 | `Bradtke1994_adaptive_lq` | páginas | **CONFIRMADO** | 3475–3479 |
| 7 | `Dean2020_sample_complexity_lqr` | páginas | **CONFIRMADO** | 633–679 (+ issue 4, que faltaba) |
| 8 | `Recht2019_tour_rl` | páginas | **CONFIRMADO** | 253–279 (+ issue 1, que faltaba) |
| 9 | `Johannink2019_residual_rl` | lista completa de autores | **CONFIRMADO** | Los 9 autores de la semilla son correctos y están en el orden correcto |
| 10 | `Park2020_tclab` | autores | **CONFIRMADO** | Park, Martin, Kelly, Hedengren — correctos |
| 11 | `Park2020_tclab` | volumen | **CONFIRMADO** | 135 |
| 12 | `Park2020_tclab` | número de artículo | **CONFIRMADO** | 106736 |
| 13 | `Park2020_tclab` | páginas | **RESUELTO — NO APLICA** | No existe rango de páginas: 106736 es número de artículo |

**Balance: 12 campos confirmados, 1 resuelto por inaplicabilidad, 0 no confirmados.**
**Salvedad crítica pendiente:** el volumen de Bertsekas (ver §2.2).

---

## 2. Detalle por entrada

### 2.1 `Kalman1960_contributions` — páginas exactas

**Marca original:** `pages = {102--119}, % VERIFICAR paginas exactas`

**Estado: CONFIRMADO (fuentes secundarias convergentes).**

La referencia *Bol. Soc. Mat. Mexicana*, vol. 5, pp. 102–119, 1960 aparece de forma consistente en
tres fuentes independientes: un registro de búsqueda de Google Scholar con los campos
`publication_year=1960`, `journal=Bol. Soc. Mat. Mexicana`, `pages=102-119`; el capítulo comentado
de M. Raginsky en *The State-Space Revolution in the Study of Complex Systems* (SFI Press), dedicado
precisamente a este artículo; y varias listas de lectura académicas.

**No consulté el original ni un registro editorial autoritativo.** El *Boletín de la Sociedad
Matemática Mexicana* de 1960 no está indexado en Crossref, así que no hay forma de elevar esto a
CONFIRMADO pleno sin acceso al fondo físico o a un facsímil.

**Corrección menor adicional (no marcada en la semilla):** el título se registra en minúsculas —
*"Contributions to the theory of optimal control"* — en todas las fuentes que vi. La entrada
semilla lo capitaliza. Es una diferencia de estilo, no un error, pero conviene homogeneizar.

**AVISO AÑADIDO EN LA RONDA 1 — riesgo de confusión.** `references.bib` contiene ahora **dos obras
de Kalman fechadas en 1960**:

- `Kalman1960_contributions` → el artículo del **LQR** (*Bol. Soc. Mat. Mexicana* 5:102–119)
- `Kalman1960_filter` → el artículo del **filtro de Kalman** (*J. Basic Engineering* 82(1):35–45,
  DOI 10.1115/1.3662552), añadido en la ronda 1 como parte de la cobertura de LQG/observador

**Son obras distintas.** `biblatex` las desambiguará como "1960a" y "1960b". **No fusionarlas ni
borrar una creyendo que es un duplicado.** El aviso está también en `references.bib`, apartado D-bis
de la sección de reconciliación.

---

### 2.2 `Bertsekas_dynamic_programming` — edición y año

**Marca original:** `year = {2017}, % VERIFICAR edicion y anio de la que se consulte`

**Estado: CONFIRMADO, pero con una salvedad que la marca original no anticipaba.**

Confirmado: existe una **4.ª edición del Volumen I**, Athena Scientific, **2017**, ISBN
9781886529434. Verificado en varios catálogos de librería coincidentes (AbeBooks/Biblio, Amazon) y
en la página de MIT de Bertsekas (`web.mit.edu/dimitrib/www/DP1_Short_View.pdf`, titulada
"Dynamic Programming and Optimal Control Volume I FOURTH EDITION").

**La salvedad crítica: la entrada semilla no declara volumen, y esto sí es un problema.**

- **Vol. I**, 4.ª edición → **2017**
- **Vol. II**, 4.ª edición → **2012**

El contenido relevante para el puente LQR ↔ RL —programación dinámica aproximada, iteración de
políticas aproximada— está en el **Volumen II**, no en el I. Si la tesis cita a Bertsekas para
sustentar la conexión DP–RL, muy probablemente el volumen correcto es el II y **el año correcto
es 2012, no 2017**.

**Acción requerida:** el estudiante debe determinar qué volumen va a consultar y ajustar
`volume` y `year` en consecuencia.

**Ruido detectado en las fuentes:** uno de los catálogos consultados titulaba el Vol. I como
*"Vol 1: Approximate Dynamic Programming"*. Eso es un error del catálogo — "Approximate Dynamic
Programming" es el subtítulo del **Vol. II**. No usar ese catálogo como fuente.

---

### 2.3 `Ogata_control_moderna` — año de la edición en español

**Marca original:** `year = {2010} % VERIFICAR anio de la edicion en espanol`

**Estado: CONFIRMADO (fuentes secundarias).**

*Ingeniería de Control Moderna*, 5.ª edición, **Pearson Educación, Madrid, 2010**,
ISBN **9788483226605**. Traducción de Sebastián Dormido Canto y Raquel Dormido Canto.

Fuentes coincidentes: ficha de catálogo AbeBooks (registro de ejemplar nuevo, editorial Pearson,
2010) y ficha bibliográfica de SciEPub que cita literalmente *"Ogata, K. 2010. Ingeniería de
Control Moderna, 5ta Edición. Pearson Educación S.A. Madrid."*

**No consulté el catálogo del editor directamente.** Añadí `address = {Madrid}`, `publisher` e
`isbn` en `references.bib`, campos que la semilla no tenía.

---

### 2.4 `Bradtke1994_adaptive_lq` — volumen y páginas

**Marca original:** `year = {1994} % VERIFICAR volumen y paginas`

**Estado: CONFIRMADO (Crossref).**

- Autores: S. J. Bradtke, B. E. Ydstie, A. G. Barto — **coinciden con la semilla**
- Actas: *Proceedings of 1994 American Control Conference — ACC '94*
- **Volumen: 3** · **Páginas: 3475–3479** · Año: 1994
- **DOI: 10.1109/ACC.1994.735224** (la semilla no lo tenía)

También se confirma el título en minúsculas.

---

### 2.5 `Dean2020_sample_complexity_lqr` — páginas

**Marca original:** `pages = {633--679}, % VERIFICAR paginas`

**Estado: CONFIRMADO (Crossref, consulta directa por DOI).**

- Autores: Sarah Dean, Horia Mania, Nikolai Matni, Benjamin Recht, Stephen Tu — **coinciden**
- Revista: *Foundations of Computational Mathematics* · Volumen: 20 · **Número: 4** ← *faltaba*
- **Páginas: 633–679** ← **el dato de la semilla era correcto**
- DOI: 10.1007/s10208-019-09426-y ← *faltaba en la semilla*

---

### 2.6 `Recht2019_tour_rl` — páginas

**Marca original:** `pages = {253--279}, % VERIFICAR paginas`

**Estado: CONFIRMADO (Crossref, consulta directa por DOI).**

- Volumen: 2 · **Número: 1** ← *faltaba* · **Páginas: 253–279** ← **correcto en la semilla**
- DOI: 10.1146/annurev-control-053018-023825 ← *faltaba*

---

### 2.7 `Johannink2019_residual_rl` — lista completa de autores

**Marca original:** `year = {2019} % VERIFICAR lista completa de autores`

**Estado: CONFIRMADO (Crossref). La lista de la semilla era correcta y está completa.**

Crossref devolvió los nueve autores en este orden: Tobias Johannink, Shikhar Bahl, Ashvin Nair,
Jianlan Luo, Avinash Kumar, Matthias Loskyll, Juan Aparicio Ojea, Eugen Solowjow, Sergey Levine.
Coinciden uno a uno con `Bibliography_base.bib`.

**Datos adicionales que la semilla no tenía:** actas *2019 ICRA*, **páginas 6023–6029**,
**DOI 10.1109/ICRA.2019.8794127**.

---

### 2.8 `Park2020_tclab` — autores, volumen, número de artículo y páginas

**Marca original:**
```
% VERIFICAR: autores, volumen, numero de articulo y paginas. Entrada
% reconstruida de memoria; confirmar contra la publicacion antes de citar.
```

**Estado: CONFIRMADO íntegramente (Crossref, consulta directa por DOI).**

Esta era la marca más grave —entrada reconstruida de memoria— y es también la entrada más
importante del archivo, porque define la plataforma de estudio. La verificación es limpia.

| Campo | Semilla | Crossref | Veredicto |
|-------|---------|----------|-----------|
| Autores | Park, Martin, Kelly, Hedengren | Junho Park, R. Abraham Martin, Jeffrey D. Kelly, John D. Hedengren | **CORRECTOS**, mismo orden |
| Título | *Benchmark Temperature Microcontroller…* | *Benchmark temperature microcontroller…* | Correcto (capitalización distinta) |
| Revista | *Computers & Chemical Engineering* | ídem | **CORRECTA** |
| Volumen | 135 | 135 | **CORRECTO** |
| Año | 2020 | 2020 (abril) | **CORRECTO** |
| Nº de artículo | — (faltaba) | **106736** | **AÑADIDO** |
| Páginas | — (marcado a verificar) | no aplica | **RESUELTO**: 106736 es número de artículo |
| DOI | — (faltaba) | 10.1016/j.compchemeng.2020.106736 | **AÑADIDO** |

**Conclusión: la reconstrucción de memoria era correcta en todos los campos que declaraba.**

**Nota de nomenclatura:** en `references.bib` esta entrada se reetiquetó como
`Park2020_tclab_benchmark` para distinguirla de `Park2025_rl_process_control_review` (Joonsoo
Park, otro autor, otra revista).

**Añadido en la ronda 1:** esta entrada fue además la **semilla del encadenamiento de citas**. Su
identificador OpenAlex es **W2998862960**, con **84 obras citantes**, todas revisadas por título.
Ninguna menciona LQR. Ver `frontier_map.md` §5.4.

---

## 3. Hallazgos sobre entradas NO marcadas

Verifiqué también las entradas sin marca `% VERIFICAR` que aparecen en la búsqueda. Ninguna
contiene errores, pero **cinco están incompletas** de forma que puede dar problemas al compilar
o al pasar el control de estilo de la tesis.

| Entrada | Hallazgo | Acción sugerida |
|---------|----------|-----------------|
| `Haarnoja2018_sac` | Falta serie, volumen y páginas. Datos: PMLR, vol. 80, pp. 1861–1870. **RONDA 1: degradada a `% UNVERIFIED`.** La página oficial de PMLR apareció en los resultados pero **no se abrió**, que es el mismo grado de evidencia que en Fazel y Tu-Recht, ambas ya degradadas. Se corrige por coherencia. | Completar, con la marca |
| `Fazel2018_policy_gradient_lqr` | Falta serie, volumen y páginas. Datos: PMLR, vol. 80, pp. 1467–1476. Marca `% UNVERIFIED` (evidencia SERP). | Completar, con la marca |
| `Lillicrap2016_ddpg` | Sede ICLR 2016, San Juan, Puerto Rico; arXiv:1509.02971. Marca `% UNVERIFIED` (evidencia SERP, fuente no nombrada). | Añadir `address` y `note`, con la marca |
| `Berkenkamp2017_safe_rl` | Sede correcta (NeurIPS 2017). El rango 908–919 circula en fuentes secundarias pero **no lo confirmé**. | Dejar sin páginas (convención de NeurIPS) |
| `Silver2018_residual_policy` | Correcta como preprint. Segundo nombre de la segunda autora: **Kelsey R. Allen** (con inicial). Confirmé que **no existe versión publicada revisada por pares**. Marca `% PUBLICACION_NO_COMPROBADA`: **citable.** | Añadir la inicial |
| `Schulman2017_ppo` | Correcta. PPO nunca se publicó en actas; el preprint arXiv **es** la cita canónica. | Ninguna |
| `AstromMurray2008_feedback_systems` | Correcta para la 1.ª edición. **Advertencia:** existe una 2.ª edición (2021) sustancialmente ampliada. | Decidir qué edición se consulta |
| `Ljung1999_system_identification` | Correcta (2.ª ed., 1999). | Ninguna |
| `SuttonBarto2018_rl` | Correcta (2.ª ed., 2018, MIT Press). | Ninguna |
| `AndersonMoore1990_optimal_control` | No la verifiqué contra ninguna fuente en esta búsqueda. | **Verificar antes de citar** |
| `AstromHagglund2006_advanced_pid` | No la verifiqué contra ninguna fuente en esta búsqueda. | **Verificar antes de citar** |

---

## 4. Lo que queda pendiente

1. **Decidir el volumen de Bertsekas** (I o II) y ajustar el año en consecuencia. Es el único
   campo con riesgo de error real que queda abierto. Ver §2.2.
2. **Verificar `AndersonMoore1990_optimal_control` y `AstromHagglund2006_advanced_pid`.** No están
   marcadas con `% VERIFICAR`, pero tampoco las comprobé; el hecho de no estar marcadas no
   significa que estén verificadas.
3. **Decidir la edición de Åström y Murray** (2008 vs 2021).
4. **Confirmar el rango de páginas de Berkenkamp et al. (2017)** o —preferible— omitirlo.
5. **Abrir las páginas de PMLR y NeurIPS Proceedings** para elevar de `% UNVERIFIED` a confirmadas
   las cuatro entradas de actas de ML: Fazel, Tu y Recht, Haarnoja, Mania. *(Ronda 1.)*
6. **Completar el campo `author`** de `East2020_infinite_horizon_diff_mpc` contra `openreview.net`,
   o eliminar la entrada. Está deliberadamente sin autores. *(Ronda 1.)*
7. **No fusionar las dos entradas de Kalman de 1960.** Ver el aviso en §2.1. *(Ronda 1.)*
8. **Homogeneizar la capitalización de títulos** en todo el archivo. Ahora hay una mezcla de
   *Title Case* y minúsculas. Cualquiera de las dos es aceptable; la inconsistencia no.

---

## 5. Declaración de método

- Toda verificación marcada **CONFIRMADO** se hizo consultando efectivamente `api.crossref.org`
  o la página oficial correspondiente durante esta sesión.
- Toda verificación marcada **CONFIRMADO (fuentes secundarias)** se apoya en dos o más fuentes
  independientes coincidentes, sin registro editorial autoritativo. Se indica en cada caso.
- **No completé ningún campo de memoria.** Donde no hubo fuente, el estado es
  **NO CONFIRMADO** o el campo se omitió.
- Los libros (y el artículo de Kalman de 1960 en revista mexicana) no están indexados en Crossref;
  por eso su nivel de confianza es estructuralmente menor que el de los artículos.
- **Ronda 1:** el criterio de "fuente consultada" se endureció. Aparecer en una página de
  resultados de búsqueda ya no cuenta; solo cuenta abrir la página. Seis entradas se degradaron a
  `% UNVERIFIED` por este criterio (cinco por el coordinador, más `Haarnoja2018_sac` por
  coherencia). **Ninguna de esas degradaciones significa que el dato sea incorrecto:** significa que
  no está confirmado al estándar que este proyecto se impuso.
