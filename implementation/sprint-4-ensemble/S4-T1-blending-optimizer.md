---
id: S4-T1
sprint: 4
owner: Lead ML Engineer
effort_h: 4
depends_on: [S3-T2]
status: todo
---
# S4-T1 — Implement OOF Blending Optimizer & Rank Averaging

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 4 | Lead ML Engineer | 4 | `S3-T2` | `docs/03-technical-spec.md` |

## Purpose
Combinar las predicciones OOF y de test de los tres modelos (LightGBM, CatBoost y XGBoost) mediante dos estrategias: (1) Rank Averaging (promedio de rangos percentiles) y (2) Optimización de pesos de probabilidad vía Nelder-Mead / Powell con SciPy, buscando maximizar el ROC-AUC conjunto.

## Preconditions
- Predicciones OOF y test de LightGBM, CatBoost y XGBoost disponibles en `output/`.

## Interface Contract
- **Input:** `optimize_blend(oof_list: List[np.ndarray], y_true: np.ndarray, test_list: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]`
- **Output:** Tupla `(best_oof_preds, best_test_preds, optimal_weights, best_auc)`.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_ensemble.py` probando optimización de pesos sobre predicciones simuladas y preservación de suma a 1. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/ensemble/blender.py` con `scipy.optimize.minimize` (loss = `-roc_auc_score`) con restricciones de pesos no negativos. (1.5 h)
- **4.3 Evaluación comparativa & Stop & Go 4:** Comparar el score del ensemble contra los modelos individuales y documentar la ganancia. (1.0 h)

## Deliverables
- `src/ensemble/blender.py`
- `tests/unit/test_ensemble.py`
- `reports/04_ensemble_benchmark_report.md`

## Acceptance Criteria
- OOF ROC-AUC del ensemble $\ge 0.7680$ (superando al mejor modelo individual en al menos $+0.0020$).
- Pesos no negativos y sumando 1.0.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_ensemble.py -v
py -3.11 -m src.ensemble.blender
```

## Edge Cases & Pitfalls
- Sobreoptimización de pesos: utilizar los pesos calculados en OOF directamente sobre el conjunto de test sin recalibrar ni modificar manualmente.

## Risks / Scope Cuts
- Si la optimización por scipy converge a mínimos locales inestables, adoptar el Rank Averaging puro con pesos uniformes `(1/3, 1/3, 1/3)`.

## Definition of Done
- [ ] Tests en verde.
- [ ] Ganancia de AUC del ensemble demostrada empíricamente.
- [ ] **Stop & Go Checkpoint 4 completado y presentado al usuario.**
