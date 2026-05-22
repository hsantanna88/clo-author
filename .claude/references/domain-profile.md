# Domain Profile — Responsabilidad Civil Médica (Perú)

## Field

**Primary:** Derecho Civil Peruano — Responsabilidad Civil Médica
**Adjacent subfields:** Derecho de Daños, Bioética Jurídica, Derecho Médico Comparado, Derecho del Consumidor (protección del paciente)

---

## Target Journals (ranked by tier)

| Tier | Journals |
|------|----------|
| Objetivo | Pro Jure (Universidad César Vallejo) |
| Nacionales | Themis (PUCP), Ius et Veritas (PUCP), Derecho & Sociedad (PUCP), Gaceta Civil & Procesal Civil |
| Iberoamericanas | InDret — Revista para el Análisis del Derecho (Barcelona), Anuario de Derecho Civil (España), Revista de Derecho Privado (Colombia/España), Revista Chilena de Derecho Privado |
| Derecho médico | Revista de Derecho y Salud, Bioética & Derecho (Barcelona) |

---

## Corpus Jurisprudencial (fuentes de datos)

| Fuente | Tipo | Acceso | Notas |
|--------|------|--------|-------|
| SPIJ (Ministerio de Justicia) | Base de datos oficial | Público (web) | Casaciones CAS completas, Sala Civil Permanente y Transitoria |
| LP Pasión por el Derecho | Plataforma curada | Público (web) | Sentencias con sumillas y análisis; buena cobertura de responsabilidad médica |
| El Peruano (edición oficial) | Boletín oficial | Público (PDF) | Sentencias de Sala Plena, resoluciones plenarias vinculantes |
| Diálogos con la Jurisprudencia | Revista + base de datos | Suscripción | Sentencias comentadas con doctrina |
| PJ (Poder Judicial) | Portal institucional | Público (web) | Consulta de expedientes; acceso a segunda instancia |

**Organización del corpus:** `data/raw/corpus_index.csv`
Campos recomendados: `id_sentencia`, `tribunal`, `sala`, `fecha`, `tipo` (CAS/EXP), `resultado` (fundada/infundada/inadmisible), `tema_principal` (lex_artis/consentimiento/daño/todos), `monto_indemnizatorio`, `url`, `notas`

---

## Metodología Jurídica

| Método | Aplicación típica | Supuesto a defender |
|--------|------------------|---------------------|
| Análisis dogmático | Exégesis del CC arts. 1969, 1970, 1314, 1321, 1985; Ley 26842 (Salud) | Coherencia con el sistema de fuentes del derecho peruano |
| Análisis jurisprudencial | Identificación de criterios reiterados en la Corte Suprema (CAS) | Representatividad del corpus: sentencias en materia de responsabilidad civil médica 2010–2024 |
| Método comparado | Contraste con España (TS), Argentina (CSJN), Colombia (CSJ) | Relevancia para el sistema romano-germánico peruano |
| Análisis de contenido | Codificación de variables en el corpus (si hay componente empírico) | Operacionalización de conceptos jurídicos como variables observables |

---

## Convenciones del Campo

- Citar artículos del Código Civil por número exacto: "art. 1969 CC", "art. 1985 CC"
- Citar casaciones por número, año y sala: "CAS. 1234-2019-LIMA (Sala Civil Permanente)"
- Citar expedientes de instancias inferiores: "Exp. 5678-2018-0 (3.ª Sala Civil de Lima)"
- Siempre distinguir entre **responsabilidad contractual** (art. 1314 CC) y **extracontractual** (art. 1969 CC) médica
- Citar la *lex artis* diferenciando: *lex artis* general (estándar de la profesión médica) vs. *lex artis ad hoc* (estándar ajustado al caso concreto)
- Discutir siempre la **carga de la prueba** del daño médico (art. 1331 CC y doctrina de la carga dinámica)
- En daño moral: distinguir daño moral subjetivo vs. daño a la persona (Fernández Sessarego)
- No usar lenguaje causal sin haber establecido el nexo causal jurídico (art. 1985 CC: causa adecuada)
- Los plazos de prescripción son relevantes: art. 2001 CC (10 años contractual, 2 años extracontractual)
- Mencionar el rol del consentimiento informado como eximente de responsabilidad (Ley 29414)

