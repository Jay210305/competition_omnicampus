---
id: S0-T2
sprint: 0
owner: Lead ML Engineer
effort_h: 4
depends_on: [S0-T1]
status: done
---
# S0-T2 — Implement Data Cleaner and Anomaly Handler

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 0 | Lead ML Engineer | 4 | `S0-T1` | `docs/03-technical-spec.md` |

## Purpose
Sanitizar anomalías conocidas del dataset de Home Credit, específicamente el valor centinela `DAYS_EMPLOYED = 365243` (jubilados/desempleados), convirtiéndolo a `NaN` e introduciendo una bandera explícita `DAYS_EMPLOYED_ANOM`.

## Preconditions
- `S0-T1` completado y verificado.

## Interface Contract
- **Input:** `clean_anomalies(df: pd.DataFrame) -> pd.DataFrame`
- **Output:** DataFrame con `DAYS_EMPLOYED` corregido y nueva columna `DAYS_EMPLOYED_ANOM` (`int8`).
- **Comportamiento:**
  ```python
  df["DAYS_EMPLOYED_ANOM"] = (df["DAYS_EMPLOYED"] == 365243).astype("int8")
  df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace({365243: np.nan})
  ```

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/unit/test_cleaner.py` con registros con `DAYS_EMPLOYED == 365243` y valores normales. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/data/cleaner.py` aplicando la sustitución de centinelas y flags. (1.5 h)
- **4.3 Reporte EDA & Stop & Go 0:** Emitir `reports/00_data_audit_report.md` con estadísticas y presentar al usuario. (1.0 h)

## Deliverables
- `src/data/cleaner.py`
- `tests/unit/test_cleaner.py`
- `reports/00_data_audit_report.md`

## Acceptance Criteria
- Cero ocurrencias de `365243` en `DAYS_EMPLOYED` tras la limpieza.
- `DAYS_EMPLOYED_ANOM` tiene exactamente valor `1` en las filas afectadas y `0` en el resto.

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_cleaner.py -v
```

## Edge Cases & Pitfalls
- Asegurarse de que `clean_anomalies` se aplique de forma idéntica tanto a `train.csv` como a `test.csv` sin fugas entre ellos.

## Risks / Scope Cuts
- Si surgen otras columnas con centinelas numéricos extremos, marcarlas como `NaN` preservando un flag.

## Definition of Done
- [x] Tests en `test_cleaner.py` en verde.
- [x] Reporte `reports/00_data_audit_report.md` generado.
- [x] **Stop & Go Checkpoint 0 completado y auditado.**
