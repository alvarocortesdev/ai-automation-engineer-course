# Ejercicio T0.5 — Del "hice X" al "X redujo Y" + write-up de trade-offs

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** El write-up de trade-offs es el
> no-negociable que casi nadie tiene —y por eso es tu mayor diferenciador. Este ejercicio entrena dos
> músculos: articular **decisiones de diseño** (qué elegiste, qué descartaste y por qué) y traducir
> descripciones de tarea ("hice X") a **lenguaje de impacto** ("X redujo Y") con métricas honestas.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.5` Portafolio diferenciado
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O2** — Articular un proyecto con el write-up de trade-offs y mapear sus decisiones a hilos de
  producción (seguridad/HITL, costo-latencia, observabilidad).
- **O3** — Traducir "hice X" a "X redujo Y" con la fórmula acción + métrica + resultado, sin inflar números.

## Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 40 min). No le pidas a la IA que escriba el write-up por ti.
2. Solo entonces relee la sección "lenguaje de impacto" y el worked example de la lección si dudaste.
3. **Solo al final**, usa IA para *revisar* tu articulación —no para generarla.
4. Mañana, reescribe un bullet de impacto de memoria. Si no te sale la fórmula sin notas, repásalo.

## El proyecto a articular

Toma **un** proyecto: idealmente el más fuerte que ya tengas. Si todavía no construiste el capstone, usa
el **brief del capstone agéntico de F7** que está en `brief.md` (un sistema que recibe tickets de soporte,
los clasifica con IA, valida la salida y ejecuta una acción). Elige uno y trabaja sobre él.

## Tu tarea (en este orden)

En `articulacion.md`, tres partes:

1. **Write-up de trade-offs** — al menos **dos** decisiones de diseño reales. Cada una con el formato
   **decisión → alternativa que descartaste → por qué**. Al menos una debe tocar un hilo de producción
   (seguridad/HITL, costo-latencia, u observabilidad). Molde: "Elegí validar la salida antes de ejecutar
   (descarté el agente autónomo) porque una acción errónea cuesta más que la latencia de validar".
2. **Tres bullets de impacto** — reescribe tres descripciones de tarea ("hice X") a lenguaje de impacto
   ("X redujo/subió Y") con la fórmula **acción + métrica + resultado**. Marca cada número como **medido**
   o **estimado**. Nada inventado.
3. **Checklist de los tres no-negociables** — para ese proyecto, declara el estado de cada uno:
   - ¿la demo **CORRE** (link vivo o video real, no screenshot)?
   - ¿el README está/estaría en **inglés**?
   - ¿este **write-up** existe?
   Si alguno falta, escribe la **acción concreta** para cerrarlo.

## Qué entregar (deja este archivo en esta carpeta)

- `articulacion.md` — el write-up de trade-offs, los 3 bullets de impacto y el checklist de no-negociables.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **≥2 decisiones** con su alternativa descartada y un "por qué" defendible.
- [ ] **≥1 decisión** toca un hilo de producción (seguridad/HITL, costo-latencia, observabilidad).
- [ ] **3 bullets de impacto** con la fórmula acción + métrica + resultado; cada número marcado como
      medido o estimado (**ninguno inflado**).
- [ ] **Checklist** de los tres no-negociables con estado real y acción de cierre para lo que falte.
- [ ] Puedes **defender cada decisión sin notas** (check de dominio).

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Una decisión de diseño no es "usé FastAPI" —eso es una elección sin alternativa visible. Una decisión es
un cruce donde había **al menos dos caminos razonables** y elegiste uno por una razón defendible. Para el
capstone agéntico, los cruces ricos están en producción: ¿el agente actúa solo o valida antes de ejecutar?
¿modelo caro siempre o ruteo por costo? ¿qué pasa si el LLM devuelve basura? Para los bullets de impacto,
si no tienes un número medido, **estímalo honestamente** ("de ~15 min a menos de 1 min, estimado") en vez
de inventar uno preciso que no puedas defender en la entrevista. Revisa el worked example de la lección.

</details>

## Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/writeup-impacto-tradeoffs.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/writeup-impacto-tradeoffs.md` — no la mires
antes de intentarlo. El corrector revisará si tus decisiones tienen **alternativa real y un porqué
defendible**, y si tus métricas son **honestas** (no que coincidan con un ejemplo).
