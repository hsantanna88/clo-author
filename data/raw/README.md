# Corpus Jurisprudencial — Responsabilidad Civil Médica (Perú)

## Estructura de carpetas

```
data/raw/
├── corte_suprema/          # Casaciones (CAS.) — Sala Civil Permanente y Transitoria
├── cortes_superiores/      # Sentencias de segunda instancia (Exp.)
├── primera_instancia/      # Sentencias de primera instancia de especial relevancia
└── corpus_index.csv        # Ficha maestra del corpus
```

## Fuentes recomendadas

| Fuente | Tipo de sentencia | Acceso | URL |
|--------|------------------|--------|-----|
| SPIJ (Ministerio de Justicia) | Casaciones CAS. completas | Gratuito | https://spij.minjus.gob.pe |
| LP Pasión por el Derecho | Sentencias curadas con sumillas | Gratuito (parcial) | https://lpderecho.pe |
| Portal del Poder Judicial | Consulta de expedientes | Gratuito | https://cej.pj.gob.pe |
| El Peruano (edición oficial) | Resoluciones plenarias vinculantes | Gratuito | https://elperuano.pe |
| Diálogos con la Jurisprudencia | Sentencias comentadas | Suscripción | — |

## Formato de los archivos

- **Preferido:** PDF original de la sentencia (descargado de SPIJ o el PJ)
- **Alternativo:** TXT extraído del PDF si se requiere análisis de texto
- **Nombre del archivo:** `CAS_1234-2019-LIMA.pdf` o `EXP_5678-2018-LIMA-3SC.pdf`

## Ficha maestra: `corpus_index.csv`

Columnas recomendadas:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `id` | Identificador interno | `001` |
| `tipo` | Tipo de resolución | `CAS` / `EXP` |
| `numero` | Número y año | `1234-2019` |
| `sala` | Sala o juzgado | `Sala Civil Permanente CS` |
| `ciudad` | Distrito judicial | `LIMA` |
| `fecha` | Fecha de la resolución (AAAA-MM-DD) | `2019-08-15` |
| `resultado` | Resultado para el demandante | `fundada` / `infundada` / `inadmisible` |
| `tema_lex_artis` | ¿Discute lex artis? | `sí` / `no` |
| `tema_consentimiento` | ¿Discute consentimiento informado? | `sí` / `no` |
| `tema_dano` | ¿Discute tipo/cuantía del daño? | `sí` / `no` |
| `tipo_dano` | Tipos de daño reconocidos | `daño moral; lucro cesante` |
| `monto_sol` | Monto indemnizatorio en soles (0 si no aplica) | `50000` |
| `nexo_causal_discutido` | ¿El fallo analiza el nexo causal? | `sí` / `no` |
| `regimen` | Régimen aplicado | `contractual` / `extracontractual` / `mixto` |
| `archivo` | Nombre del archivo PDF | `CAS_1234-2019-LIMA.pdf` |
| `url` | URL de consulta | `https://spij.minjus.gob.pe/...` |
| `notas` | Observaciones relevantes | `Primer precedente sobre pérdida de chance` |

## Criterios de selección del corpus

- **Período:** 2010–2024 (post-Ley 29414 de Derechos del Paciente)
- **Materias:** responsabilidad civil médica, mala praxis, consentimiento informado, negligencia médica
- **Tribunales:** Corte Suprema (prioridad) + Cortes Superiores de Lima, Arequipa, La Libertad
- **Mínimo recomendado:** 20 sentencias de Corte Suprema + sentencias complementarias de instancias inferiores
- **Exclusiones:** casos de responsabilidad administrativa o penal (a menos que incluyan pronunciamiento civil)

## Notas sobre derechos de autor

Las sentencias judiciales son actos del Estado peruano y tienen carácter público.
Su reproducción parcial con fines de investigación académica está permitida.
Citar siempre la fuente oficial (SPIJ o El Peruano).
