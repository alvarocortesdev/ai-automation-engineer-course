# Ejercicio 7.5a — Diseñar un star schema + clasificar en capas medallion

> **Modalidad: a mano (sin código, sin IA).** Este ejercicio entrena tu criterio de **modelado
> analítico**: decidir el *grain*, separar hechos de dimensiones, desnormalizar a propósito y ubicar
> cada transformación en la arquitectura medallion. No se mide la prosa: se mide la **calidad de las
> decisiones de diseño**.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.5a` ELT moderno + modelado analítico
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Diseñar un **star schema** (tabla de hechos + dimensiones) a partir de un esquema
  transaccional, **declarando el grain** en una sola frase.
- **O2** — Clasificar transformaciones en la arquitectura **medallion** (bronze / silver / gold) con
  justificación.
- **O3** — Decidir **ELT vs ETL** para un caso concreto, justificando por la **causa** (costo de
  compute, privacidad, auditabilidad), no por la sigla.

## 📋 Contexto

Antes de materializar nada con dbt (lección [7.5b](../../../src/content/docs/fase-7-automatizacion/7-5b-dbt.mdx)),
tienes que **diseñar el modelo en papel**. Un star schema mal grainado contamina todo lo que se
calcule encima. Este diseño es el paso previo al capstone agéntico de la fase: el contexto de datos
que tu agente consultará sale de una tabla de hechos como la que vas a modelar aquí.

## El caso: plataforma de cursos online

En producción (OLTP), el esquema está **normalizado** (3NF):

```sql
estudiantes(estudiante_id PK, nombre, email, pais, fecha_registro)
categorias(categoria_id PK, nombre)                       -- "Programación", "Diseño", ...
cursos(curso_id PK, titulo, categoria_id FK, instructor_id FK, precio)
instructores(instructor_id PK, nombre, pais)
inscripciones(inscripcion_id PK, estudiante_id FK, curso_id FK, fecha, precio_pagado, cupon_id FK NULL)
cupones(cupon_id PK, codigo, descuento_pct)
```

Quieres responder, rápido y sobre millones de filas, preguntas como:
*ingresos por categoría por mes*, *inscripciones por país del estudiante*, *descuento promedio por
instructor*.

## Lista de transformaciones a clasificar (para la sección Medallion)

```text
T1) Cargar el export JSON crudo de inscripciones, tal cual, en modo append.
T2) Construir fact_inscripciones + dim_curso + dim_estudiante + dim_fecha (star schema).
T3) Deduplicar inscripciones repetidas y convertir las fechas string a tipo date.
T4) Resolver el precio final aplicando el descuento del cupón cuando existe (manejar el cupon_id NULL).
T5) Calcular la tabla resumen "ingresos diarios por categoría" para el dashboard de gerencia.
T6) Unificar el campo país (la web manda "CL", el sistema legado manda "Chile") a un valor canónico.
```

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces consulta **documentación oficial** (Kimball, Databricks medallion).
3. **Solo al final**, usa IA para *revisar y explicar* tu diseño — no para *generarlo*.
4. Mañana, **redibuja el star schema de memoria**. Si no puedes declarar el grain sin mirar, no lo
   aprendiste todavía.

## 🛠️ Tu tarea — entrega `diseno.md` con tres secciones

### Sección 1 — Star schema

- **Declara el grain** de `fact_inscripciones` en **una sola frase** inequívoca.
- Para la **tabla de hechos**: lista sus *medidas* (números que se suman/promedian) y sus *claves*
  hacia dimensiones. Separa claramente unas de otras.
- Para cada **dimensión** (`dim_curso`, `dim_estudiante`, `dim_fecha`, y las que falten): lista sus
  atributos. Marca al menos **un atributo desnormalizado** (traído desde otra tabla del OLTP) y
  **explica por qué** lo desnormalizas.

### Sección 2 — Medallion

- Clasifica **cada** transformación T1–T6 en **bronze / silver / gold** y justifica cada una en media
  línea. Ojo: una de ellas **no es ninguna capa todavía** —es el transporte previo— o cae claramente
  en la frontera; argumenta tu decisión.

### Sección 3 — ELT vs ETL

- Decide el enfoque para esta plataforma y **justifícalo por la causa** (costo de compute elástico,
  privacidad/regulación, auditabilidad del SQL versionado), no por la sigla de moda.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **grain** está declarado en una frase única e inequívoca.
- [ ] La tabla de hechos **separa medidas de claves** correctamente.
- [ ] Hay al menos **una desnormalización explícita y justificada**.
- [ ] Las 6 transformaciones están clasificadas en una capa con razón.
- [ ] La decisión ELT/ETL está justificada por su **causa**, no por moda.
- [ ] Puedes **explicar tu diseño sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por el grain: ¿qué representa **una fila** de `fact_inscripciones`? La respuesta más natural
es "una inscripción de un estudiante a un curso". Todo lo demás cuelga de eso. Las medidas son los
números que sumarías (`precio_pagado`, y quizá un conteo); las claves apuntan a *quién* (estudiante),
*qué* (curso), *cuándo* (fecha). La categoría y el instructor **no** son dimensiones propias del hecho:
viven **dentro** de `dim_curso` (ahí está la desnormalización). Para medallion, pregúntate por cada T:
¿deja el dato *crudo*, *limpio* o *listo para consumo*? Revisa la sección medallion de la lección antes
de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-7/star-schema-medallion-diseno/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-7/` — no la mires antes de intentarlo de
verdad. El corrector revisará tus **decisiones de diseño** (grain, desnormalización, capas), no si tu
redacción es bonita.
