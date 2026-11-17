# 01 — Overview & Requerimientos del Sistema

## 1. Visión y Casos de Uso

El proyecto implementa una solución de clasificación crediticia de alto rendimiento para la competición *Home Credit Default Risk*. El sistema toma registros tabulares con datos sociodemográficos, financieros y de historial crediticio, y predice la probabilidad calibrada de que un solicitante incurra en mora.

### Casos de Uso Principales
1. **CU-01 (Auditoría y Validación de Datos):** Cargar `train.csv` y `test.csv`, detectar anomalías (p. ej. `DAYS_EMPLOYED = 365243`), cuantificar nulos y verificar la paridad entre esquemas.
2. **CU-02 (Transformación e Ingeniería de Características):** Transformar variables crudas en variables enriquecidas respetando el principio de aislamiento de folds para evitar fuga.
3. **CU-03 (Entrenamiento CV y Generación de OOF):** Entrenar modelos GBDT con partición estratificada de 5 folds, registrar métricas OOF y guardar modelos entrenados.
4. **CU-04 (Ensemble y Blending):** Combinar las predicciones OOF de múltiples familias de modelos para maximizar el ROC-AUC conjunto.
5. **CU-05 (Generación y Verificación de Submission):** Generar las predicciones de test, aplicar verificaciones de sanidad formal y emitir `output/submission.csv` listo para subir a Omnicampus.

---

## 2. Clasificación de Restricciones

### No Negociables (Strict Constraints)
* **Plazo de entrega:** Finaliza el 20 de Noviembre a la 1:00 AM UTC.
* **Prohibición de Datos Externos:** Uso exclusivo de `input/train.csv` y `input/test.csv`.
* **Prohibición de Hand-Labeling:** Ninguna modificación manual de predicciones individuales.
* **Formato de Salida:** Archivo CSV con cabeceras `SK_ID_CURR,TARGET`, idéntico a `sample_submission.csv` en tamaño y tipos.

### Con Límite Superior (Capped Constraints)
* **Memoria RAM:** Uso máximo de 8 GB durante entrenamiento e inferencia.
* **Tiempo de Ejecución:** Entrenamiento del pipeline completo $\le 15$ minutos en la máquina local.
* **Almacenamiento en Disco:** Artefactos intermedios y modelos $\le 2$ GB.

### Negociables (Negotiable / Trade-offs)
* **Número de modelos en ensemble:** Se puede reducir de 3 a 2 si los tiempos o recursos se ven comprometidos.
* **Búsqueda exhaustiva de hiperparámetros (Optuna):** Reducir el número de *trials* si el rendimiento de los hiperparámetros base con regularización ya alcanza los umbrales de éxito.

---

## 3. Priorización de Requerimientos (MoSCoW)

| ID | Prioridad | Requerimiento | Descripción |
|---|---|---|---|
| **REQ-M01** | **Must** | Validación Cruzada Estratificada | 5-Fold Stratified K-Fold con semilla fija (`SEED = 42`). |
| **REQ-M02** | **Must** | Baseline LightGBM | Pipeline inicial reproducible con cálculo estricto de OOF ROC-AUC. |
| **REQ-M03** | **Must** | Corrección de Anomalía de Empleo | Tratamiento del valor 365243 en `DAYS_EMPLOYED` como NaN y generación del flag `DAYS_EMPLOYED_ANOM`. |
| **REQ-M04** | **Must** | Ratios Financieros de Dominio | Creación de `CREDIT_INCOME_RATIO`, `ANNUITY_INCOME_RATIO`, `PAYMENT_RATE` y `GOODS_CREDIT_RATIO`. |
| **REQ-M05** | **Must** | Interacciones de EXT_SOURCE | Estadísticas agregadas (`MEAN`, `STD`, `MIN`, `MAX`, `PROD`) y productos cruzados de las 3 fuentes externas. |
| **REQ-M06** | **Must** | Verificación de Submission | Validación automática de número de filas (61,500), IDs, ausencia de NaN/Inf y rango $[0, 1]$. |
| **REQ-M07** | **Must** | Puntos de Control Stop & Go | Paradas explícitas de auditoría tras cada hito para revisión de métricas antes de avanzar. |
| **REQ-S01** | **Should** | Multimodelo CatBoost & XGBoost | Implementación de modelos complementarios sobre los mismos 5 folds para ganar diversidad. |
| **REQ-S02** | **Should** | Blending / Ensemble Óptimo | Ponderación de predicciones OOF mediante optimización de pesos o promedio por rangos. |
| **REQ-S03** | **Should** | Target Encoding Out-of-Fold | Encodings categóricos calculados estrictamente dentro del conjunto de entrenamiento de cada fold. |
| **REQ-C01** | **Could** | Optimización con Optuna | Ajuste fino de regularización (`colsample_bytree`, `subsample`, `reg_alpha`, `reg_lambda`). |
| **REQ-C02** | **Could** | Frequency Encoding | Conteo de frecuencia de categorías de alta cardinalidad. |
| **REQ-W01** | **Won't** | Modelos Neuronales Profundos | Redes tipo MLP / TabNet descartadas por ratio costo/beneficio en tiempo y recursos. |
| **REQ-W02** | **Won't** | Pseudo-labeling | Descartado para evitar riesgo de sobreajuste o penalizaciones de reproducibilidad. |
