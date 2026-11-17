# 06 — CI/CD, Quality Gates y Ambientes

## 1. Tabla Unificada de Quality Gates (Quality Gates Table)

Esta tabla define los criterios objetivos que deben cumplirse antes de dar por cerrada cualquier tarea o sprint tanto localmente como en CI:

| Gate | Herramienta | Umbral / Criterio | Acción en Fallo |
|---|---|---|---|
| **Formato y Linter** | `ruff` o `flake8` | 0 errores de sintaxis o estilo | Bloqueo de commit |
| **Pruebas Unitarias** | `pytest` | 100% de tests verdes | Bloqueo de avance de tarea |
| **Cobertura de Código**| `pytest-cov` | Cobertura $\ge 80\%$ en `src/` | Bloqueo de DoD del Sprint |
| **Contrato de Submission** | `src/utils/validation.py` | 61,500 filas, 0 nulos, rango $[0, 1]$ | Rechazo de submission y fallo del pipeline |
| **Consistencia de Semilla** | Verificación determinista | Folds y predicciones idénticas con `SEED=42` | Bloqueo de entrega |
| **Tiempo de Inferencia** | Benchmark local | Generación de test $\le 3$ minutos | Alerta y optimización |

---

## 2. Estrategia de Ramas y Commits

* **Rama Principal:** `main` (código estable, probado y listo para reproducción).
* **Convención de Commits:** Conventional Commits con trazabilidad de tareas:
  * `feat(S1-T2): implement baseline LightGBM trainer and submission generator`
  * `test(S2-T1): add unit tests for financial ratios without division by zero`
  * `fix(S0-T2): treat DAYS_EMPLOYED 365243 anomaly as NaN with indicator flag`

---

## 3. Entorno de Ejecución (Execution Environment)

* **Intérprete Principal:** Python 3.11 x64 (verificado en el sistema local).
* **Dependencias de Producción:**
  * `lightgbm == 4.7.0`
  * `xgboost == 3.2.0`
  * `catboost == 1.2.10`
  * `scikit-learn == 1.8.0`
  * `pandas == 3.0.3`
  * `numpy == 2.4.6`
  * `scipy == 1.17.1`
* **Dependencias de Testing:**
  * `pytest >= 8.0`
  * `pytest-cov`
