---
id: S2-T3
sprint: 2
owner: Lead ML Engineer
effort_h: 4
depends_on: [S2-T2]
status: todo
---
# S2-T3 — Implement Out-of-Fold Target Encoding & Feature Matrix Verification

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 2 | Lead ML Engineer | 4 | `S2-T2` | `docs/03-technical-spec.md` |

## Purpose
Implementar Target Encoding y Frequency Encoding libres de fuga de datos (*leakage-free*), reentrenar el modelo LightGBM sobre la nueva matriz de características de 5 folds y medir el lift de AUC frente al baseline.

## Preconditions
- `S2-T1` y `S2-T2` completados.

## Interface Contract
- **Input:** `fit_transform_oof_target_enc(df_train, df_test, cat_cols, folds, smoothing=10.0) -> Tuple[pd.DataFrame, pd.DataFrame]`
- **Regla Estricta:** Las medias por categoría para el fold de validación $k$ se calculan **únicamente** con los registros de entrenamiento de ese fold.
- **Output:** Matriz completa de características enriquecida.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_encoders.py` verificando ausencia total de target leakage en las columnas de validación. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/features/categorical_encoders.py` con codificación de frecuencia y target encoding con suavizado Bayesiano. (1.5 h)
- **4.3 Reentrenamiento & Stop & Go 2:** Entrenar LightGBM con todas las features, generar `reports/02_feature_importance_report.md` y presentar el lift de AUC al usuario. (1.0 h)

## Deliverables
- `src/features/categorical_encoders.py`
- `tests/unit/test_encoders.py`
- `reports/02_feature_importance_report.md`

## Acceptance Criteria
- Cero filtración de target en validación (probado por tests).
- Incremento de OOF ROC-AUC: $\ge 0.7620$ (superando el baseline de $0.7450$ en al menos $+0.0150$).

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_encoders.py -v
py -3.11 -m src.models.train_lgb_features
```

## Edge Cases & Pitfalls
- Categorías presentes en test pero ausentes en train deben imputarse con la media global de entrenamiento para evitar `NaN`.

## Risks / Scope Cuts
- Si el Target Encoding muestra sobreajuste o inestabilidad, aplicar el Disparador de Corte 1: descartar target encoding y retener Label + Frequency Encoding.

## Definition of Done
- [ ] Tests de target encoding libres de fuga en verde.
- [ ] OOF ROC-AUC $\ge 0.7620$ alcanzado.
- [ ] **Stop & Go Checkpoint 2 completado y auditado con el usuario.**
