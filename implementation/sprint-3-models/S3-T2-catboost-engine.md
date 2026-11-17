---
id: S3-T2
sprint: 3
owner: Lead ML Engineer
effort_h: 4
depends_on: [S3-T1]
status: todo
---
# S3-T2 — Implement CatBoost Engine & Model Diversity Diagnostics

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 3 | Lead ML Engineer | 4 | `S3-T1` | `docs/03-technical-spec.md`, `docs/09-decisions-adrs.md` |

## Purpose
Entrenar el motor CatBoost sobre los mismos 5 folds y evaluar la diversidad de predicciones calculando la matriz de correlación de Pearson y Spearman entre las predicciones OOF de LightGBM, CatBoost y XGBoost.

## Preconditions
- `S3-T1` completado; predicciones de XGBoost y LightGBM disponibles.

## Interface Contract
- **Input:** `train_catboost_model(X_train, y_train, X_test, folds, cat_features) -> Tuple[np.ndarray, np.ndarray, float]`
- **Output:** Tupla `(oof_preds_cat, test_preds_cat, cat_auc)`.
- **Salida en disco:** `output/oof_cat.csv` y reporte de correlación.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_cat_engine.py` validando manejo de categorías nativas y cálculo de AUC. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/models/cat_engine.py` con `CatBoostClassifier(eval_metric='AUC', early_stopping_rounds=100)`. (1.5 h)
- **4.3 Diagnóstico de diversidad & Stop & Go 3:** Calcular la matriz de correlación entre los 3 modelos y presentar la tabla comparativa al usuario. (1.0 h)

## Deliverables
- `src/models/cat_engine.py`
- `tests/unit/test_cat_engine.py`
- `output/oof_cat.csv`
- `reports/03_model_diversity_report.md`

## Acceptance Criteria
- OOF ROC-AUC de CatBoost $\ge 0.7590$.
- Correlación de Pearson entre predicciones de los modelos en el rango ideal $[0.92, 0.97]$ (confirmando diversidad efectiva).

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_cat_engine.py -v
py -3.11 -m src.models.cat_engine
```

## Edge Cases & Pitfalls
- CatBoost requiere que las categorías nulas se representen como strings constantes (p. ej. `"MISSING"`) en lugar de `NaN` numérico.

## Risks / Scope Cuts
- Si CatBoost sobrepasa el límite de memoria, aplicar el Disparador de Corte 2: descartar CatBoost y enfocar el ensemble en LightGBM + XGBoost.

## Definition of Done
- [ ] Tests en verde.
- [ ] Reporte de correlación y diversidad generado.
- [ ] **Stop & Go Checkpoint 3 completado y auditado con el usuario.**
