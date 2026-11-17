---
id: S2-T2
sprint: 2
owner: Lead ML Engineer
effort_h: 4
depends_on: [S2-T1]
status: todo
---
# S2-T2 — Implement External Sources Interaction & Statistical Transformers

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 2 | Lead ML Engineer | 4 | `S2-T1` | `docs/03-technical-spec.md` |

## Purpose
Construir agregaciones estadísticas e interacciones no lineales entre las 3 variables más predictivas del dataset (`EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3`), extrayendo el máximo poder predictivo de los scores externos de riesgo.

## Preconditions
- `S2-T1` completado.

## Interface Contract
- **Input:** `add_external_sources_features(df: pd.DataFrame) -> pd.DataFrame`
- **Output:** DataFrame con nuevas variables estadísticas e interacciones (`MEAN`, `STD`, `MIN`, `MAX`, `PROD`, `EXT_1_x_EXT_2`, `EXT_2_x_EXT_3`, `EXT_1_x_EXT_3`, `EXT_2_x_PAYMENT_RATE`).

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_external_sources.py` con combinaciones de nulos y valores conocidos. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/features/external_sources.py` calculando agregaciones vectorizadas eficientes en NumPy/Pandas. (1.5 h)
- **4.3 Optimización y tipado:** Convertir nuevas columnas a `np.float32` para preservar memoria. (1.0 h)

## Deliverables
- `src/features/external_sources.py`
- `tests/unit/test_external_sources.py`

## Acceptance Criteria
- Variables agregadas calculadas correctamente incluso si 1 o 2 de las fuentes externas son `NaN`.
- Las interacciones numéricas pasan todos los tests de paridad estadística.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_external_sources.py -v
```

## Edge Cases & Pitfalls
- Cuando las 3 fuentes externas son nulas en un registro, `row_mean` y `row_prod` deben resultar en `NaN` consistente, no en cero arbitrario.

## Risks / Scope Cuts
- Si el producto cruzado `EXT_2_x_PAYMENT_RATE` presenta multicolinealidad extrema, retener sólo las estadísticas agregadas (`MEAN`, `STD`, `MIN`, `MAX`).

## Definition of Done
- [ ] Tests en `test_external_sources.py` en verde.
- [ ] Módulo integrado en el generador de la matriz de características.
