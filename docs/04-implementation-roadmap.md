# 04 — Roadmap de Implementación (Sprints 0 a 5)

## 1. Resumen Ejecutivo del Roadmap

El proyecto se estructura en 6 sprints de desarrollo ágil e incremental, siguiendo el principio de **Walking Skeleton** en el Sprint 1 (pipeline vertical completo de punta a punta con generación de archivo de submission válido) antes de expandir el espacio de características y la diversidad de modelos.

Cada sprint concluye con un **Punto de Control Stop & Go** explícito donde se auditan métricas y artefactos con el usuario antes de desbloquear el siguiente sprint.

---

## Sprint 0: Setup, Data Audit & Anomaly Cleaning (Día 1)
**Duration:** 1 día | **Effort:** 8 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Auditar la calidad de los datos de entrada, identificar nulos y corregir anomalías conocidas (centinela `DAYS_EMPLOYED = 365243`).

### Deliverables
1. `src/data/loader.py`
2. `src/data/cleaner.py`
3. `reports/00_data_audit_report.md`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S0-T1 | Data loader y verificador de esquemas de entrada | 4 | Lead ML Engineer | ⬜ | Carga de 171,202 filas train y 61,500 test en $\le 5$ s; reporte de nulos generado sin error. |
| S0-T2 | Limpieza de centinelas y flags de anomalías | 4 | Lead ML Engineer | ⬜ | Valor 365243 en `DAYS_EMPLOYED` reemplazado por `NaN`; flag `DAYS_EMPLOYED_ANOM` creado; test pasa al 100%. |

### DoD
- [ ] Cobertura de pruebas en `src/data/` $\ge 85\%$
- [ ] Reporte de auditoría EDA emitido con distribución de clases (~8.07% default)
- [ ] **Stop & Go Checkpoint 0:** Aprobación del usuario del reporte de anomalías

### Mitigations
- R1 (Fuga de datos) → Tratar `cleaner.py` como transformador sin estado global (S0-T2).

---

## Sprint 1: Walking Skeleton & 5-Fold Stratified Baseline (Día 1-2)
**Duration:** 1 día | **Effort:** 8 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Construir el pipeline de validación cruzada estratificada de 5 folds y el modelo baseline LightGBM produciendo una primera submission válida.

### Deliverables
1. `src/utils/validation.py`
2. `src/models/baseline_lgb.py`
3. `output/submission_baseline.csv`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S1-T1 | Generador de particiones Stratified 5-Fold CV | 4 | Lead ML Engineer | ⬜ | Folds deterministas con semilla 42; ratio de target constante en cada fold ($8.07\% \pm 0.05\%$). |
| S1-T2 | Entrenador baseline LightGBM y generación de submission | 4 | Lead ML Engineer | ⬜ | OOF ROC-AUC $\ge 0.7450$; submission de 61,500 filas validada contra contrato de datos. |

### DoD
- [ ] Pipeline de punta a punta funcional (`train.csv` → CV → OOF → `submission_baseline.csv`)
- [ ] Cobertura de pruebas en validación y modelo $\ge 80\%$
- [ ] **Stop & Go Checkpoint 1:** Presentación de OOF ROC-AUC baseline y validación de submission

### Mitigations
- R4 (Sobreajuste) → Registro estricto de OOF de cada fold por separado (S1-T1).

---

## Sprint 2: Domain Feature Engineering Pipeline (Día 2)
**Duration:** 1 día | **Effort:** 12 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Implementar y verificar el catálogo completo de características de dominio (ratios financieros, estadísticas de fuentes externas y encodings).

### Deliverables
1. `src/features/financial_ratios.py`
2. `src/features/external_sources.py`
3. `src/features/categorical_encoders.py`
4. `reports/02_feature_importance_report.md`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S2-T1 | Ratios financieros y normalización demográfica | 4 | Lead ML Engineer | ⬜ | Ratios calculados sin división por cero (`CREDIT_INCOME_RATIO`, etc.); 0 nulos introducidos. |
| S2-T2 | Interacciones no lineales y estadísticas de EXT_SOURCE | 4 | Lead ML Engineer | ⬜ | Creación de `MEAN`, `STD`, `MIN`, `MAX`, `PROD` y productos cruzados; test de consistencia numérico OK. |
| S2-T3 | Target Encoding out-of-fold y Frequency Encoding | 4 | Lead ML Engineer | ⬜ | Target Encoding calculado exclusivamente dentro de folds de entrenamiento (0 fuga comprobada por test). |

### DoD
- [ ] Modelo LightGBM reentrenado con nuevas features alcanza OOF ROC-AUC $\ge 0.7620$ ($+0.0150$ de lift)
- [ ] Tabla de Top 25 feature importances generada
- [ ] **Stop & Go Checkpoint 2:** Aprobación del usuario del lift de AUC y ranking de variables

### Mitigations
- R1 (Fuga en target encoding) → Implementación de suavizado Bayesiano dentro del ciclo CV (S2-T3).

---

## Sprint 3: Multi-Model Scaling (XGBoost & CatBoost) (Día 2-3)
**Duration:** 1 día | **Effort:** 8 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Entrenar modelos XGBoost y CatBoost sobre los mismos 5 folds para ganar diversidad algorítmica.

