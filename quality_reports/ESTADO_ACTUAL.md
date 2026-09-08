# Estado al 2026-09-08 10:15 — leer esto primero al retomar

## Dónde quedó todo

**Rama:** `config/adaptacion-control` — 3 commits locales, **sin subir a GitHub**.

| Commit | Contenido |
|---|---|
| `e9e76d6` | Adaptación de la plantilla clo-author (economía) a control automático |
| `666d3cc` | Revisión de literatura ronda 1 + informes críticos de rondas 0 y 1 |
| `547a79f` | `references.bib` parcial de la ronda 2 |

## AVISO: los archivos de literatura están en estado MIXTO

El agente de la ronda 2 murió por límite de la API justo después de reescribir
`references.bib` y antes de tocar los demás. Por tanto:

| Archivo | Estado |
|---|---|
| `references.bib` | **ronda 2** (parcial: entradas nuevas + taxonomía de marcas unificada) |
| `annotated_bibliography.md` | ronda 1 |
| `frontier_map.md` | ronda 1 |
| `positioning.md` | ronda 1 |
| `verificacion_bib_semilla.md` | ronda 1 |

**Consecuencia:** puede haber entradas en `references.bib` que la bibliografía
anotada no describe, y niveles de lectura declarados en un archivo y no en otro.
No confíes en la coherencia entre archivos hasta terminar la ronda 2.

## Qué falta de la ronda 2 (informe: `literature/tclab-lqr-rl/critic_report_ronda2.md`)

Puntaje vigente: **73/100**, umbral 80. Es la ronda 3 de 3; si no pasa, escala al usuario.

1. **Consistencia de proximidad (C6, C7)** — no requiere buscar nada, es lo que más recupera.
   La tabla §11 declara "el escalar general es el mínimo del vector" y lo incumple en 4 de 13
   filas: Holt y Armellin, Alqithami, Zhang y Fernandez tienen mínimo 1 y escalar declarado 2.
   Luego hacer consistente la fila "Riesgo de solapamiento" de `positioning.md` §5, que hoy
   califica (a) como Bajo cuando la §11 le da tres competidores de proximidad 1.
2. **Disciplina de nivel para `[SERP]` (C8, C9, C10, C11)** — regla equivalente a la de `[META]`;
   hedge a Perkins y Barto en §3 y en la tabla §5; degradar o abrir Gros y Zanon y
   Wabersich–Zeilinger; retirar "demuestra formalmente" de `frontier_map.md` §2; ampliar la
   marca en Lin2024 e Ishihara2023; unificar la taxonomía de marcas.
3. **Vacíos de cobertura (C1, C2)** — identificación de sistemas (Van Overschee y De Moor 1996;
   una referencia de diseño PRBS) y declararlo en la tabla §12; rama ADP / RL inverso del eje (b)
   (Jiang y Jiang 2012; Vrabie y Lewis 2009; Ng y Russell 2000).
4. **CMDP (C3)** — Achiam et al. (2017) en `positioning.md` §6 como alternativa, no como
   componente del eje (c).
5. **Barrido que falta (C13)** — OpenAlex `title_and_abstract.search` sobre
   `"TCLab" OR "temperature control lab"`, y declarar que el cribado por título produce falsos
   negativos.

**NO añadir entradas para compensar el hallazgo C4** (70 entradas, cero textos completos): eso
agrava el problema. Lo resuelve el estudiante consiguiendo cuatro artículos por la biblioteca.

## Acciones que solo puede hacer el usuario

1. **Subir la rama a GitHub.** El remoto es HTTPS y la máquina no tiene credenciales.
   Ruta más corta en CachyOS/Arch:
   ```
   sudo pacman -S github-cli
   gh auth login
   gh auth setup-git
   git push -u origin config/adaptacion-control
   ```
   Alternativa con SSH: `ssh-keygen -t ed25519 -C "lmvm.zzz@gmail.com"`, añadir
   `~/.ssh/id_ed25519.pub` en github.com/settings/keys, y luego
   `git remote set-url origin git@github.com:luviuche/tesis-modalidad.git`

2. **Conseguir por la biblioteca de la Universidad Distrital los cuatro artículos decisivos:**
   - Patel (2023), *Computers & Chemical Engineering* 174:108232
   - Soza Mamani y Prado Romo (2025), *Processes* 13(6):1627
   - Zhang et al. (2026), *Mathematics* 14(5):895
   - Lawrence et al. (2022), *Control Engineering Practice*

   El crítico señala que leer estos cuatro a fondo informa la elección de eje mejor que
   veinte entradas bibliográficas más, y que ninguna ronda de corrección lo sustituye.

3. **Instalar el entorno** (requiere sudo):
   ```
   sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra \
                  texlive-bibtexextra texlive-fontsrecommended texlive-mathscience \
                  texlive-langspanish texlive-binextra biber python312
   python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```

4. **Decidir el volumen de Bertsekas.** La entrada semilla dice 2017 sin declarar volumen, pero
   la 4.ª ed. del Vol. II es 2012 y es el volumen con la programación dinámica aproximada,
   que es para lo que la tesis lo citará. Ver `references.bib`, sección de reconciliación.

5. **Fusionar `references.bib` con `Bibliography_base.bib`.** Hay 6 colisiones exactas de clave
   y 7 obras duplicadas. El procedimiento de siete pasos está al final de `references.bib`.

## El siguiente paso del proyecto, cuando la literatura cierre

```
/discover interview control de temperatura TCLab con LQR y aprendizaje por refuerzo
```

La pregunta de investigación **sigue sin definir**, y eso es correcto: la búsqueda de literatura
existía para informar esa decisión, no para cerrarla. El mapa de los cuatro ejes está en
`literature/tclab-lqr-rl/positioning.md` §5 y en `frontier_map.md` §12 — esas dos tablas cargan
casi todo el peso decisorio; el resto es respaldo.
