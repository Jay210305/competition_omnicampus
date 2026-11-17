# CLI & Execution Contract

## 1. CLI de Ejecución del Pipeline

El pipeline puede ser ejecutado de forma modular o completa a través de comandos deterministas en Python.

### 1.1 Comando Principal
```powershell
py -3.11 -m src.main --stage <stage_name> [--seed <int>] [--config <path>]
```

### Argumentos y Banderas

| Argumento | Tipo | Requerido | Valor por Defecto | Valores Permitidos | Descripción |
|---|---|---|---|---|---|
| `--stage` | `string` | Sí | `all` | `audit`, `baseline`, `features`, `models`, `ensemble`, `submission`, `all` | Etapa del pipeline a ejecutar |
| `--seed` | `int` | No | `42` | Entero $\ge 0$ | Semilla global para reproducibilidad |
| `--models` | `string` | No | `lgb,cat,xgb` | Lista separada por comas | Modelos a entrenar en etapa `models` |
| `--output-dir`| `string` | No | `output` | Ruta válida de directorio | Directorio para artefactos generados |

---

## 2. Códigos de Salida (Exit Codes)

| Código | Significado | Causa Típica |
|---|---|---|
| `0` | **Success** | Etapa ejecutada correctamente, métricas y artefactos validados. |
| `1` | **Validation Error** | El archivo de submission generado no cumple el contrato (nulos, filas faltantes, rango fuera de $[0, 1]$). |
| `2` | **Data Missing / Corrupt** | Archivos `input/train.csv` o `input/test.csv` no encontrados o corruptos. |
| `3` | **Modeling / Runtime Error** | Error durante el entrenamiento o memoria insuficiente. |

---

## 3. Ejemplos de Invocación

### Ejemplo Válido (Ejecución de Baseline)
```powershell
py -3.11 -m src.main --stage baseline --seed 42
# Stdout:
# [INFO] Stage: baseline
# [INFO] 5-Fold Stratified CV initialized (Seed=42)
# [INFO] Fold 1 ROC-AUC: 0.7482
# [INFO] Fold 2 ROC-AUC: 0.7451
# [INFO] Fold 3 ROC-AUC: 0.7479
# [INFO] Fold 4 ROC-AUC: 0.7438
# [INFO] Fold 5 ROC-AUC: 0.7465
# [INFO] Mean OOF ROC-AUC: 0.7463 (+/- 0.0016)
# [INFO] Submission saved to output/submission_baseline.csv (Status: Validated)
# Exit code: 0
```

### Ejemplo Inválido (Etapa Desconocida)
```powershell
py -3.11 -m src.main --stage unknown_stage
# Stderr:
# [ERROR] Argument '--stage': Invalid choice 'unknown_stage'. Allowed: audit, baseline, features, models, ensemble, submission, all.
# Exit code: 1
```
