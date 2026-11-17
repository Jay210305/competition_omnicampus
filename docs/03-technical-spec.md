# 03 — Especificación Técnica

## 1. Referencia a Contratos

Los contratos de interfaz y esquemas de datos son fuente única de verdad y residen en:
* **Contratos de Datos:** [docs/contracts/data-contracts.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/docs/contracts/data-contracts.md)
* **Contrato de CLI y Ejecución:** [docs/contracts/cli-contract.md](file:///c:/Users/jay21/Documents/Universidad/Omnicampus/Competition/docs/contracts/cli-contract.md)

---

## 2. Esquemas de Datos Internos y Transformaciones

### 2.1 Limpieza y Corrección de Centinelas
* `DAYS_EMPLOYED`: Si el valor es igual a `365243`, se transforma a `np.nan` y se crea una columna indicadora binaria `DAYS_EMPLOYED_ANOM = 1` (y `0` para el resto).
* `DAYS_BIRTH`, `DAYS_REGISTRATION`, `DAYS_ID_PUBLISH`: Valores negativos en días. Se transforman a años positivos dividiendo por `-365.25` para interpretabilidad de árboles.

### 2.2 Especificación de Ratios Financieros
1. `CREDIT_INCOME_RATIO = AMT_CREDIT / (AMT_INCOME_TOTAL + 1e-5)`
2. `ANNUITY_INCOME_RATIO = AMT_ANNUITY / (AMT_INCOME_TOTAL + 1e-5)`
3. `PAYMENT_RATE = AMT_ANNUITY / (AMT_CREDIT + 1e-5)`
4. `GOODS_CREDIT_RATIO = AMT_GOODS_PRICE / (AMT_CREDIT + 1e-5)`
5. `INCOME_PER_FAMILY_MEMBER = AMT_INCOME_TOTAL / (CNT_FAM_MEMBERS + 1e-5)`
6. `EMPLOYED_TO_AGE_RATIO = DAYS_EMPLOYED / (DAYS_BIRTH + 1e-5)`

### 2.3 Especificación de Interacciones de Fuentes Externas
Las columnas `EXT_SOURCE_1`, `EXT_SOURCE_2` y `EXT_SOURCE_3` concentran más del 60% de la importancia de características en modelos de crédito de Home Credit. Se generan:
* `EXT_SOURCES_MEAN = row_mean([EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3])`
* `EXT_SOURCES_STD = row_std([EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3])`
* `EXT_SOURCES_MIN = row_min([EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3])`
* `EXT_SOURCES_MAX = row_max([EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3])`
* `EXT_SOURCES_PROD = EXT_SOURCE_1 * EXT_SOURCE_2 * EXT_SOURCE_3`
* `EXT_1_x_EXT_2 = EXT_SOURCE_1 * EXT_SOURCE_2`
* `EXT_2_x_EXT_3 = EXT_SOURCE_2 * EXT_SOURCE_3`
* `EXT_1_x_EXT_3 = EXT_SOURCE_1 * EXT_SOURCE_3`
* `EXT_2_x_PAYMENT_RATE = EXT_SOURCE_2 * PAYMENT_RATE`

### 2.4 Encodings Categóricos
* **Label Encoding:** Para variables con cardinalidad baja ($\le 5$ valores únicos), compatible nativamente con LightGBM y CatBoost.
* **Frequency Encoding:** Para variables con cardinalidad media-alta (`ORGANIZATION_TYPE`, `OCCUPATION_TYPE`). Se calcula como la proporción de aparición en el dataset.
* **Out-of-Fold Target Encoding:** Para categorías de alta correlación con la mora, calculando la media de `TARGET` por categoría **exclusivamente sobre el conjunto de entrenamiento de cada fold**, agregando suavizado Bayesiano para categorías infrecuentes.

---

## 3. Estrategia de Validación Cruzada (CV)

* **Algoritmo:** `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
* **Métrica de Evaluación:** `sklearn.metrics.roc_auc_score(y_true, y_pred_prob)`
* **Aislamiento de Folds:** Todas las transformaciones dependientes de datos (imputadores, normalizadores, target encodings) se ajustan (`fit`) únicamente en el split de entrenamiento del fold y se aplican (`transform`) en el split de validación y en el conjunto de test.
* **Agregación de Predicciones de Test:** Cada modelo entrenado en el fold $k$ ($k=1..5$) predice sobre el conjunto de test. La predicción final del modelo es el promedio de las 5 predicciones:
  $$\hat{y}_{\text{test}} = \frac{1}{5} \sum_{k=1}^5 \hat{y}_{\text{test}, k}$$

---

## 4. Modelado y Algoritmos

### 4.1 LightGBM
* `objective`: `binary`
* `metric`: `auc`
* `boosting_type`: `gbdt`
* `learning_rate`: `0.03`
* `num_leaves`: `31`
* `max_depth`: `-1`
* `colsample_bytree`: `0.8`
* `subsample`: `0.8`
* `n_estimators`: `2000` con `early_stopping_rounds`: `100`

### 4.2 CatBoost
* `loss_function`: `Logloss`
* `eval_metric`: `AUC`
* `iterations`: `2000` con `early_stopping_rounds`: `100`
* `learning_rate`: `0.04`
* `depth`: `6`
* `random_seed`: `42`

### 4.3 XGBoost
* `objective`: `binary:logistic`
* `eval_metric`: `auc`
* `tree_method`: `hist`
* `learning_rate`: `0.03`
* `max_depth`: `6`
* `subsample`: `0.8`
* `colsample_bytree`: `0.8`
* `n_estimators`: `2000` con `early_stopping_rounds`: `100`

---

## 5. Modelo de Errores y Logging

* El pipeline utiliza el módulo estándar `logging` de Python con formato estructurado:
  `[%(levelname)s] %(asctime)s - %(name)s - %(message)s`
* Todas las excepciones de validación de esquemas lanzan `SchemaValidationError` detallando la fila/columna infractora.
* En caso de discrepancia en el número de filas o presencia de nulos en `output/submission.csv`, la ejecución aborta inmediatamente con código de salida `1`.
