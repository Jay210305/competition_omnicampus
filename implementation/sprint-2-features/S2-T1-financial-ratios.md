---
id: S2-T1
sprint: 2
owner: Lead ML Engineer
effort_h: 4
depends_on: [S1-T2]
status: todo
---
# S2-T1 — Implement Financial Ratios & Demographic Transformers

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 2 | Lead ML Engineer | 4 | `S1-T2` | `docs/03-technical-spec.md` |

## Purpose
Generar variables de dominio financiero y sociodemográfico (`CREDIT_INCOME_RATIO`, `ANNUITY_INCOME_RATIO`, `PAYMENT_RATE`, `GOODS_CREDIT_RATIO`, `EMPLOYED_TO_AGE_RATIO`, `INCOME_PER_FAMILY_MEMBER`) garantizando estabilidad numérica sin divisiones por cero.

## Preconditions
- Baseline de Sprint 1 validado.

## Interface Contract
- **Input:** `add_financial_ratios(df: pd.DataFrame) -> pd.DataFrame`
- **Output:** DataFrame enriquecido con 6 nuevas columnas de ratios.
- **Fórmulas:**
  - `CREDIT_INCOME_RATIO = df['AMT_CREDIT'] / (df['AMT_INCOME_TOTAL'] + 1e-5)`
  - `ANNUITY_INCOME_RATIO = df['AMT_ANNUITY'] / (df['AMT_INCOME_TOTAL'] + 1e-5)`
  - `PAYMENT_RATE = df['AMT_ANNUITY'] / (df['AMT_CREDIT'] + 1e-5)`
  - `GOODS_CREDIT_RATIO = df['AMT_GOODS_PRICE'] / (df['AMT_CREDIT'] + 1e-5)`
  - `EMPLOYED_TO_AGE_RATIO = df['DAYS_EMPLOYED'] / (df['DAYS_BIRTH'] + 1e-5)`
  - `INCOME_PER_FAMILY_MEMBER = df['AMT_INCOME_TOTAL'] / (df['CNT_FAM_MEMBERS'] + 1e-5)`

## Essential Sub-tasks
- **4.1 Test first (TDD):** Escribir `tests/unit/test_financial_ratios.py` probando valores extremos (ingreso cero, crédito cero, valores nulos). (1.5 h)
- **4.2 Implementación:** Desarrollar `src/features/financial_ratios.py` implementando los ratios con protección contra overflow/división por cero. (1.5 h)
- **4.3 Integración:** Conectar el transformador al pipeline de features y verificar consistencia en memoria. (1.0 h)

## Deliverables
- `src/features/financial_ratios.py`
- `tests/unit/test_financial_ratios.py`

## Acceptance Criteria
- Cero divisiones por cero (0 valores `Inf`).
- Las 6 variables se crean correctamente tanto en train como en test.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_financial_ratios.py -v
```

## Edge Cases & Pitfalls
- `AMT_ANNUITY` o `AMT_GOODS_PRICE` contienen valores nulos originalmente en el dataset. El ratio resultante debe mantener `NaN` en lugar de fallar o generar `Inf`.

## Risks / Scope Cuts
- Ninguno; ratios esenciales de bajo coste computacional.

## Definition of Done
- [ ] Tests en `test_financial_ratios.py` en verde.
- [ ] Ratios integrados sin errores.
