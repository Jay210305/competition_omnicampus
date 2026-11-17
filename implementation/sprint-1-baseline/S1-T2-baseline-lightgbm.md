---
id: S1-T2
sprint: 1
owner: Lead ML Engineer
effort_h: 4
depends_on: [S1-T1]
status: todo
---
# S1-T2 — Implement Baseline LightGBM Engine & Walking Skeleton Submission

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 1 | Lead ML Engineer | 4 | `S1-T1` | `docs/03-technical-spec.md`, `docs/contracts/data-contracts.md` |

## Purpose
Construir el primer pipeline vertical completo (*Walking Skeleton*): entrenar un modelo LightGBM baseline sobre los 5 folds, registrar el score OOF de referencia y emitir el primer archivo de submission validado `output/submission_baseline.csv`.

## Preconditions
- `S1-T1` completado; generador de folds disponible.

## Interface Contract
- **Input:** `train_baseline_lgb(df_train: pd.DataFrame, df_test: pd.DataFrame, folds: List) -> Tuple[np.ndarray, np.ndarray, float]`
- **Output:** Tupla `(oof_preds, test_preds, mean_auc)`.
- **Salida en disco:** `output/submission_baseline.csv` (formato `SK_ID_CURR,TARGET`).

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/integration/test_baseline_pipeline.py` ejecutando 2 folds sintéticos y verificando emisión de submission. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/models/baseline_lgb.py` con `LGBMClassifier`, `early_stopping` sobre AUC y agregación test. (1.5 h)
- **4.3 Verificador de Submission & Stop & Go 1:** Crear `src/utils/submission_validator.py`, validar `submission_baseline.csv` y presentar métricas. (1.0 h)

## Deliverables
- `src/models/baseline_lgb.py`
- `src/utils/submission_validator.py`
- `output/submission_baseline.csv`
- `tests/integration/test_baseline_pipeline.py`

## Acceptance Criteria
- OOF ROC-AUC $\ge 0.7450$.
- `output/submission_baseline.csv` cumple estrictamente: 61,500 filas, 0 nulos, rango $[0.0, 1.0]$.

## Verification
```powershell
py -3.11 -m pytest tests/integration/test_baseline_pipeline.py -v
py -3.11 -m src.models.baseline_lgb
```

## Edge Cases & Pitfalls
- Asegurarse de que el cálculo de `predict_proba` tome la columna índice 1 (probabilidad de `TARGET=1`).

## Risks / Scope Cuts
- Si los 2000 árboles toman demasiado tiempo en CPU, ajustar `n_estimators=1000` con `learning_rate=0.05`.

## Definition of Done
- [ ] OOF ROC-AUC $\ge 0.7450$ registrado y documentado.
- [ ] `submission_baseline.csv` validado contra contrato sin errores.
- [ ] **Stop & Go Checkpoint 1 completado y presentado al usuario.**
