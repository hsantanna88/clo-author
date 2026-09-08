# Datos crudos — corridas del TCLab

**Estos archivos no se editan nunca** (INV-26). Son la evidencia experimental de la tesis.
Toda transformación produce un archivo nuevo en `data/cleaned/` mediante un script versionado.

## Nomenclatura

```
AAAA-MM-DD_HHMMSS_<experimento>_<variante>.csv
AAAA-MM-DD_HHMMSS_<experimento>_<variante>_meta.json
```

Ejemplos:

```
2026-09-15_143022_escalon_Q1-50.csv
2026-09-15_143022_escalon_Q1-50_meta.json
2026-09-20_091500_evaluacion_lqr_rep3.csv
2026-10-02_170411_evaluacion_rl-sac_semilla2.csv
```

El campo `<experimento>` identifica el protocolo (`escalon`, `prbs`, `evaluacion`, `validacion`).
El campo `<variante>` identifica la configuración concreta (amplitud, controlador, repetición,
semilla).

## Esquema del CSV

| Columna | Unidad | Descripción |
|---------|--------|-------------|
| `t_s` | s | Instante **real** de la muestra, medido, no el nominal `k*Ts` |
| `T1_C` | °C | Temperatura del sensor 1 |
| `T2_C` | °C | Temperatura del sensor 2 |
| `Q1_pct` | % | Potencia aplicada al calentador 1 |
| `Q2_pct` | % | Potencia aplicada al calentador 2 |
| `SP1_C` | °C | Referencia para el lazo 1 |
| `SP2_C` | °C | Referencia para el lazo 2 |

En corridas de lazo abierto, las columnas de referencia van vacías.

## Esquema de los metadatos (INV-22)

```json
{
  "ts_s": 1.0,
  "ambiente_inicial_C": 23.4,
  "placa": "TCLAB-01",
  "git_hash": "a1b2c3d",
  "semilla": 0,
  "modo": "hardware",
  "script": "scripts/python/identification/ensayo_escalon.py",
  "config": "config/planta.yaml",
  "desbordes_periodo": 0,
  "duracion_real_s": 1200.3,
  "notas": "Ventana cerrada, sin corrientes de aire"
}
```

Sin metadatos, una corrida no es utilizable como evidencia: no se sabe en qué condiciones se tomó.

## Antes de cada corrida

1. Verificar que la placa esté a temperatura ambiente (`enfriamiento_previo_s` en `config/planta.yaml`)
2. Registrar la temperatura ambiente inicial
3. Confirmar que el script apaga los calentadores en `finally` (INV-20)
4. Confirmar que el repositorio está limpio, para que el hash de git identifique el código ejecutado
