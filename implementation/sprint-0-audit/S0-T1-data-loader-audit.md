---
id: S0-T1
sprint: 0
owner: Lead ML Engineer
effort_h: 4
depends_on: []
status: done
---
# S0-T1 — Implement Data Loader and Schema Auditor

| Sprint | Owner | Effort (h) | Dependencies | Related docs |
|---|---|---|---|---|
| Sprint 0 | Lead ML Engineer | 4 | Ninguna | `docs/03-technical-spec.md`, `docs/contracts/data-contracts.md` |

## Purpose
Cargar los datasets `train.csv` y `test.csv` desde `input/`, verificar exhaustivamente que cumplan con las dimensiones esperadas (171,202 y 61,500 filas) y generar un reporte cuantitativo de nulos por columna.

## Preconditions
- Archivos `input/train.csv` y `input/test.csv` presentes en disco y con permisos de lectura.

## Interface Contract
- **Input:** Función `load_data(train_path: str, test_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]`
- **Output:** Tupla `(df_train, df_test)` con columnas y tipos verificados.
- **Errors:** `FileNotFoundError` si los archivos no existen; `ValueError` si las dimensiones o columnas obligatorias difieren.
- **Ejemplo Válido:**
  ```python
  from src.data.loader import load_data
  train, test = load_data("input/train.csv", "input/test.csv")
  assert len(train) == 171202
  assert len(test) == 61500
  ```

## Essential Sub-tasks
- **4.1 Test first (TDD):** Escribir `tests/unit/test_loader.py` probando carga de fixtures y detección de esquemas inválidos. (1.5 h)
- **4.2 Implementación:** Desarrollar `src/data/loader.py` con tipado optimizado (`float32`, `int32`) y verificación de esquemas. (1.5 h)
- **4.3 Auditoría de nulos:** Añadir función `audit_missingness(df: pd.DataFrame) -> pd.DataFrame` y refactorizar. (1.0 h)

## Deliverables
- `src/data/loader.py`
- `tests/unit/test_loader.py`

## Acceptance Criteria
- Carga de train y test en $\le 5$ segundos en memoria.
- Detección precisa de 171,202 filas en train (34 columnas) y 61,500 en test (33 columnas).

## Verification
```powershell
py -3.11 -m pytest tests/unit/test_loader.py -v
```

## Edge Cases & Pitfalls
- `test.csv` no tiene columna `TARGET`; el loader debe manejar explícitamente esta asimetría esperada.

## Risks / Scope Cuts
- Si el reporte de nulos detallado toma demasiado tiempo, generar únicamente porcentaje de nulos por columna.

## Definition of Done
- [x] Tests en `test_loader.py` pasan al 100%.
- [x] Tipos de datos convertidos a `float32`/`int32` para reducir consumo de memoria.
- [x] `status` actualizado a `done`.
