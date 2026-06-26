# Ejercicio 2.4 — El juicio: ¿abstraer o no?

> **Modalidad: razonamiento/diseño (sin IA primero).** Este ejercicio no se corrige con tests verdes: se
> corrige con la **calidad de tus argumentos**. Es la mitad de SOLID que el mercado paga y que ninguna IA
> tiene por ti: decidir **cuándo aplicar un principio es ingeniería y cuándo es sobre-ingeniería**, y
> defenderlo como en un code review.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.4` SOLID con crítica
**Ruta:** crítica · **Timebox:** 25–35 min

## 🎯 Objetivo

Evaluar el **trade-off** entre aplicar un principio SOLID y caer en sobre-abstracción (YAGNI), decidiendo
para tres escenarios reales si abstraes o no, y **defendiendo cada decisión** nombrando el smell presente o
ausente, un principio a favor, un argumento en contra y —si dejas algo concreto— el gatillo que te haría
cambiar de opinión.

## 📋 Contexto

La marca del semi-senior no es recitar los cinco principios: es decidir, con criterio, dónde NO aplicarlos.
"El smell justifica el principio, no al revés". En el Capstone F2 documentarás en un ADR dónde decidiste **no**
abstraer y por qué; este ejercicio es el ensayo de ese músculo.

## 📏 Primero-Sin-IA

1. Resuelve los tres escenarios **solo**, a mano, dentro del timebox. Decide tú; defiende tú.
2. Solo entonces relee la sección 5 de la lección (la crítica) y ajusta.
3. **Solo al final**, usa IA para *cuestionar* tus argumentos —no para escribirlos.
4. Mañana, vuelve a un escenario y mira si defenderías lo mismo.

## 🛠️ Los tres escenarios

Sin escribir código de producción. Para cada uno, decide **aplicar el principio** o **NO aplicarlo (YAGNI)**.

1. **El reporte que solo exporta a PDF.** Una función `exportar(reporte)` que hoy genera PDF. El PM dice
   "quizás algún día agreguemos Excel, no sé". ¿Creas ya una abstracción `Exportador` (OCP/DIP) o dejas la
   función concreta?
2. **El cliente de pagos.** Tu `ServicioCheckout` instancia `StripeCliente()` por dentro. Necesitas testear el
   checkout sin cobrar tarjetas reales, y el negocio evalúa agregar un segundo proveedor el próximo trimestre.
   ¿Inviertes la dependencia (DIP) o lo dejas concreto?
3. **La clase `Usuario`.** Tiene `nombre`, `email`, y métodos `validar_email()` y `nombre_completo()`. Un colega
   dice "viola SRP, hay que separar la validación en una clase aparte". ¿Lo separas o no?

## ✍️ Qué entregar

Crea `decisiones.md` en esta carpeta. Para **cada** escenario, escribe:

- **(a) Decisión:** abstraigo / no abstraigo (sé concreto sobre qué).
- **(b) Smell:** el smell concreto **presente** que la justifica —o la **ausencia de smell** como razón para no
  abstraer.
- **(c) Trade-off:** un principio **a favor** y un argumento **en contra** (YAGNI / Rule of Three / costo de
  indirección / testabilidad).
- **(d) Gatillo:** si dejas algo sin abstraer, el evento observable que te haría refactorizar ("si pasa X,
  abstraigo").

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios resueltos con los cuatro puntos (a–d).
- [ ] Cada decisión nombra el smell **presente o ausente** (la ausencia de smell es una razón válida para NO
      abstraer).
- [ ] Cada decisión expone un argumento a favor **y** uno en contra (no hay decisión sin trade-off).
- [ ] Las decisiones de "no abstraer" incluyen un **gatillo** concreto y observable.
- [ ] Puedes **defender en voz alta** cualquiera de las tres como en un code review.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No hay respuesta "correcta" universal, pero sí decisiones mejor y peor defendidas. Dirección, no respuesta: el
escenario 2 tiene **dos** fuerzas empujando a abstraer (testabilidad *hoy* + segundo proveedor *probable*);
contrasta eso con el escenario 1, donde el "quizás algún día" es pura especulación (speculative generality). El
escenario 3 es una trampa de SRP dogmático: pregúntate si `validar_email` y `nombre_completo` cambian por
**razones distintas** o son la misma cohesión de "qué es un usuario". Distinguir un eje de variación **real y
presente** de uno **especulado** es todo el ejercicio. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `decisiones.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/solid-juicio-sobre-abstraccion.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/solid-juicio-sobre-abstraccion.md` — no la mires
antes de intentarlo de verdad. El corrector evalúa la **calidad de tu razonamiento**, no si coincidiste con un
bando.
