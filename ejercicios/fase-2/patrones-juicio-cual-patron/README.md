# Ejercicio 2.5 — El juicio: ¿qué patrón, o ninguno?

> **Modalidad: a mano (razonamiento, sin IA primero).** No se escribe código de producción. Este ejercicio
> entrena la mitad de los patrones que el mercado de verdad paga: **reconocer qué patrón convoca un smell —y
> saber cuándo NINGUNO aplica (pattern-itis / YAGNI)**. Una IA escribe la `AbstractFactory`; el juicio de no
> escribirla es tuyo.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.5` Patrones de diseño esenciales
**Ruta:** profundización · **Timebox:** 25–35 min

## 🎯 Objetivo

Para cuatro escenarios, decidir **qué patrón aplica** (Strategy / Factory / Repository / Adapter / Observer) o
**NINGUNO (YAGNI)**, y defender la decisión por escrito nombrando el smell presente o ausente, una fuerza a favor,
un argumento en contra, y —si decides no abstraer— el gatillo que te haría cambiar de opinión.

## 📋 Los cuatro escenarios

1. **El exportador de un solo formato.** Una función `exportar(reporte)` que hoy genera PDF y solo PDF. El PM
   dice "quizás algún día Excel, no sé". ¿Metes Strategy + Factory ahora, o dejas la función concreta?
2. **El cliente de LLM que llamas en 8 sitios.** Tu negocio llama directo al SDK de un proveedor en ocho
   lugares; el equipo evalúa migrar a otro proveedor el próximo trimestre y además necesitas testear sin gastar
   tokens. ¿Adapter, o lo dejas directo?
3. **`confirmar_pedido` que hace exactamente dos cosas.** Hoy guarda el pedido y manda un email, y no hay
   ninguna reacción más prevista. Un colega dice "métele un Observer para desacoplar". ¿Lo haces o no?
4. **El acceso a la tabla `users`.** Tres funciones distintas repiten SQL crudo contra `users`, y vienen más
   queries en el roadmap; además quieres testear la lógica de negocio sin levantar Postgres. ¿Repository o SQL
   directo?

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). El punto es *decidir y defender*, no acertar la "respuesta".
2. Solo entonces consulta la lección (`2.5`, secciones 4 y 5) para contrastar tu razonamiento.
3. **Solo al final**, usa IA para *cuestionar* tus argumentos —no para que decida por ti.
4. Mañana, vuelve a defender una decisión **de memoria**, en voz alta. Si no puedes, no la entendiste.

## 🛠️ Entregable

Crea `decisiones.md` en esta carpeta. Para **cada** uno de los cuatro escenarios, escribe:

- **(a) Decisión:** el patrón que aplicas, o "ninguno (YAGNI)".
- **(b) Smell:** el smell concreto **presente o ausente** que la justifica (la ausencia de smell es razón válida
  para NO aplicar un patrón).
- **(c) Trade-off:** una fuerza **a favor** y un argumento **en contra** (Rule of Three / costo de indirección /
  control de flujo invisible / acoplamiento a un tercero).
- **(d) Gatillo:** si decides NO aplicar el patrón, el evento observable que te haría cambiar de opinión
  ("si pasa X, refactorizo").

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los cuatro escenarios resueltos, cada uno con (a)(b)(c)(d).
- [ ] Cada decisión nombra el smell **presente o ausente**; ninguna decisión queda sin trade-off explícito.
- [ ] Las decisiones de "ninguno" incluyen un **gatillo** concreto y observable.
- [ ] Distingues los escenarios con **una sola fuerza especulativa** (1, 3) de los que tienen **dos fuerzas
      reales y presentes** (2, 4: testabilidad *hoy* + cambio *probable*), y lo dices explícitamente.
- [ ] Puedes **defender en voz alta** cualquiera de las cuatro como en un code review.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No hay respuesta universal, pero hay decisiones **mejor y peor defendidas**. Dirección, no respuesta: en 1 y 3
hay **una sola** fuerza, y es especulativa ("quizás algún día", "por si acaso") —pesan la Rule of Three y el costo
del control de flujo invisible (un Observer para dos reacciones fijas es pattern-itis). En 2 y 4 hay **dos**
fuerzas reales y presentes (testabilidad *hoy* + cambio *probable*), lo que inclina la balanza hacia abstraer.
Distinguir un eje de variación **real y presente** de uno **especulado** es todo el ejercicio. Revisa la
sección 5 de la lección. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `decisiones.md`,
- la **rúbrica**: `.ai/rubricas/fase-2/patrones-juicio-cual-patron.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/patrones-juicio-cual-patron.md` — no la mires antes
de intentarlo de verdad.
