# Data Contracts — Schemas & Validation Rules

## 1. Contrato de Entrada: `input/train.csv`

* **Propósito:** Conjunto de datos etiquetado para entrenamiento y validación cruzada.
* **Dimensiones esperadas:** 171,202 filas $\times$ 34 columnas.
* **Formato:** CSV delimitado por comas, codificación UTF-8 o ASCII estándar.
* **Esquema de Columnas Clave:**

| Columna | Tipo de Dato | Nulos Permitidos | Rango / Valores Válidos | Descripción |
|---|---|---|---|---|
| `SK_ID_CURR` | `int64` | No | Entero positivo único | Identificador del solicitante |
| `TARGET` | `int64` | No | `{0, 1}` | Variable objetivo (1: default, 0: no default) |
| `NAME_CONTRACT_TYPE`| `string/object` | No | `{"Cash loans", "Revolving loans"}` | Tipo de contrato |
| `CODE_GENDER` | `string/object` | No | `{"M", "F", "XNA"}` | Género del cliente |
| `AMT_INCOME_TOTAL` | `float64` | No | $> 0` | Ingresos totales declarados |
| `AMT_CREDIT` | `float64` | No | $> 0` | Monto total del crédito solicitado |
| `AMT_ANNUITY` | `float64` | Sí | $\ge 0$ | Cuota anual del préstamo |
| `DAYS_BIRTH` | `int64` | No | $\le 0$ (en días negativos) | Edad en días al momento de la solicitud |
| `DAYS_EMPLOYED` | `int64` | No | Entero (incluye centinela 365243) | Días en empleo actual |
| `EXT_SOURCE_1` | `float64` | Sí | $[0.0, 1.0]$ o `NaN` | Puntaje crediticio externo 1 |
| `EXT_SOURCE_2` | `float64` | Sí | $[0.0, 1.0]$ o `NaN` | Puntaje crediticio externo 2 |
| `EXT_SOURCE_3` | `float64` | Sí | $[0.0, 1.0]$ o `NaN` | Puntaje crediticio externo 3 |

---

## 2. Contrato de Entrada: `input/test.csv`

* **Propósito:** Conjunto de datos sin etiquetar para evaluación de la competición.
* **Dimensiones esperadas:** 61,500 filas $\times$ 33 columnas (mismas columnas que train excepto `TARGET`).
* **Regla de integridad:** El conjunto de IDs en `test.csv` debe coincidir exactamente con los IDs de `sample_submission.csv`.

---

## 3. Contrato de Salida: `output/submission.csv`

* **Propósito:** Archivo final para subir a la plataforma Omnicampus.
* **Dimensiones esperadas:** Exactamente 61,500 filas de datos + 1 fila de encabezado (total 61,501 líneas).
* **Columnas obligatorias:** Exactamente dos columnas denominadas `SK_ID_CURR,TARGET`.
* **Reglas de Validación Estrictas:**
  1. `SK_ID_CURR`: Entero de 6 dígitos coincidente uno a uno en orden o valor con `input/sample_submission.csv`.
  2. `TARGET`: Probabilidad continua en formato decimal, $0.0 \le \text{TARGET} \le 1.0$.
  3. Cero valores `NaN`, `null`, `inf`, vacíos o espacios en blanco.

### Ejemplo Válido de Submission
```csv
SK_ID_CURR,TARGET
171202,0.0842
171203,0.1251
171204,0.0319
171205,0.2410
```

### Ejemplo Inválido (Rechazado)
```csv
SK_ID_CURR,TARGET
171202,NaN       <-- Error: Valor nulo no permitido
171203,-0.05     <-- Error: Probabilidad fuera de rango [0, 1]
171204,1.45      <-- Error: Probabilidad mayor que 1
                 <-- Error: Menos de 61,500 filas
```