### Deliverables
1. `src/models/xgb_engine.py`
2. `src/models/cat_engine.py`
3. `output/oof_xgb.csv` y `output/oof_cat.csv`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S3-T1 | Motor de entrenamiento XGBoost (hist method) | 4 | Lead ML Engineer | ⬜ | OOF ROC-AUC de XGBoost $\ge 0.7580$; inferencia test generada en $\le 3$ min. |
| S3-T2 | Motor de entrenamiento CatBoost (categorical nativo) | 4 | Lead ML Engineer | ⬜ | OOF ROC-AUC de CatBoost $\ge 0.7590$; correlación con LightGBM entre $0.92$ y $0.97$. |

### DoD
- [ ] Matriz de correlación de predicciones OOF entre LightGBM, CatBoost y XGBoost documentada
- [ ] Todos los modelos entrenados sobre particiones idénticas (semilla 42)
- [ ] **Stop & Go Checkpoint 3:** Comparativa de rendimiento individual y diversidad entre modelos

### Mitigations
- R3 (Límite de memoria) → Liberación explícita de DataFrames y recolección de basura entre entrenadores (S3-T1, S3-T2).

---

## Sprint 4: Ensembling & Blending Optimizer (Día 3)
**Duration:** 0.5 días | **Effort:** 4 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Encontrar la combinación óptima de modelos mediante optimización de pesos sobre OOF y rank averaging.

### Deliverables
1. `src/ensemble/blender.py`
2. `output/oof_ensemble.csv`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S4-T1 | Optimizador de pesos OOF y Rank Averaging | 4 | Lead ML Engineer | ⬜ | OOF ROC-AUC Ensemble $\ge 0.7680$ ($+0.0030$ superior al mejor modelo individual). |

### DoD
- [ ] Pesos de ensemble optimizados por scipy minimize (Powell / Nelder-Mead) sin sobreajuste
- [ ] **Stop & Go Checkpoint 4:** Demostración del incremento de AUC en ensemble frente a modelos base

### Mitigations
- R4 (Sobreajuste de pesos) → Regularización en función de pérdida de pesos (suma = 1, bounds $[0, 1]$).

---

## Sprint 5: Final Submission, Verification & Honors Packaging (Día 3)
**Duration:** 0.5 días | **Effort:** 8 h | **Status:** ⬜ | **Owner:** Lead ML Engineer  
**Goal:** Generar la submission final, verificar rigurosamente el contrato de datos y compilar el paquete reproducible para Honors.

### Deliverables
1. `output/submission.csv`
2. `src/main.py`
3. `reproduce_submission.py`
4. `submission_audit_report.md`

| ID | Description | Effort (h) | Assignee | Status | Acceptance criteria |
|---|---|---|---|---|---|
| S5-T1 | Auditoría estricta de submission final | 4 | Lead ML Engineer | ⬜ | 61,500 filas exactas; 0 nulos; $0.0 \le p \le 1.0$; hash de verificación OK. |
| S5-T2 | Empaquetado de script de reproducción para Honors | 4 | Lead ML Engineer | ⬜ | `reproduce_submission.py` se ejecuta de forma independiente y reproduce `output/submission.csv` bit a bit. |

### DoD
- [ ] Validación automática de contrato de submission superada al 100%
- [ ] Código documentado con citación de fuentes para auditoría académica
- [ ] **Stop & Go Checkpoint 5:** Entrega final al usuario para carga en Omnicampus

---

## 2. Reconciliación de Esfuerzo y Capacidad (Step 4)

| Componente | Horas Estimadas |
|---|---|
| **Sprint 0** (Setup & Data Audit) | 8 h |
| **Sprint 1** (Walking Skeleton & Baseline) | 8 h |
| **Sprint 2** (Feature Engineering) | 12 h |
| **Sprint 3** (Multi-Model Scaling) | 8 h |
| **Sprint 4** (Ensemble & Blending) | 4 h |
| **Sprint 5** (Final Submission & Honors Pack) | 8 h |
| **Subtotal Tareas:** | **48 h** |
| Buffer de contingencia (~15%): | 7 h |
| Documentación y reportes de auditoría: | 4 h |
| Revisiones de usuario Stop & Go (6 checkpoints $\times$ 30 min): | 3 h |
| **Total Proyecto:** | **62 h** |
| **Capacidad Total Disponible:** | **70 h** (Holgura: 8 h) |

---

## 3. Ruta Crítica y Disparadores de Corte (Critical Path & Scope Cuts)

### Ruta Crítica
```
S0 (Audit) ──► S1 (Baseline) ──► S2 (Features) ──► S3 (Models) ──► S4 (Ensemble) ──► S5 (Submission)
```
*Toda la secuencia está en ruta crítica; sin embargo, S3 y S4 pueden modularse en alcance.*

### Disparadores de Corte (Cut Triggers)
1. **Disparador 1:** Si el Sprint 2 sufre un retraso $> 4$ horas:
   * *Acción:* Descartar el Target Encoding out-of-fold (S2-T3) y retener únicamente ratios financieros e interacciones de `EXT_SOURCE`.
2. **Disparador 2:** Si el Sprint 3 sufre un retraso $> 3$ horas o problemas de memoria con CatBoost:
   * *Acción:* Descartar CatBoost (S3-T2) y entrenar únicamente LightGBM + XGBoost.
3. **Disparador 3:** Si la fecha límite está a $\le 6$ horas:
   * *Acción:* Congelar inmediatamente el ensemble al mejor modelo validado (LightGBM optimizado) y ejecutar directamente S5 (Submission & Verificación).
