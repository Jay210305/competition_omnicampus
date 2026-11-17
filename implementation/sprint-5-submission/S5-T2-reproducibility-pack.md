---
id: S5-T2
sprint: 5
owner: Lead ML Engineer
effort_h: 4
depends_on: [S5-T1]
status: todo
---
# S5-T2 — Build Standalone Reproducibility Pack & Honors Audit

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 5 | Lead ML Engineer | 4 | `S5-T1` | `docs/10-glossary-references.md`, `README.ipynb` |

## Purpose
Generar un script ejecutable autocontenido y un notebook reproducible (`reproduce_submission.py` / `reproduce_submission.ipynb`) que permita a los evaluadores de la competición reproducir exactamente el archivo `output/submission.csv` desde cero, cumpliendo con todos los requisitos para consideración a Mención de Honor / Alumno Destacado (*Honors/Outstanding Student*).

## Preconditions
- `S5-T1` completado y validado.

## Interface Contract
- **Input:** Comando único en consola limpia `py -3.11 reproduce_submission.py`.
- **Output:** Genera `output/submission.csv` idéntico bit a bit (mismo hash MD5) al archivo entregado.
- **Requisitos de Honors:**
  - Código estructurado y comentado.
  - Citación explícita de referencias y kernels originales (Aguiar 2018, Tunguz 2018, etc.).
  - Semillas aleatorias fijadas.
  - Empaquetado en `output/solution_pack.zip`.

## Essential Sub-tasks
- **4.1 Test first (TDD):** Crear `tests/e2e/test_reproducibility.py` que ejecute el pipeline sobre un sample determinista y verifique igualdad de hash. (1.5 h)
- **4.2 Implementación del script autocontenido:** Consolidar `reproduce_submission.py` con todas las dependencias modulares empaquetadas. (1.5 h)
- **4.3 Empaquetado ZIP & Stop & Go 5:** Crear `output/solution_pack.zip` y presentar el reporte de cierre final al usuario. (1.0 h)

## Deliverables
- `reproduce_submission.py`
- `output/solution_pack.zip`
- `tests/e2e/test_reproducibility.py`
- `reports/final_project_closure_report.md`

## Acceptance Criteria
- La re-ejecución del script reproduce `submission.csv` con coincidencia numérica absoluta.
- Zip generado conteniendo código y documentación listo para Honors.

## Verification
```powershell
py -3.11 -m pytest tests/e2e/test_reproducibility.py -v
py -3.11 reproduce_submission.py
```

## Edge Cases & Pitfalls
- Discrepancias de versiones de librerías: congelar las dependencias con `py -3.11 -m pip freeze > requirements.txt`.

## Risks / Scope Cuts
- Si el tiempo no permite exportar a notebook interactivo, entregar el script `.py` documentado y validado (válido para Honors según las reglas).

## Definition of Done
- [ ] Reproducibilidad verificada por test E2E.
- [ ] Paquete `solution_pack.zip` generado.
- [ ] **Stop & Go Checkpoint 5 completado y firmado con el usuario.**
