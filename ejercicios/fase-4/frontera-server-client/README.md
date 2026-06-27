# Ejercicio 4.6 B — Decide la frontera servidor/cliente y el modo de render

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.6` Next.js
**Ruta:** crítica · **Modalidad:** a mano (razonamiento y diseño) · **Timebox:** 35 min

> Este ejercicio **no tiene código que ejecutar**. Es una revisión de arquitectura, como las que harás en una entrevista de system design o al planificar una feature. Entrena el juicio que separa al que "hizo el tutorial" del semi-senior: **decidir dónde corre cada cosa**.

## 🎯 Objetivo

Para una página de catálogo de modelos de IA con 7 piezas, decidir qué es cada una —**Server Component**, **Client Component**, **Route Handler** o **Server Action**—, dónde cae la frontera `'use client'`, y qué **modo de render** (estático / ISR / dinámico) le corresponde a la página, **justificando el trade-off**.

## 🧩 La página a diseñar

Una página `/modelos` que muestra el catálogo de modelos de IA. Tiene estas 7 piezas:

1. La **lista de modelos** cargada desde la base de datos al abrir la página.
2. La **caja de búsqueda** que filtra la lista ya cargada, en vivo, mientras el usuario teclea.
3. El **botón de tema** claro/oscuro, que lee y escribe la preferencia en `localStorage`.
4. El botón **"marcar favorito"** que guarda el favorito del usuario en la base de datos.
5. Un **autocompletado** que, al teclear, pide sugerencias al servidor contra un índice de búsqueda grande (no la lista en memoria).
6. El **layout** con el logo y la navegación (no cambia entre páginas).
7. Un **ping de analítica** que se dispara una sola vez cuando el usuario abre la página.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Decide con tu modelo mental, no con docs abiertas.
2. Solo entonces consulta la **documentación oficial**: <https://nextjs.org/docs/app/getting-started/server-and-client-components>.
3. **Solo al final**, usa IA para *revisar y discutir* tus decisiones —no para que las tome por ti.
4. Mañana, **reconstruye la tabla de memoria**. Si no puedes justificar cada celda, no lo aprendiste.

## 📝 Qué entregar (crea estos archivos en esta carpeta)

`decisiones.md` con:

1. Una **tabla** de las 7 piezas. Por cada una: la categoría elegida (Server Component / Client Component / Route Handler / Server Action) + **1-2 frases** de justificación (por qué servidor o por qué navegador).
2. Una frase indicando **en qué piezas** pondrías la directiva `'use client'` y **por qué no** en la página completa.
3. El **modo de render de la página** `/modelos` (estático / ISR / dinámico) con una justificación que mencione **frescura vs. costo/latencia**. Si crees que depende de algo, di **de qué** depende.
4. Una nota de **seguridad**: en qué pieza(s) la validación/autorización es obligatoria **en el servidor** y por qué no basta con validar en el cliente.

> No hay tests ni respuesta única cerrada: hay decisiones **defendibles** y decisiones **indefendibles**. El valor está en la **calidad y honestidad de tu razonamiento**, no en adivinar "la" respuesta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las 7 piezas clasificadas, cada una con justificación (no solo la etiqueta).
- [ ] Distingues correctamente **Route Handler** (datos bajo demanda a un cliente) de **Server Action** (mutación que la UI dispara).
- [ ] Distingues la **pieza 2** (filtra una lista ya cargada → cliente) de la **pieza 5** (pide al servidor → necesita endpoint).
- [ ] Dices explícitamente dónde va `'use client'` y por qué **no** en la raíz.
- [ ] Eliges un modo de render y **defiendes el trade-off** (no solo "uso ISR").
- [ ] Identificas dónde la validación/autorización debe vivir en el servidor.
- [ ] Puedes **explicar sin notas** por qué un secreto leído en un Client Component se filtra.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Pregúntate por cada pieza, en este orden:
1. ¿Necesita **interactividad o APIs del navegador** (estado, eventos, `localStorage`)? → Client Component.
2. ¿Solo **lee datos y arma HTML**, sin interacción? → Server Component.
3. ¿**Muta datos** que la propia UI dispara (un favorito)? → Server Action.
4. ¿Expone datos **bajo demanda a un cliente** (autocompletar contra un índice grande)? → Route Handler.

La pieza 2 y la 5 parecen iguales pero no lo son: una filtra una lista que **ya tienes** en memoria (cliente, sin servidor), la otra **pide** al servidor cada vez. Para el modo de render pregúntate: ¿los datos son **por usuario**? (apunta a dinámico) ¿cada cuánto cambian? (estable → estático/ISR). Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/frontera-server-client/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/frontera-server-client.md` — no la mires antes de intentarlo de verdad.
