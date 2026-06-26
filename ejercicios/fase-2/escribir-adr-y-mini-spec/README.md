# Ejercicio 2.13 — Mini-spec + ADR de una decisión real

> **Modalidad: razonamiento/diseño (sin IA primero).** No se corrige con tests verdes: se corrige
> con la **calidad de tus artefactos**. Es spec-driven dev en miniatura — el músculo de *pensar antes
> de teclear* y *dejar registro de por qué* — que separa al semi-senior del que improvisa.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.13` Colaboración, spec-driven dev y ADRs
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Escribir un **mini-spec** que resuelva la ambigüedad de una feature *antes* de codearla (entradas,
salidas, casos borde, criterios de aceptación falsables) y un **ADR** que capture la decisión técnica
significativa que el spec destapa, con contexto, opciones consideradas, decisión y consecuencias.

## 📋 Contexto

El issue es vago a propósito. Tu trabajo no es implementar: es **convertir la ambigüedad en un
contrato** y **registrar la decisión que el código esconde**. En el Capstone F2 arrancarás con un
mini-spec y documentarás tus decisiones en ADRs; este ejercicio es el ensayo directo de ese hábito.

> **Feature a especificar (NO la implementes):**
> `acortar_titulo(titulo, max_len)` — recorta un título largo para mostrarlo en una tarjeta de UI.
> Debe "verse bien": no cortar a mitad de palabra si se puede evitar, y señalar que hubo recorte.

## 📏 Primero-Sin-IA

1. Resuelve la ambigüedad **solo**, a mano, dentro del timebox. Decide tú; defiende tú.
2. Solo entonces relee la sección 4.2–4.3 de la lección (mini-spec + ADR) y ajusta el formato.
3. **Solo al final**, usa IA para *cuestionar* tu spec/ADR —no para escribirlos.
4. Mañana, escribe el ADR **de memoria**: si no te salen las 4 secciones, no lo aprendiste.

## 🛠️ Instrucciones

Tienes dos starters en esta carpeta: `spec.md` y `adr-0001-plantilla.md`. Complétalos.

1. **`spec.md`** — completa:
   - **Objetivo** (1 línea).
   - **Entradas**: tipos **y restricciones** (no solo `str` e `int`; ¿`max_len` puede ser 0? ¿negativo?).
   - **Salida**: tipo y la **invariante** que siempre se cumple.
   - **≥3 casos borde acordados**: como mínimo (a) el título ya es más corto que `max_len`;
     (b) `max_len` minúsculo (p. ej. 3); (c) ¿el carácter de elipsis "…" cuenta dentro de `max_len`
     o se suma aparte? Resuélvelos **a propósito**, no "lo veré al codear".
   - **Criterios de aceptación**: checklist **falsable** (cada ítem se puede volver un test).
2. **`adr-0001-<renómbralo>.md`** — identifica la **decisión técnica significativa** que el spec
   destapó (al menos una; la elipsis dentro/fuera de `max_len`, o cortar en el último espacio vs corte
   duro) y escríbela con la estructura completa: **contexto/problema**, **2-3 opciones con pro/contra**,
   **decisión + por qué**, **consecuencias (+/−) y un gatillo de revisión**.

> ⚠️ **No escribas la implementación.** Si te descubres codeando `acortar_titulo`, paraste de
> especificar y empezaste a adivinar. El entregable son los **artefactos**, no la función.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `spec.md` tiene entradas con **restricciones** (no solo tipos), salida con **invariante**, y **≥3 casos borde** resueltos a propósito.
- [ ] Los criterios de aceptación son **falsables** (se pueden volver tests), no deseos vagos ("que se vea bien").
- [ ] El ADR nombra **≥2 opciones** con su pro y su contra (no una sola "decisión obvia").
- [ ] La decisión está **justificada por el contexto** e incluye un **gatillo** de cuándo reabrirla.
- [ ] Puedes **defender en voz alta** por qué resolviste cada caso borde así.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `spec.md` — el mini-spec completo.
- `adr-0001-<slug>.md` — el ADR de la decisión significativa.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El truco del spec no es predecir el código: es **destapar las preguntas que el código te obligaría a
contestar a la mala**. Recorre `acortar_titulo` con tres entradas extremas: un título de 4 caracteres
con `max_len=20` (no recortes), uno de 100 con `max_len=3` (¿cabe siquiera "…"?), y uno donde el
último espacio queda lejos del corte (¿corte duro o palabra colgando?). Cada respuesta no-obvia es un
**caso borde** (spec) o una **decisión** (ADR). La mejor candidata a ADR suele ser "¿la elipsis cuenta
dentro de `max_len`?": cambia el resultado y es defendible en ambos sentidos. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tus `spec.md` y `adr-0001-<slug>.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/escribir-adr-y-mini-spec.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/escribir-adr-y-mini-spec.md` — no la mires
antes de intentarlo de verdad. El corrector evalúa la **calidad de tu razonamiento**, no si coincidiste
con una respuesta única (no la hay).
