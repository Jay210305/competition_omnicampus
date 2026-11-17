---
id: S5-T1
sprint: 5
owner: Lead ML Engineer
effort_h: 4
depends_on: [S4-T1]
status: todo
---
# S5-T1 — Implement Final Submission Generator & Strict Integrity Audit

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 5 | Lead ML Engineer | 4 | `S4-T1` | `docs/contracts/data-contracts.md` |

## Purpose
Generar el archivo de predicciones final `output/submission.csv` y someterlo a una batería rigurosa de verificaciones de integridad respecto a `input/sample_submission.csv` para garantizar que no existan discrepancias que puedan ocasionar penalización (score -1) en Omnicampus.

## Preconditions
- Predicciones del ensemble del Sprint 4 aprobadas en Stop & Go 4.

## Interface Contract
- **Input:** Predicciones de test del ensemble `best_test_preds`, `sample_submission.csv`.
- **Output:** `output/submission.csv` formateado y validado.
- **Batería de Verificación Obligatoria:**
  1. Número exacto de líneas: 61,501 (incluyendo header).
  2. Nombres de columnas exactos: `SK_ID_CURR,TARGET`.
  3. Alineación exacta de IDs de clientes con `sample_submission.csv`.
  4. Cero valores `NaN`, `null`, `Inf` o vacíos.
  5. Todas las probabilidades contenidas en $[0.0, 1.0]$.
  6. Comparación de percentiles de predicción frente a la tasa real de defaults de train (~8.07%).

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/integration/test_submission_audit.py` probando todos los casos de fallo (filas de más/menos, IDs alterados, valores fuera de rango). (1.5 h)
- **4.2 Implementación:** Desarrollar `src/utils/submission_auditor.py` con generación de reporte detallado de sanidad. (1.5 h)
- **4.3 Ejecución y validación de `submission.csv`:** Generar el archivo final y validar todas las reglas de negocio. (1.0 h)

## Deliverables
- `output/submission.csv`
- `src/utils/submission_auditor.py`
- `tests/integration/test_submission_audit.py`
- `reports/05_submission_audit_report.md`

## Acceptance Criteria
- 100% de cumplimiento con las reglas de validación sin una sola advertencia.
- `output/submission.csv` emitido y verificado en disco.

## Verification
```powershell
py -3.11 -m pytest tests/integration/test_submission_audit.py -v
py -3.11 -m src.utils.submission_auditor --file output/submission.csv
```

## Edge Cases & Pitfalls
- Nunca permitir que pandas exporte el índice numérico (`index=False` siempre obligatorio).

## Risks / Scope Cuts
- Ninguno; verificación de misión crítica no negociable.

## Definition of Done
- [ ] Batería de tests de submission en verde.
- [ ] Reporte de sanidad `reports/05_submission_audit_report.md` generado.
- [ ] Archivo `output/submission.csv` listo para descarga y envío.
