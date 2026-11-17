---
id: S3-T1
sprint: 3
owner: Lead ML Engineer
effort_h: 4
depends_on: [S2-T3]
status: todo
---
# S3-T1 — Implement XGBoost Histogram Training Engine

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 3 | Lead ML Engineer | 4 | `S2-T3` | `docs/03-technical-spec.md`, `docs/09-decisions-adrs.md` |

## Purpose
Desarrollar y entrenar el motor XGBoost (`tree_method='hist'`) sobre las particiones idénticas de 5 folds construidas en el Sprint 1, generando predicciones OOF y de test.

## Preconditions
- Matriz de características del Sprint 2 aprobada y validada en Stop & Go 2.

## Interface Contract
- **Input:** `train_xgb_model(X_train, y_train, X_test, folds) -> Tuple[np.ndarray, np.ndarray, float]`
- **Output:** Tupla `(oof_preds_xgb, test_preds_xgb, xgb_auc)`.
- **Salida en disco:** `output/oof_xgb.csv` y `output/test_xgb.csv`.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_xgb_engine.py` entrenando sobre un subset pequeño sintético y verificando convergencia y métricas. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/models/xgb_engine.py` con `xgb.XGBClassifier(tree_method='hist', eval_metric='auc')` y early stopping. (1.5 h)
- **4.3 Ejecución y persistencia:** Ejecutar el entrenamiento de 5 folds en CPU, persistir predicciones OOF y calcular score global. (1.0 h)

## Deliverables
- `src/models/xgb_engine.py`
- `tests/unit/test_xgb_engine.py`
- `output/oof_xgb.csv`
- `output/test_xgb.csv`

## Acceptance Criteria
- OOF ROC-AUC de XGBoost $\ge 0.7580$.
- Tiempo total de entrenamiento $\le 4$ minutos.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_xgb_engine.py -v
py -3.11 -m src.models.xgb_engine
```

## Edge Cases & Pitfalls
- XGBoost requiere que las categorías no contengan caracteres especiales no válidos o tipos string puros; asegurar imputación adecuada de categorías o conversión a enteros.

## Risks / Scope Cuts
- Si el tiempo de cómputo en CPU es elevado, limitar `max_depth=5` y `n_estimators=1000`.

## Definition of Done
- [ ] Tests en verde.
- [ ] Predicciones OOF y test de XGBoost guardadas en `output/`.
