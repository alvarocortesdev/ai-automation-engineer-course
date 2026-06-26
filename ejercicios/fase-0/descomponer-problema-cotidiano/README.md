# Ejercicio 0.2 — Descompón un problema cotidiano con las 4 herramientas

> **Modalidad: a mano (sin código, sin IA).** Este ejercicio entrena el músculo *anterior* a programar: atacar un problema confuso con las cuatro herramientas del pensamiento computacional. No se escribe código. Se piensa.

## Objetivos

- **O1** — Descomponer un problema cotidiano en subproblemas pequeños e independientes, y **nombrar las dependencias** entre ellos.
- **O2** — Identificar al menos un **patrón** repetido y **abstraer** explícitamente qué detalles se ignoran y por qué.
- **O3** — Diseñar un **algoritmo** en pasos numerados, sin ambigüedad, que incluya **al menos dos casos borde**.

## El problema

Elige **uno** de estos tres (de preferencia el que menos hayas pensado en tu vida):

1. **Organizar una mudanza** de un departamento a otro.
2. **Preparar y enviar las 30 invitaciones** de un cumpleaños.
3. **Decidir el menú de almuerzos** de una semana completa para dos personas.

> Son cotidianos a propósito: el objetivo es que veas las cuatro herramientas *sin* que la sintaxis te distraiga. El mismo razonamiento aplicará idéntico cuando el problema sea código.

## Tu tarea (en este orden — Primero-Sin-IA, timebox 35 min)

Trabaja **a mano** (papel o `.md`), sin IA. Aplica las cuatro lentes:

1. **Descomposición.** Parte el problema en 4–7 subproblemas. Dibuja un árbol o una lista jerárquica. **Marca las dependencias**: "B no puede empezar hasta que A esté listo".
2. **Reconocimiento de patrones.** Identifica al menos **un patrón**: algo que se repite (un "haz esto para cada…") o que se parece a un problema que ya conoces. Explícalo en una frase.
3. **Abstracción.** Escribe qué detalles **decides ignorar** y *por qué* no afectan al resultado. Mínimo tres detalles ignorados.
4. **Diseño de algoritmo.** Escribe la solución en **pasos numerados**, sin ambigüedad, en lenguaje natural o pseudocódigo. Incluye **al menos dos casos borde** (qué pasa si algo sale raro: una caja se rompe, un invitado no responde, falta un ingrediente).

## Qué entregar

Completa la plantilla `PLANTILLA-RESPUESTA.md` (en esta carpeta) con tus cuatro secciones, o crea tus propios archivos:

- `descomposicion.md` — el árbol/lista con dependencias.
- `patrones-y-abstraccion.md` — el patrón identificado + los detalles ignorados con su justificación.
- `algoritmo.md` — los pasos numerados + los dos casos borde.

> No hay tests automáticos: esto es razonamiento. Tu propia honestidad es el primer corrector; la IA es el segundo.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El problema está partido en 4–7 subproblemas con **al menos una dependencia** explícita.
- [ ] Hay **un patrón** nombrado y explicado.
- [ ] Hay **3+ detalles ignorados** con su porqué (abstracción consciente, no por olvido).
- [ ] El algoritmo está en pasos numerados **sin ambigüedad** y cubre **2 casos borde**.
- [ ] Puedes **defender** cada decisión sin notas (check de dominio).

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/descomponer-problema-cotidiano/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿las dependencias son reales? ¿la abstracción es consciente o es olvido? ¿los casos borde son los que de verdad rompen?), no si tu redacción es bonita. La **solución de referencia** vive en `.ai/soluciones/` — no la mires antes de intentarlo de verdad.
