# 10 — Glosario y Referencias Citadas

## 1. Glosario Técnico

* **ROC-AUC (Receiver Operating Characteristic - Area Under Curve):** Medida de separabilidad entre clases binarias; evalúa el orden relativo de las probabilidades independientemente del umbral de decisión.
* **Stratified K-Fold:** Técnica de particionado en $K$ subconjuntos preservando el porcentaje exacto de cada clase en cada fold.
* **OOF (Out-of-Fold) Predictions:** Vector de predicciones concatenado donde cada observación es predicha exclusivamente por el modelo que no la vio en su conjunto de entrenamiento.
* **Target Encoding:** Reemplazo de categorías cualitativas por el valor medio esperado de la variable objetivo condicional a dicha categoría.
* **Frequency Encoding:** Transformación de una categoría categórica en su frecuencia relativa en el dataset.
* **Rank Averaging:** Promedio ponderado de los percentiles o rangos normalizados de las predicciones en lugar de sus probabilidades directas, útil cuando los modelos tienen diferente calibración de probabilidad pero buen ordenamiento.

---

## 2. Referencias Citadas (Reglamento de Citas y Honors)

En cumplimiento con el reglamento de la competición GCI Global 2026 sobre transparencia y citación de código de referencia:
1. **Tutorial Oficial:** `tutorial.ipynb` (GCI Global 2026 In-class Competition Tutorial).
2. **Kaggle Home Credit Default Risk (2018):**
   * Aguiar, W. (2018). *LightGBM with Simple Features*. Kaggle Discussion & Kernel. (Inspiración para ratios financieros: `CREDIT_INCOME_RATIO`, `PAYMENT_RATE` y tratamiento de anomalía de `DAYS_EMPLOYED`).
   * Bojan Tunguz, Dan Becker, et al. (2018). *Introduction to Manual Feature Engineering: EXT_SOURCE interactions*.
3. **Scikit-learn Documentation:** *Cross-validation: evaluating estimator performance & StratifiedKFold*.
4. **LightGBM Documentation:** *Parameters and Early Stopping in Binary Classification*.
