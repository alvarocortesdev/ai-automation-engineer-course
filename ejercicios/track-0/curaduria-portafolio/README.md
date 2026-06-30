# Ejercicio T0.5 — Cura el portafolio: mata el 80% idéntico

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** Un portafolio fuerte no se mide por
> cuántos repos tiene, sino por la **señal** que envía en los diez segundos que un reclutador le dedica.
> Este ejercicio entrena la disciplina que casi nadie practica: **curar** —decidir qué se muestra y, sobre
> todo, qué se esconde— para que tus 2-3 mejores proyectos no queden enterrados bajo el ruido de tutoriales.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.5` Portafolio diferenciado
**Ruta:** crítica · **Timebox:** 35 min

## Objetivos

- **O1** — Curar un portafolio: seleccionar 2-3 proyectos profundos, justificar por qué baten a los
  tutoriales clonados, identificar el patrón del "80% idéntico" y defender por qué el capstone agéntico es
  la estrella por encima del RAG-sobre-docs genérico.
- **O2** — Mapear cada proyecto sobreviviente a una *skill* concreta que un hiring manager pediría.

## Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 35 min). No le pidas a la IA que clasifique los repos por ti.
2. Solo entonces relee la sección "El reencuadre: cura, no acumules" de la lección si dudaste.
3. **Solo al final**, usa IA para *revisar* tu curaduría —no para generarla.
4. Mañana, vuelve a elegir la estrella de memoria y justifícala. Si no puedes sin notas, repásalo.

## El portafolio a curar

Trabaja sobre estos **nueve repos** de un candidato ficticio (también están en `repos.md`, donde dejarás
tu trabajo). El candidato postula a roles de **AI/Automation Engineer**.

1. **`todo-app-react`** — app de tareas de un tutorial de YouTube. README de plantilla, en español.
2. **`weather-dashboard`** — consume una API de clima; clon de un curso de Udemy.
3. **`100-days-of-code`** — carpeta con 100 mini-scripts de un challenge.
4. **`ticket-triage-agent`** — sistema propio: recibe tickets de soporte, los clasifica con un LLM, valida
   la salida, pide confirmación humana para acciones sensibles y ejecuta la acción. Tiene tests y un video
   de demo. README en inglés.
5. **`pdf-chatbot`** — "chatea con tu PDF": RAG básico copiado de un tutorial. Sin eval, sin reranking.
   README de plantilla.
6. **`rag-knowledge-platform`** — plataforma RAG propia: ingest, vector DB, retrieval con reranking,
   evaluación con ragas y observabilidad. Desplegada. README en inglés.
7. **`nextjs-starter-fork`** — fork de un starter de Next.js que tocó dos días; sin cambios reales.
8. **`homebase`** — app fullstack propia (TS, Next.js, tests, CI/CD, estados completos). En uso real.
9. **`crypto-price-tracker`** — script que imprime precios de cripto; ejemplo de un tutorial.

## Tu tarea (en este orden)

En `curaduria.md`:

1. **Clasifica** cada uno de los 9 repos como **señal** (evidencia de que construye) o **ruido**
   (tutorial / experimento a medias), con **una línea** de justificación por cada uno.
2. **Selecciona los 2-3** que quedan en la vitrina; di explícitamente cuáles **archivas/escondes** y por
   qué (curar es decir que no).
3. **Elige la estrella** (pin #1) y **justifica** por qué encabeza el portafolio. Defiende por qué el
   capstone agéntico va por encima del RAG genérico.
4. **Mapea** cada proyecto sobreviviente a **una *skill* concreta** que un hiring manager pediría (no
   "Python" en abstracto).
5. En 2-3 frases, **nombra el patrón del "80% idéntico"**: ¿qué comparten los repos que descartaste y por
   qué hacen invisible a un candidato?

## Qué entregar (deja este archivo en esta carpeta)

- `curaduria.md` — la clasificación de los 9, la selección, la estrella justificada, el mapeo a skills y la
  reflexión sobre el "80% idéntico".

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los **9 repos** clasificados como señal o ruido, con justificación.
- [ ] **2-3** elegidos para la vitrina; el resto archivado **explícitamente**.
- [ ] La **estrella** elegida y defendida (con el argumento agéntico-vs-RAG).
- [ ] Cada sobreviviente **mapeado a una skill** del mercado (concreta, no genérica).
- [ ] El patrón del **"80% idéntico"** nombrado en tus palabras.
- [ ] Puedes **explicar tu curaduría sin notas** (check de dominio).

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Hay un repo trampa: uno que tiene "IA" en el nombre y *parece* señal, pero es ruido (un RAG-sobre-PDF de
tutorial, el "hola mundo" de la IA que el reclutador ya vio mil veces). No basta con que un proyecto sea
"de IA" para que diferencie. Pregúntate, repo por repo: ¿esto demuestra **juicio propio** o solo que seguí
un tutorial? ¿Lo tiene cualquiera, o es difícil de fakear? Para la estrella, piensa cuál demuestra que tu
sistema **decide y actúa** y que sabes **qué hacer cuando falla** —eso es lo que el RAG genérico no puede
mostrar. Revisa la jerarquía de proyectos de la lección.

</details>

## Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/curaduria-portafolio.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/curaduria-portafolio.md` — no la mires antes
de intentarlo. El corrector revisará tu **criterio de curaduría** (sobre todo el repo trampa y la defensa
de la estrella), no que tu selección coincida palabra por palabra con un ejemplo.
