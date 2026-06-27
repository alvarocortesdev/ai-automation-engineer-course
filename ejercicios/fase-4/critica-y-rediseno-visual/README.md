# Ejercicio 4.3 — Crítica de diseño: nombra la heurística, no el gusto

> **Modalidad: a mano (razonamiento/diseño, sin código).** No vas a rediseñar en CSS: vas a
> **diagnosticar** una pantalla por escrito, nombrando la palanca y la heurística exacta que viola cada
> problema. Es el músculo que te hace buen revisor en code review y buen cliente de la IA.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.3` Fundamentos de diseño visual
**Ruta:** crítica · **Timebox:** 25–30 min

## 🎯 Objetivo

- **O1** — Diagnosticar una interfaz nombrando, por cada problema, la **palanca** (jerarquía, layout/
  alineación, tipografía, espaciado, color) y la **heurística concreta** que viola (proximidad, contraste
  AA, escala, alineación, longitud de línea, 60-30-10…). No vale "se ve feo".
- **O2** — Proponer una **corrección accionable** por problema (qué cambiarías, con un valor o regla).
- **O3** — **Priorizar**: si solo pudieras arreglar tres cosas, cuáles y por qué (por impacto en
  legibilidad y accesibilidad).

## 📋 Contexto

La pantalla a criticar está descrita en detalle en `pantalla-a-criticar.md` (con valores concretos:
tamaños, colores, espacios). Diagnosticarla con precisión es exactamente lo que harás cuando revises el
PR de un compañero o cuando le pidas a una IA "mejora esta UI": si no nombras el problema, no puedes
evaluar la solución.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba), con la checklist de las cinco palancas al lado.
2. Documentación oficial permitida (WCAG, MDN) para verificar umbrales de contraste.
3. **Solo al final**, usa IA para *contrastar* tu diagnóstico — no para *generarlo*.
4. Mañana, mira una interfaz que uses a diario y repite el diagnóstico de memoria.

## 🛠️ Instrucciones

1. Lee `pantalla-a-criticar.md`.
2. Recorre la pantalla con la **checklist de las cinco palancas**, una por una. Por cada problema que
   encuentres, escribe en `critica.md` una entrada con esta forma:

   ```text
   - Problema: <qué está mal, concreto>
     Palanca: <jerarquía | layout/alineación | tipografía | espaciado | color>
     Heurística violada: <nombre exacto, p. ej. "ley de proximidad" / "contraste AA 4.5:1">
     Corrección: <qué cambiarías, con un valor o regla concreta>
   ```

3. Al final de `critica.md`, agrega un **top-3 priorizado**: las tres correcciones de mayor impacto,
   cada una con una frase de por qué va primero.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Identificaste **al menos cinco** problemas distintos, cada uno atado a **una de las cinco
      palancas** (y entre todos cubres las cinco).
- [ ] Cada problema nombra la **heurística concreta** que viola (no un juicio de gusto).
- [ ] Cada problema trae una **corrección accionable** con valor o regla.
- [ ] El **top-3 priorizado** está justificado por impacto (legibilidad/accesibilidad), no por orden de
      aparición.
- [ ] Puedes **defender tu diagnóstico sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No mires la pantalla "en general": pregúntate por **cada** palanca "¿se respeta aquí?". Para el contraste,
calcula o verifica los pares grises sobre blanco (un gris claro como `#c4c4c4` no pasa AA). Para priorizar,
pondera dos ejes: cuánto rompe la **jerarquía/legibilidad** (¿sé qué leer y qué hacer primero?) y cuánto
rompe la **accesibilidad** (¿pasa el contraste? ¿la información depende solo del color?). Lo que falla
ambos ejes va primero. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `critica.md`,
- la **rúbrica**: `.ai/rubricas/fase-4/critica-y-rediseno-visual.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-4/critica-y-rediseno-visual.md` — no la mires
antes de intentarlo de verdad.
