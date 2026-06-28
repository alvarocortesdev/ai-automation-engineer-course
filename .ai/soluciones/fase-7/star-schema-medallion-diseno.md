---
ejercicio_id: fase-7/star-schema-medallion-diseno
fase: fase-7
sub_unidad: "7.5a"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diseñar un star schema + clasificar en capas medallion

No hay una única redacción correcta. Lo que sigue es el conjunto de decisiones que un diseño
**competente** cubre. **Excelente** = además articula la causa raíz (el cambio de objetivo respecto a
F3) y los matices de capa.

## Sección 1 — Star schema

### Grain (la decisión más importante)

> **Una fila de `fact_inscripciones` = una inscripción de un estudiante a un curso.**

Inequívoco. (Aceptable también "una inscripción + pago" si el alumno lo razona; lo que NO es aceptable
es "a nivel de estudiante" o "a nivel de curso" —eso pierde el detalle.)

### Tabla de hechos: `fact_inscripciones`

| Tipo | Columnas | Comentario |
|---|---|---|
| **Claves** (FK a dimensiones) | `estudiante_key`, `curso_key`, `fecha_key` | hacia *quién*, *qué*, *cuándo* |
| **Medidas** (se suman/promedian) | `precio_pagado`, `inscripciones` (= 1 por fila, para conteos) | números; `precio_pagado` ya es el final |
| (opcional) degenerate dimension | `inscripcion_id` | el id de negocio, útil para trazar al origen |

El `cupon_id` / descuento **no** se guarda como dimensión separada típica de análisis; el efecto del
cupón ya está resuelto en `precio_pagado` (ver T4). Aceptable modelar `dim_cupon` si se justifica
(analizar uso de cupones), pero no es obligatorio.

### Dimensiones

- **`dim_curso`** — `curso_key`, `titulo`, **`categoria`** (desnormalizada desde `categorias`),
  **`instructor`**, **`instructor_pais`** (desnormalizados desde `instructores`), `precio_lista`.
- **`dim_estudiante`** — `estudiante_key`, `nombre`, **`pais`**, `segmento`, `fecha_registro`.
- **`dim_fecha`** — `fecha_key`, `dia`, `mes`, `trimestre`, `anio` (dimensión de calendario clásica).

### Desnormalización justificada (clave del ejercicio)

En el OLTP, `categoria` e `instructor` viven en tablas propias (`categorias`, `instructores`) para no
repetirlos —normalización 3NF, óptima para **escribir** sin anomalías. En el star schema los **copio
dentro de `dim_curso`**, repitiéndolos en cada fila de curso. Razón: en analítica se hace *un join
menos por query* sobre millones de filas de hechos, y la dimensión se escribe poco y se lee muchísimo.

**Causa raíz (excelente):** cambió el objetivo. F3 normaliza para evitar anomalías de escritura; aquí
se desnormaliza para minimizar joins de lectura. El mismo dato, objetivo opuesto, decisión opuesta —y
ambas correctas en su contexto.

## Sección 2 — Medallion

| T | Capa | Por qué |
|---|---|---|
| T1 — cargar JSON crudo en append | **bronze** | dato crudo, tal cual llegó, sin tocar; fuente de verdad reproducible. |
| T3 — deduplicar + parsear fechas | **silver** | limpieza/tipado: vuelve el dato confiable. |
| T4 — resolver precio final con cupón (NULL) | **silver** | regla de negocio de limpieza/integración que produce el dato validado. |
| T6 — unificar país ("CL" vs "Chile") | **silver** | integración/canonicalización de fuentes. |
| T2 — star schema (`fact_inscripciones` + dims) | **gold** | modelo de consumo listo para el negocio. |
| T5 — resumen "ingresos diarios por categoría" | **gold** | tabla pre-agregada para un dashboard. |

**Matiz (excelente):** T2 y T5 son **ambas gold** pero con propósito distinto —T2 es el modelo
dimensional de consumo; T5 es una agregación servida para un dashboard concreto. T3 (deduplicación) es
la frontera que convierte bronze en algo confiable (silver). La **extracción** desde la API (si el
alumno la menciona) es transporte previo, **no** una capa.

## Sección 3 — ELT vs ETL

**ELT.** Causa: el warehouse (BigQuery/Snowflake/Databricks) ofrece compute elástico y barato, así que
conviene **cargar el crudo primero** (bronze) y transformar **después, dentro del warehouse**, con SQL
versionado (dbt). Beneficios concretos para esta plataforma: iterar métricas nuevas sin re-extraer,
guardar el histórico crudo, y auditar la transformación en Git.

**Matiz (excelente):** si hubiera PII regulada que exigiera anonimizar **antes** de cargar, ETL
volvería a tener sentido. ELT es el default moderno *porque* se abarató el compute, no un dogma.

## Rango de soluciones aceptables

- Cualquier grain inequívoco a nivel de inscripción cuenta como competente, aunque incluya el matiz del
  pago.
- La frontera silver/gold es aceptable mientras la deduplicación/limpieza quede en silver y el modelo
  dimensional + resúmenes en gold.
- Modelar o no `dim_cupon` es opcional; lo que importa es que el efecto del cupón esté resuelto en la
  medida `precio_pagado`.
- ELT es la respuesta esperada; mencionar la excepción de privacidad sube a excelente pero no es
  requisito de competente.
