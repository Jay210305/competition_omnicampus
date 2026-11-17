# Implementation Index & Tracking

## 1. Índice de Tareas (Task Index)

| ID | Tarea | Archivo | Propietario | Horas | Estado |
|---|---|---|---|---|---|
| **S0-T1** | Implement Data Loader and Schema Auditor | [S0-T1-data-loader-audit.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-0-audit/S0-T1-data-loader-audit.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S0-T2** | Implement Data Cleaner and Anomaly Handler | [S0-T2-cleaner-anomalies.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-0-audit/S0-T2-cleaner-anomalies.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S1-T1** | Implement Stratified 5-Fold Cross-Validation Splitter | [S1-T1-cv-splitter.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-1-baseline/S1-T1-cv-splitter.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S1-T2** | Implement Baseline LightGBM Engine & Walking Skeleton Submission | [S1-T2-baseline-lightgbm.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-1-baseline/S1-T2-baseline-lightgbm.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S2-T1** | Implement Financial Ratios & Demographic Transformers | [S2-T1-financial-ratios.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-2-features/S2-T1-financial-ratios.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S2-T2** | Implement External Sources Interaction & Statistical Transformers | [S2-T2-external-sources.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-2-features/S2-T2-external-sources.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S2-T3** | Implement Out-of-Fold Target Encoding & Feature Matrix Verification | [S2-T3-categorical-encoders.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-2-features/S2-T3-categorical-encoders.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S3-T1** | Implement XGBoost Histogram Training Engine | [S3-T1-xgboost-engine.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-3-models/S3-T1-xgboost-engine.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S3-T2** | Implement CatBoost Engine & Model Diversity Diagnostics | [S3-T2-catboost-engine.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-3-models/S3-T2-catboost-engine.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S4-T1** | Implement OOF Blending Optimizer & Rank Averaging | [S4-T1-blending-optimizer.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-4-ensemble/S4-T1-blending-optimizer.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S5-T1** | Implement Final Submission Generator & Strict Integrity Audit | [S5-T1-submission-audit.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-5-submission/S5-T1-submission-audit.md) | Lead ML Engineer | 4 h | ⬜ todo |
| **S5-T2** | Build Standalone Reproducibility Pack & Honors Audit | [S5-T2-reproducibility-pack.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/implementation/sprint-5-submission/S5-T2-reproducibility-pack.md) | Lead ML Engineer | 4 h | ⬜ todo |

**Total Horas Tareas:** 48 h

---

## 2. Ruta Crítica (Critical Path)

```
[Sprint 0: Audit]
  S0-T1 ──► S0-T2 ──► [STOP & GO 0]
                         │
                         ▼
[Sprint 1: Baseline]
  S1-T1 ──► S1-T2 ──► [STOP & GO 1]
                         │
                         ▼
[Sprint 2: Features]
  S2-T1 ──► S2-T2 ──► S2-T3 ──► [STOP & GO 2]
                                   │
                                   ▼
[Sprint 3: Models]
  S3-T1 ──► S3-T2 ────────────► [STOP & GO 3]
                                   │
                                   ▼
[Sprint 4: Ensemble]
  S4-T1 ──────────────────────► [STOP & GO 4]
                                   │
                                   ▼
[Sprint 5: Submission & Honors]
  S5-T1 ──► S5-T2 ────────────► [STOP & GO 5 (FINAL)]
```

---

## 3. Reglas Transversales (Cross-Cutting Rules)

1. **TDD Estricto:** Cada sub-tarea implementa su test antes de escribir código productivo. Ninguna función entra a `src/` sin prueba unitaria que valide su comportamiento y casos extremos.
2. **Determinismo:** `SEED = 42` fijado en todas las operaciones que involucren aleatoriedad (splits, inicialización de modelos).
3. **Cero Fuga de Datos:** Todas las estadísticas, transformaciones y target encodings se calculan únicamente sobre los datos de entrenamiento de cada fold.
4. **Commits Convencionales:** Un commit por tarea con formato:
   `<tipo>(<ID>): <descripción corta>`
5. **Tipado y Estilo:** Type hints en todas las funciones públicas de `src/`; código PEP8 verificado con linter.
6. **Inmutabilidad de Input:** La carpeta `input/` es de estricta sólo lectura.

---

## 4. Control del Documento (Document Control)

* **Versión:** 1.0.0
* **Fecha:** 2026-11-17
* **Mantenimiento:** Lead ML Engineer (Antigravity Agent) & Product Owner (Usuario)
* **Historial de Cambios:**
  * `v1.0.0 (2026-11-17)`: Creación inicial del plan completo siguiendo la metodología de `PLANNING_METHODOLOGY.md` con 6 puntos de control Stop & Go.
