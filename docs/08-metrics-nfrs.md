# 08 — Métricas y Requerimientos No Funcionales (NFRs)

## 1. Métricas de Rendimiento del Modelo (Model Metrics)

| Métrica | Umbral Mínimo (Must) | Umbral Objetivo (Target) | Método de Medición |
|---|---|---|---|
| **OOF ROC-AUC Baseline** | $\ge 0.7450$ | $\ge 0.7480$ | `sklearn.metrics.roc_auc_score` sobre predicciones OOF concatenadas (171,202 filas) |
| **OOF ROC-AUC Feature Engineered** | $\ge 0.7600$ | $\ge 0.7630$ | Mismo esquema con LightGBM + nuevas features |
| **OOF ROC-AUC Ensemble Final** | $\ge 0.7680$ | $\ge 0.7720$ | Blending de LightGBM + CatBoost + XGBoost |
| **Dispersión entre Folds** | Desviación estándar $\le 0.0035$ | Desviación estándar $\le 0.0020$ | Estabilidad de métricas fold a fold |

---

## 2. Requerimientos No Funcionales (NFRs)

### NFR-01: Rendimiento Computacional y Tiempos de Ejecución
* **Tiempo total de entrenamiento 5-Fold Baseline:** $\le 3$ minutos en CPU local.
* **Tiempo total de entrenamiento 5-Fold Ensemble completo:** $\le 15$ minutos en CPU local.
* **Tiempo de inferencia sobre test (61,500 registros):** $\le 30$ segundos por modelo.

### NFR-02: Consumo de Memoria y Recursos
* **Pico de Memoria RAM:** $\le 8$ GB en todo momento.
* **Tipado de Memoria:** Conversión de columnas float de 64 bits a 32 bits y enteros a tipos óptimos (`np.float32`, `np.int32`) para reducir huella de memoria en un 50%.

### NFR-03: Determinismo y Reproducibilidad
* Todas las divisiones de datos, particiones de folds y semillas de inicialización de árboles fijadas en `42`.
* Re-ejecutar el script desde cero debe producir exactamente los mismos valores numéricos de predicción hasta el sexto decimal ($10^{-6}$).

### NFR-04: Observabilidad y Trazabilidad de Experimentos
* Cada ejecución debe emitir en consola y en archivo log estructurado:
  1. Número de fold.
  2. Número de árboles óptimos por *early stopping*.
  3. ROC-AUC en validación de cada fold.
  4. Media y desviación estándar OOF.
  5. Tamaño del archivo y hash MD5 del submission generado.
