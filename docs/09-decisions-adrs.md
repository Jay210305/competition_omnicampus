# 09 — Registro de Decisiones de Arquitectura (ADRs)

## ADR-001: Selección del Entorno de Ejecución Python 3.11

* **Contexto:** El sistema cuenta con Python 3.14 (sistema por defecto) y Python 3.13 / 3.11 en el usuario. Python 3.14 no posee wheels binarios precompilados en Windows para librerías críticas de Gradient Boosting (`catboost`, `xgboost`, `lightgbm`).
* **Opciones Consideradas:**
  1. Compilar desde fuentes en Python 3.14 (riesgo alto de incompatibilidad de compiladores C++).
  2. Utilizar el entorno Python 3.11 existente donde los wheels oficiales de `lightgbm 4.7.0`, `xgboost 3.2.0` y `catboost 1.2.10` instalan y funcionan de forma nativa.
* **Decisión:** Utilizar explícitamente Python 3.11 (`py -3.11`) para todo el pipeline y pruebas.
* **Consecuencias:** Estabilidad absoluta de librerías, sin dependencia de compilación local y compatibilidad comprobada.

---

## ADR-002: Esquema de Validación 5-Fold Stratified K-Fold

* **Contexto:** El problema presenta un desbalance de clases de ~8.07% de mora (`TARGET` = 1) sobre 171,202 registros. Una partición simple train/validation del 20% (usada en el tutorial) introduce alta varianza en la estimación de la métrica en leaderboard y desperdicia datos valiosos.
* **Opciones Consideradas:**
  1. Holdout simple 80/20 (enfoque del tutorial).
  2. K-Fold estándar sin estratificación.
  3. Stratified 5-Fold Cross-Validation.
* **Decisión:** Adoptar Stratified 5-Fold Cross-Validation con semilla `42`.
* **Consecuencias:** Todas las observaciones de entrenamiento se evalúan fuera de muestra (OOF), generando un estimador no sesgado del AUC que correlaciona fielmente con el Private Leaderboard. Permite además promediar 5 modelos en inferencia de test para reducir la varianza.

---

## ADR-003: Modelado Multimodelo GBDT vs. Redes Neuronales

* **Contexto:** Se requiere maximizar la métrica ROC-AUC en datos tabulares con heterogeneidad de tipos y valores nulos.
* **Opciones Consideradas:**
  1. Únicamente LightGBM con búsqueda de hiperparámetros.
  2. Híbrido Red Neuronal Tabular (PyTorch) + LightGBM.
  3. Ensemble de múltiples familias de árboles: LightGBM + CatBoost + XGBoost.
* **Decisión:** Desarrollar un ensemble de las 3 familias GBDT principales (LightGBM, CatBoost, XGBoost).
* **Consecuencias:** Las distintas implementaciones de árboles (split por hojas vs. simétricos de CatBoost vs. histogramas de XGBoost) ofrecen errores no correlacionados, generando un impulso probado de $+0.003$ a $+0.007$ en ROC-AUC sin la fragilidad ni los tiempos de cómputo de redes neuronales.

---

## ADR-004: Metodología Stop & Go con Puntos de Control Explícitos

* **Contexto:** El usuario requiere auditar y verificar detalladamente las decisiones, métricas y artefactos en cada fase del desarrollo antes de continuar la ejecución.
* **Opciones Consideradas:**
  1. Ejecución continua autónoma de punta a punta.
  2. Checkpoints explícitos "Stop & Go" tras cada sprint/hito donde se emite un reporte auditable y se detiene la ejecución a la espera de validación.
* **Decisión:** Adoptar la arquitectura Stop & Go de 6 checkpoints (0 a 5).
* **Consecuencias:** Garantiza que no se avance con código o transformaciones defectuosas, previene la degradación silenciosa de métricas y otorga control total al usuario.
