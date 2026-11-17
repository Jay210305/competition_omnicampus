---
id: S1-T1
sprint: 1
owner: Lead ML Engineer
effort_h: 4
depends_on: [S0-T2]
status: done
---
# S1-T1 — Implement Stratified 5-Fold Cross-Validation Splitter

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 1 | Lead ML Engineer | 4 | `S0-T2` | `docs/03-technical-spec.md`, `docs/09-decisions-adrs.md` |

## Purpose
Proporcionar una estrategia de partición de validación cruzada estratificada de 5 folds determinista (`random_state=42`) para garantizar que la tasa de defaults (~8.07%) se mantenga estrictamente idéntica en cada fold y evitar fuga de información.

## Preconditions
- `S0-T2` completado; dataset `train` limpio.

## Interface Contract
- **Input:** `get_stratified_folds(df: pd.DataFrame, target_col: str = "TARGET", n_splits: int = 5, seed: int = 42) -> List[Tuple[np.ndarray, np.ndarray]]`
- **Output:** Lista de 5 tuplas `(train_indices, val_indices)`.
- **Invariante:** La unión de `val_indices` cubre exactamente el 100% de `df` sin solapamientos.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_validation.py` verificando número de folds, cobertura total sin solapamiento y estratificación de clases. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/utils/validation.py` utilizando `StratifiedKFold` de scikit-learn. (1.5 h)
- **4.3 Función de evaluación OOF:** Añadir `compute_oof_roc_auc(y_true, y_pred) -> float` con cálculo de intervalo de confianza. (1.0 h)

## Deliverables
- `src/utils/validation.py`
- `tests/unit/test_validation.py`

## Acceptance Criteria
- 5 folds deterministas.
- Diferencia de tasa de `TARGET=1` entre folds $\le 0.05\%$.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_validation.py -v
```

## Edge Cases & Pitfalls
- No permitir reordenamiento sin fijar semilla (`shuffle=True, random_state=42` siempre obligatorio).

## Risks / Scope Cuts
- Ninguno; componente crítico no recortable.

## Definition of Done
- [x] Tests en `test_validation.py` en verde.
- [x] Función de cálculo de ROC-AUC OOF verificada.