---

## Referencias Seminales

### Doctrina peruana (obligatoria)

| Obra | Por qué importa |
|------|----------------|
| Espinoza Espinoza, Juan. *Derecho de la Responsabilidad Civil* (última ed.) | Tratado de referencia del sistema de responsabilidad civil peruano; define los elementos: antijuridicidad, factor de atribución, nexo causal, daño |
| De Trazegnies Granda, Fernando. *La Responsabilidad Extracontractual* (2 vols.) | Obra fundacional del derecho de daños en el Perú; interpretación del Libro VII del CC de 1984 |
| Taboada Córdova, Lizardo. *Elementos de la Responsabilidad Civil* | Análisis sistemático de los elementos; referencia para la distinción contractual/extracontractual |
| Fernández Cruz, Gastón. Artículos sobre responsabilidad médica y consentimiento informado | Desarrolla la *lex artis ad hoc* y el nexo causal en el contexto médico |
| Fernández Sessarego, Carlos. *Daño a la persona y daño moral* | Fundamento doctrinal del daño a la persona como categoría autónoma en el CC peruano |
| León Hilario, Leysser. *La responsabilidad civil. Líneas fundamentales y nuevas perspectivas* | Perspectiva comparatista; conexión con el derecho italiano; crítica del sistema peruano |

### Normativa clave

| Norma | Relevancia |
|-------|-----------|
| Código Civil (D.Leg. 295, 1984) — arts. 1314, 1321, 1969, 1970, 1985 | Marco general de responsabilidad civil |
| Ley General de Salud (Ley 26842, 1997) — arts. 15, 27, 36, 40 | Derechos del paciente, deber de información, consentimiento informado |
| Ley de Derechos de los Usuarios de los Servicios de Salud (Ley 29414, 2009) | Regula el consentimiento informado con detalle; derechos del paciente |
| Código de Ética y Deontología del CMP (2000) | Estándar de conducta médica; referencia para la *lex artis* |

### Doctrina comparada (complementaria)

| Obra | Por qué importa |
|------|----------------|
| Galán Cortés, Julio César. *Responsabilidad civil médica* (España) | Referencia ibérica; sistema similar al peruano; buena sistematización de *lex artis* |
| Lorenzetti, Ricardo Luis. *Responsabilidad civil de los médicos* (Argentina) | Sistema argentino próximo al peruano; tipología del daño médico |
| Busnelli, Francesco. *Il danno biologico* (Italia) | Origen doctrinario del daño a la persona en el civil law |

---

## Preocupaciones típicas de los árbitros/revisores

- "¿El corpus de sentencias es representativo? ¿Cuántas sentencias y de qué período?"
- "¿Se distingue claramente entre lex artis y consentimiento informado como fuentes autónomas de responsabilidad?"
- "¿Se discute la diferencia entre el régimen contractual y extracontractual en la práctica jurisprudencial?"
- "¿El análisis del nexo causal es suficiente? La causalidad médica es especialmente compleja."
- "¿Se aborda la responsabilidad del hospital (persona jurídica) vs. el médico (persona natural)?"
- "¿La propuesta de *lege ferenda* (si la hay) es compatible con el sistema del CC peruano de 1984?"

---

## Umbrales de calidad

| Elemento | Criterio | Justificación |
|----------|----------|---------------|
| Corpus mínimo | ≥ 20 sentencias de Corte Suprema | Representatividad del análisis |
| Período | 2010–2024 (post-Ley 29414) | Marco normativo vigente; corte relevante |
| Cobertura doctrinal | Doctrina nacional + ≥ 2 referencias comparadas | Estándar de revistas nacionales de primer nivel |
| Extensión del artículo | 8.000–15.000 palabras (cuerpo del texto) | Rango habitual en Themis, Pro Jure, InDret |
