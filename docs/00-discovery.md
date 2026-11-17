# 00 — Discovery & Problem Formulation

## 1. Problema y Objetivo

**Problema:** En el marco de la competición in-class de Omnicampus "Home Credit Default Risk" (GCI Global 2026), se requiere predecir con alta precisión la probabilidad de impago (*default*, `TARGET` = 1) de clientes solicitantes de préstamos utilizando exclusivamente datos tabulares censurados.

**Objetivo:** Desarrollar un pipeline integral de Machine Learning supervisado, reproducible y libre de fuga de datos (*data leakage*), que optimice la métrica **ROC-AUC** sobre el conjunto de test (`input/test.csv`), estructurado en fases con puntos de control de parada y auditoría (*Stop & Go*) antes de cada avance.

### Criterios de Éxito Medibles
1. **OOF ROC-AUC Baseline:** $\ge 0.7450$ en validación cruzada estratificada de 5 folds (superando significativamente el 0.68-0.70 del tutorial).
2. **OOF ROC-AUC con Ingeniería de Características:** $\ge 0.7620$ en la misma partición CV.
3. **OOF ROC-AUC Ensemble Final:** $\ge 0.7680$ (objetivo stretch: $\ge 0.7720$).
4. **Integridad de Submission:** 100% de cumplimiento con `input/sample_submission.csv` (exactamente 61,500 filas, columnas `SK_ID_CURR,TARGET`, 0 nulos, predicciones acotadas estrictamente en $[0.0, 1.0]$).
5. **Tiempo de Ejecución:** Entrenamiento y evaluación completa de 5 folds en $\le 15$ minutos en hardware local.
6. **Reproducibilidad:** Semillas aleatorias fijadas (`SEED = 42`); ejecución determinista documentada para opción a mención de honor (*Honors/Outstanding Student*).

---

## 2. Interesados y Equipo (Stakeholders & Team)

| Rol | Responsable | Dedicación | Responsabilidades |
|---|---|---|---|
| **Product Owner / Auditor** | Usuario (Data Scientist) | 10 h/semana | Aprobación de especificaciones, revisión de métricas en puntos *Stop & Go*, toma de decisiones de corte. |
| **Lead ML Engineer / Implementador** | Antigravity AI Agent | Continuo | Diseño técnico, desarrollo TDD, ejecución de experimentos, generación de artefactos y reportes. |

---

## 3. Alcance (Scope) y Fuera de Alcance (Out of Scope)

### Dentro del Alcance (In Scope)
* **Auditoría EDA exhaustiva:** Detección y tratamiento del centinela `DAYS_EMPLOYED = 365243`, imputación y flags de nulidad en variables clave (`EXT_SOURCE_1`, `EXT_SOURCE_3`, `OWN_CAR_AGE`).
* **Ingeniería de Características de Dominio:**
  * Ratios financieros (`CREDIT_INCOME_RATIO`, `ANNUITY_INCOME_RATIO`, `PAYMENT_RATE`, `GOODS_CREDIT_RATIO`).
  * Interacciones no lineales y estadísticas de fuentes externas (`EXT_SOURCE_1/2/3`: media, desviación, mínimo, máximo, producto, productos cruzados).
  * Variables demográficas y de empleo normalizadas (`DAYS_EMPLOYED_PERCENT`, `INCOME_PER_FAMILY_MEMBER`).
  * Target Encoding out-of-fold (sin fuga) y Frequency Encoding en variables de alta cardinalidad (`ORGANIZATION_TYPE`, `OCCUPATION_TYPE`).
* **Esquema de Validación:** 5-Fold Stratified K-Fold con semilla fija (`SEED = 42`).
* **Modelado Multimodelo GBDT:** LightGBM, CatBoost y XGBoost evaluados bajo el mismo esquema de folds.
* **Ensemble:** Blending optimizado sobre predicciones OOF (promedio ponderado / rank averaging).
* **Auditoría Stop & Go:** Checkpoints formales con reporte de métricas y validación antes de proceder a la siguiente etapa.
* **Paquete de Reproducibilidad:** Script/notebook autocontenido con citación de fuentes para auditoría académica.

### Fuera del Alcance (Out of Scope)
* **Datos externos:** Estrictamente prohibido por las reglas de la competición (`input/train.csv` y `input/test.csv` únicamente).
* **Etiquetado manual (*Hand-Labeling*):** Prohibido por reglamento. Ninguna regla heurística modificará predicciones puntuales de test.
* **Deep Learning pesado / Redes Neuronales complejas:** Ineficientes para datos tabulares en este plazo temporal y con recursos locales estándar.
* **APIs o Interfaces Gráficas Web:** El entregable es un pipeline de código reproducible y el archivo `output/submission.csv`.

---

## 4. Supuestos y Dependencias Externas

### Supuestos
1. `input/train.csv` (171,202 filas) y `input/test.csv` (61,500 filas) son representativos y provienen de la misma distribución subyacente.
2. La métrica de evaluación en la plataforma Omnicampus es el Área Bajo la Curva ROC (ROC-AUC).
3. El hardware local dispone de al menos 8 GB de memoria RAM libre y soporte multi-hilo para CPU.

### Dependencias
* Python 3.11 x64 instalado y funcional.
* Librerías verificadas: `pandas >= 2.0`, `numpy`, `scipy`, `scikit-learn >= 1.5`, `lightgbm >= 4.0`, `xgboost >= 2.0`, `catboost >= 1.2`, `optuna >= 3.0`.
* Conexión a la plataforma Omnicampus gestionada por el usuario para la carga del archivo `output/submission.csv`.

---

## 5. Glosario de Términos del Dominio

* **TARGET:** Variable objetivo binaria (1 = cliente con dificultades de pago / mora; 0 = préstamo pagado en término).
* **ROC-AUC:** Receiver Operating Characteristic - Area Under Curve. Métrica de ranking entre probabilidades predichas y clases reales.
* **OOF (Out-of-Fold):** Predicciones generadas sobre la porción de validación de cada fold sin que el modelo haya visto esos registros en entrenamiento.
* **EXT_SOURCE_1, 2, 3:** Puntuaciones crediticias normalizadas de fuentes externas; son los predictores individuales más potentes del dataset.
* **Data Leakage (Fuga de datos):** Contaminación de información del conjunto de test o de los folds de validación dentro del conjunto de entrenamiento.
* **Stop & Go:** Punto de control donde el agente detiene la ejecución para auditar métricas y artefactos con el usuario antes de continuar.
