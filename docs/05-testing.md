# 05 — Estrategia de Pruebas y Validación (Testing)

## 1. Pirámide de Pruebas

```
        / \
       /   \        E2E Tests (10%)
      /  E2E\       Pipeline completo: input -> features -> CV -> submission
     /-------\
    /         \     Integration / Contract Tests (30%)
   /Integration\    Contratos de CSV, validación de esquemas, aislamiento de folds
  /-------------\
 /               \  Unit Tests (60%)
/    Unit Tests   \ Limpieza de anomalías, fórmulas de ratios, encodings, métricas
-------------------
```

---

## 2. Niveles de Prueba y Alcance

### 2.1 Pruebas Unitarias (`tests/unit/`)
* **`test_cleaning.py`:** Verifica que el valor `365243` en `DAYS_EMPLOYED` se reemplace por `NaN` y que `DAYS_EMPLOYED_ANOM` sea binario.
* **`test_financial_ratios.py`:** Verifica la estabilidad numérica de ratios (sin división por cero con ingresos = 0).
* **`test_external_sources.py`:** Comprueba el cálculo de medias y productos cruzados frente a datos sintéticos conocidos.
* **`test_metrics.py`:** Comprueba que la función de cálculo de ROC-AUC coincida con el estándar de `scikit-learn`.

### 2.2 Pruebas de Contrato e Integración (`tests/integration/`)
* **`test_data_contracts.py`:** Verifica que los archivos `input/train.csv` y `input/test.csv` cumplan los tipos y rangos definidos en `docs/contracts/data-contracts.md`.
* **`test_fold_isolation.py`:** Verifica que los transformadores (imputadores, target encoders) ajustados en el fold $k$ no filtren estadísticas del conjunto de validación (test de cero fuga de datos).
* **`test_submission_contract.py`:** Verifica que cualquier archivo generado en `output/` cumpla:
  * Exactamente 61,500 filas de predicción.
  * Columnas `SK_ID_CURR,TARGET`.
  * Probabilidades en $[0.0, 1.0]$.
  * 0 valores `NaN`, `Inf` o nulos.

### 2.3 Pruebas de Sistema / End-to-End (`tests/e2e/`)
* **`test_pipeline_smoke.py`:** Ejecuta un pipeline sintético reducido (100 filas, 2 folds, 10 árboles) de punta a punta para garantizar que no existan errores de tipado o importación.

---

## 3. Fixtures y Datos Sintéticos de Prueba

* Se utiliza `pytest` con fixtures en `tests/conftest.py`:
  * `sample_raw_df`: DataFrame sintético de 20 filas con casos límite (ingreso 0, crédito 0, `DAYS_EMPLOYED = 365243`, `EXT_SOURCE` nulos).
  * `dummy_submission_df`: DataFrame de validación de contrato.

---

## 4. Umbrales de Cobertura y Ejecución

* **Cobertura Mínima Requerida:** $\ge 80\%$ de líneas en `src/`.
* **Comando de Verificación:**
  ```powershell
  py -3.11 -m pytest tests -v --cov=src --cov-report=term-missing
  ```
