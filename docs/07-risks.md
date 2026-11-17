# 07 — Matriz de Riesgos y Mitigaciones

| ID | Riesgo | Impacto | Probabilidad | Propietario | Estrategia de Mitigación |
|---|---|---|---|---|---|
| **R1** | **Fuga de datos (Data Leakage) en validación** | Crítico | Media | Lead ML Engineer | Implementar aislamiento estricto de transformaciones dentro de cada fold (`fit` sólo en train del fold, `transform` en val/test). Test unitario específico de validación de fuga. |
| **R2** | **Formato inválido de submission en Omnicampus** | Crítico | Baja | Lead ML Engineer | Validador automatizado que compara dimensionalidad, columnas, nulos y rango contra `input/sample_submission.csv` antes de emitir cualquier CSV de salida. |
| **R3** | **Desbordamiento de memoria (OOM) con múltiples GBDTs** | Alto | Media | Lead ML Engineer | Recolección de basura forzada (`gc.collect()`), eliminación de copias innecesarias de DataFrames y tipos de datos eficientes (`float32`, `int32`). |
| **R4** | **Sobreajuste (Overfitting) al Public Leaderboard** | Alto | Media | Product Owner / Lead ML Engineer | Confiar en la métrica local OOF ROC-AUC de 5 folds como único criterio de decisión para seleccionar modelos y mezclas. |
| **R5** | **Retraso temporal frente al deadline (20 Noviembre)** | Alto | Media | Product Owner | Aplicar disparadores de corte (Cut Triggers) definidos en el roadmap: eliminar modelos secundarios o encodings complejos si el tiempo apremia. |
| **R6** | **No reproducibilidad para opción a Honors** | Alto | Baja | Lead ML Engineer | Fijar todas las semillas (`random_state=42`), documentar el entorno (`pip list`) y generar un script de ejecución autocontenido `reproduce_submission.py`. |
