# Memoria del proyecto

Hechos aprendidos y correcciones que persisten entre sesiones.
Cuando se corrija un error, agrega una entrada `[LEARN:categoría]` abajo.

---

## Entorno

[LEARN:entorno] El intérprete del sistema es Python 3.14, demasiado nuevo para `torch` y
`stable-baselines3` (sin ruedas precompiladas). El entorno del proyecto vive en `.venv/` sobre
Python 3.12. Nunca instalar dependencias del proyecto en el intérprete del sistema.

[LEARN:entorno] TeX Live y MATLAB no están instalados en esta máquina. Antes de prometer que la
tesis "compila", verificar que `latexmk` exista. Si falta, decirlo en lugar de asumir.

## Plataforma

[LEARN:hardware] TCLab es hardware físico: los calentadores siguen encendidos si el script muere
por excepción. Toda sesión con la placa usa gestor de contexto y apaga `Q1`/`Q2` en `finally`
(INV-23). Esto no es una preferencia de estilo, es seguridad del equipo.

[LEARN:hardware] TCLab es un sistema lento: constantes de tiempo de minutos. Un experimento de
identificación o una evaluación de política toman tiempo real; no se pueden acelerar en la placa.
El entrenamiento de RL ocurre en simulación por esta razón.

## Método

[LEARN:alcance] La pregunta de investigación NO está definida. La combinación LQR+RL (residual,
auto-tuning de Q/R, filtro de seguridad, o comparación) se decide en `/discover interview`.
Ningún agente debe suponer un método concreto antes de esa entrevista.

## Interoperación

[LEARN:codigo] MATLAB y Python intercambian datos por archivo (`.mat`/`.csv`), nunca por copiar y
pegar valores. Los resultados que entran a la tesis deben ser trazables hasta la línea del script
que los generó (INV-22).

## Plantilla de origen

[LEARN:meta] Este repo es un fork de clo-author, plantilla de economía empírica. Lo adaptado vive
en `.claude/references/` y `.claude/rules/`; lo original está archivado en `.template-reference/`
(ignorado por git). Si un agente empieza a hablar de DiD, variables instrumentales o códigos JEL,
quedó vocabulario de economía sin adaptar — corregirlo en el archivo de reglas, no en la salida.
