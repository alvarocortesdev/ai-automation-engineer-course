---
ejercicio_id: fase-2/escribir-adr-y-mini-spec
fase: fase-2
sub_unidad: "2.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). **Importante:** este ejercicio **no tiene
> respuesta correcta única.** Esto es una *orientación de qué artefacto es defendible*, no una plantilla a
> la que el alumno deba converger. Califica si **resolvió la ambigüedad y pesó alternativas**, no si
> coincidió con estas decisiones.

# Solución de referencia — Mini-spec + ADR de una decisión real

## Cómo usar esta solución
El alumno entrega `spec.md` + `adr-0001-<slug>.md`. Contrasta su trabajo contra la dirección de abajo.
Lo que mide la rúbrica es si el spec **cierra los bordes a propósito** y si el ADR **pesa ≥2 opciones
con un gatillo**, no si llegó a estas mismas decisiones. Una decisión contraria, bien fundada, es
`competente`/`excelente`.

## `spec.md` de referencia (una versión defendible)

```markdown
# Spec — acortar_titulo(titulo, max_len)

## Objetivo
Recortar un título para que quepa en una tarjeta de UI sin pasarse de `max_len`
caracteres y señalando visualmente que hubo recorte.

## Entradas
- titulo: str. Puede ser "" o solo espacios (se devuelve tal cual si cabe).
- max_len: int, >= 1. Si max_len <= 0 → ValueError (no tiene sentido un ancho 0).

## Salida
- str. Invariante: len(resultado) <= max_len SIEMPRE.

## Casos borde (acordados)
1. len(titulo) <= max_len → se devuelve el título intacto (sin elipsis).
2. max_len muy chico (1-2, menor que "…" útil) → se devuelve titulo[:max_len]
   (corte duro, sin elipsis: no cabe). Decisión, no accidente.
3. La elipsis "…" CUENTA dentro de max_len (ver ADR-0001): el resultado con
   recorte es titulo recortado + "…", y el total no supera max_len.
4. Se prefiere cortar en el último espacio antes del límite; si no hay espacio
   razonable (palabra larguísima), se corta duro.

## Criterios de aceptación (falsables)
- [ ] len(acortar_titulo(t, n)) <= n para todo t, n>=1.
- [ ] Si len(t) <= n, acortar_titulo(t, n) == t (sin elipsis).
- [ ] Si hubo recorte y n permite elipsis, el resultado termina en "…".
- [ ] max_len <= 0 lanza ValueError.
```

## `adr-0001` de referencia (la decisión significativa)

```markdown
# ADR-0001 — La elipsis cuenta dentro de max_len

- Estado: aceptado
- Fecha: 2026-06-26
- Decididores: alumno

## Contexto y problema
Al recortar, se añade "…" para señalar el corte. ¿Ese carácter cuenta dentro de
max_len o se suma aparte? Si no se decide, dos implementaciones dan largos
distintos y la invariante "cabe en la tarjeta" se rompe en una de ellas.

## Opciones consideradas
1. **La elipsis cuenta dentro de max_len.** Garantiza len(resultado) <= max_len
   siempre (la UI nunca se desborda). Contra: con max_len chico queda poco texto.
2. **La elipsis se suma aparte (max_len + 1).** Más texto visible. Contra: rompe
   la promesa "cabe en max_len"; la UI puede desbordarse 1 carácter.

## Decisión
Opción 1: la elipsis cuenta dentro de max_len. El objetivo es "caber en la
tarjeta"; una invariante estricta (len <= max_len) es más valiosa que 1 carácter
extra de texto.

## Consecuencias
- (+) Invariante simple y testeable: el resultado nunca supera max_len.
- (−) Con max_len muy chico (3-4) queda poquísimo texto antes de "…".
- Gatillo de revisión: si diseño/UX pide priorizar texto visible sobre el ajuste
  exacto, reabrir y migrar a la opción 2 (elipsis aparte).
```

## Razonamiento paso a paso (lo que el corrector busca)
1. **El spec resuelve, no describe.** Lo valioso es que cada borde tiene una respuesta *elegida*
   (corte duro cuando no cabe la elipsis, espacio vs corte duro, max_len<=0 → error). Un spec que dice
   "recorta bien" no resolvió nada.
2. **La invariante es el corazón.** `len(resultado) <= max_len` es lo que vuelve falsables los criterios
   y conecta con tests (property-based ideal). Sin invariante explícita, el spec es prosa.
3. **El ADR pesa una alternativa real.** "Elipsis dentro vs aparte" es una decisión genuina con
   consecuencias opuestas y defendibles; por eso es buena candidata a ADR. La decisión está atada al
   objetivo (caber), no al gusto, y tiene gatillo.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Spec = implementación.** Si hay pseudo-código de `acortar_titulo`, el alumno codeó en vez de
   especificar. C1 en-progreso como mucho; señalar que el spec define *qué*, no *cómo*.
2. **Bordes sin resolver.** "Veré la elipsis al codear" es justo la ambigüedad que el ejercicio pide
   cerrar. C1 incompleto/en-progreso.
3. **ADR de una opción.** Sin alternativa con su contra, no hubo decisión: hubo un capricho documentado.
4. **ADR sin gatillo.** Una decisión "no hago X" sin el evento que la reabriría está a medias.
5. **Confundir spec y ADR.** El spec es el contrato del comportamiento (todos los bordes); el ADR es UNA
   decisión técnica con sus alternativas. Meter todo en uno solo pierde ambos propósitos.

## Rango de soluciones aceptables
- **Elipsis aparte (opción 2)** como decisión: perfectamente válido **si** el ADR reconoce que sacrifica
  la invariante estricta y lo justifica (priorizar texto). Es el trade-off lo que se califica.
- **Corte duro siempre (sin intentar respetar palabras):** aceptable si el spec lo declara como decisión
  explícita (simplicidad) y no como omisión. Mejor aún si lo registra como ADR.
- **max_len<=0 → devolver "" en vez de ValueError:** válido si está acordado en el spec (no si "se
  asume").
- **Más de un ADR** (p. ej. uno para la elipsis y otro para el corte por palabra): excelente, demuestra
  que distingue decisiones independientes.
- Lo que **no** es aceptable: spec que repite el issue sin bordes; ADR sin alternativas; entregar la
  implementación de la función en vez de los artefactos.
