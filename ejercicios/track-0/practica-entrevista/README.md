# T0.3 — Cadencia de entrevistas + banco STAR + autoevaluación de mock

> **Modalidad: mixto (diseño + grabación, sin tests automáticos).** Este ejercicio
> no se "corre": se _hace_. Produces la infraestructura de tu práctica de
> entrevistas y la pones a rodar una vez. La parte que más cuesta —escucharte
> grabado— es justo la que más te mejora.

**Fase:** Track-0 — Empleabilidad, marca e inglés · **Lección:** `T0.3` Práctica de entrevista con cadencia
**Ruta:** crítica · **Timebox:** 45 min (artefactos escritos; la grabación va aparte)

## 🎯 Objetivo

Diseñar e implementar una **cadencia semanal** de mock interviews (live coding
hablado, system design de RAG, behavioral STAR), arrancar un **banco de historias
STAR** reutilizables en inglés, y **autoevaluar** una grabación tuya con rúbrica.

## 📋 Contexto

En 2026 las empresas verifican tu _proceso de pensamiento_, no tu output (el
38,5% de los candidatos técnicos dio señales de hacer trampa con IA). El gate
real es **pensar en voz alta, defender trade-offs en inglés y grabarte para
mejorar**. Este ejercicio monta el sistema que entrena exactamente eso, y conecta
directo con tu portafolio (T0.5) y tu historia de falla en producción (T0.4):
cada capstone terminado son 2-3 historias STAR nuevas.

## 📏 Primero-Sin-IA

1. Escribe los tres artefactos **a mano, sin IA** (timebox 45 min para lo escrito).
2. Graba tu mock tú solo, en voz alta, **en inglés**, antes de pedir ayuda a nadie.
3. **Solo al final**, usa IA para que te _corrija_ con el framework de `.ai/` — no para que escriba tus historias.
4. Mañana, sin mirar, recita las 5 fases del system design de RAG y las 4 partes de STAR. Si no puedes, repásalo.

## 🛠️ Instrucciones

Completa los tres archivos starter de esta carpeta (ya traen la estructura y un
ejemplo ilustrativo que debes **reemplazar** por lo tuyo):

1. **`cadencia-entrevistas.md`** — tu plan semanal como una _spec_: día/hora fijos
   para los 3 formatos, herramientas, y tu regla (siempre inglés, siempre grabado,
   siempre autoevaluado el mismo día).
2. **`banco-star.md`** — **3 historias STAR** completas en inglés (semilla de las
   8-10), con S/T/A/R etiquetados, _Action_ dominante y _Result_ con número. Debajo
   de cada una, las preguntas behavioral que cubre (≥3 por historia).
3. **`autoevaluacion-mock.md`** — graba **un** mock (≥15 min, inglés, en voz alta,
   solo), escúchate y autoevalúate con la rúbrica. Anota 2 aciertos y **1 mejora
   concreta**.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La cadencia tiene día/hora **concretos** y cubre los 3 formatos.
- [ ] Las 3 historias STAR están en inglés, con las 4 partes, _Action_ dominante y _Result_ con número.
- [ ] Cada historia mapea a **≥3 preguntas** behavioral distintas.
- [ ] Grabaste y **te escuchaste**: la autoevaluación nombra 1 mejora accionable (no "hablar mejor").
- [ ] Al menos una historia **demuestra** un hábito de ingeniería (testing/idempotencia/observabilidad/seguridad) sin decirlo explícitamente.
- [ ] Puedes **explicar sin notas** por qué la práctica va por cadencia y no "cuando me sienta listo".

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No inventes historias épicas: las mejores salen de cosas pequeñas y reales (un
bug que perseguiste, un proceso lento que aceleraste). Haz una lista de 6-8
momentos y para cada uno pregúntate _¿cuál fue el número?_. Si no recuerdas el
impacto, esa historia es débil. El truco no es tener historias espectaculares;
es tenerlas **estructuradas y listas** para no improvisar. Para la grabación: no
busques que salga bien — busca _datos_ sobre cómo lo haces hoy.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: los 3 `.md`),
- la **rúbrica**: `.ai/rubricas/track-0/practica-entrevista.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

> "Corrige `ejercicios/track-0/practica-entrevista/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/track-0/practica-entrevista/`
— no la mires antes de intentarlo de verdad. El corrector revisará tu **proceso**
(¿están estructuradas? ¿hay número en el Result? ¿la autoevaluación es honesta y
accionable?), no si tus historias son "impresionantes".
