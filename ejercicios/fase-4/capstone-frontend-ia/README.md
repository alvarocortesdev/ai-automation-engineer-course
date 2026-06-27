# Capstone Fase 4 — Frontend de una app de IA

> **Modalidad: capstone (mixto — código + spec/ADR/README + infra).** Es el proyecto final de la Fase 4:
> un **frontend Next.js + TypeScript** sobre tu backend FastAPI de la Fase 3, con un chat de IA con
> streaming token por token, datos cacheados con TanStack Query, formularios validados con RHF + zod y
> Zustand para el client-state. No es un ejercicio con tests que ya están escritos: aquí decides la
> estructura, la frontera entre tipos de estado y cada decisión de UX, y luego la defiendes. Es la **cara
> visible** que la Fase 6 llenará con RAG y agentes reales.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.P` Capstone — Frontend de una app de IA
**Ruta:** crítica · **Timebox:** proyecto · 15–25 h repartidas en 1–2 semanas

## 🎯 Objetivo

Construir un frontend que cumpla el **Definition of Done** del curso para una UI: spec primero con inventario
de estados, App Router con separación Server/Client correcta, server-state en TanStack Query y formularios con
React Hook Form + zod, Zustand solo donde aplique, un chat de IA con streaming, **accesibilidad WCAG 2.2 y los
cuatro estados de primera clase como gate**, salida del LLM renderizada de forma segura, tests de componentes,
README en inglés y demo que corre. Al terminar puedes explicar y defender cada decisión sin notas.

## 📋 Contexto

Las once sub-unidades de la Fase 4 fueron piezas: HTML/CSS, Tailwind, diseño visual, a11y, React+TS, Next.js,
TanStack Query + RHF/zod, Zustand, design systems, estados de primera clase y UI de IA. Este capstone las
ensambla en **una** app coherente que consume tu [API de la Fase 3](../../fase-3/capstone-api-produccion/). Es
la cara de todo lo que construiste y de todo lo que viene: en la Fase 6 la lógica de RAG y agentes vivirá detrás
de este mismo frontend, sin que la UI cambie. Hacerlo bien una vez te ahorra reescribirlo —y es la primera pieza
"fullstack + IA" de tu portafolio.

## 📏 Primero-Sin-IA (el corazón de este capstone)

Este capstone es **repaso integrador**: ya conoces cada concepto, ahora los combinas. Por eso el Primero-Sin-IA
es de entrada (no hay worked example nuevo que copiar), con andamiaje en el *proceso*, no en el código.

1. **Piensa tú las fronteras.** La frontera server/client/chat-state, el inventario de estados de cada vista y
   las decisiones de a11y las razonas a mano, sin IA. Es la parte que más se aprende pensándola.
2. Consulta **documentación oficial** (Next.js, TanStack Query, RHF, zod, Vercel AI SDK, WCAG 2.2) cuando lo
   necesites.
3. **Solo al final**, si quieres, usa IA para *revisar y explicar* lo que ya construiste —nunca para *generar la
   arquitectura ni la frontera de estado*. Pegar una app completa de un chat es saltarse el capstone entero.
4. **Mañana**, reescribe tu inventario de estados de memoria. Si no puedes, no internalizaste tu propio diseño.

> "Sin IA para razonar" = no le delegas el diseño, la frontera de estado ni las decisiones de UX/a11y. Usar docs
> oficiales y autocompletado básico está bien. Si quitarte el chat te deja sin saber dónde poner cada dato, ese
> vacío es justo lo que el capstone vino a llenar.

## 🛠️ El brief

Construye un frontend de **producción** sobre tu API de la Fase 3. Recomendado (y pensado para que la Fase 6 lo
convierta en RAG sin reescribir): la cara de tu **base de conocimiento de documentos** —login, gestión de
colecciones/documentos, y un chat que responde preguntas con streaming.

### Las tres superficies que el capstone exige (sí o sí)

1. **Datos del servidor** (lista que se lee y se muta) → superficie de **server-state** (TanStack Query + los
   cuatro estados). Ej.: lista de `colecciones`, crear/borrar.
2. **Un chat de IA con streaming** → superficie de **UI de IA** (optimistic UI, streaming, seis estados,
   seguridad). Ej.: "pregunta sobre tus documentos".
3. **Al menos un formulario validado** → superficie de **RHF + zod**. Ej.: login, crear colección.

### Requisitos mínimos (lo que se evalúa)

- **Stack:** Next.js (App Router) + TypeScript + Tailwind. Separación correcta Server/Client Components
  (interactivo = `"use client"`; solo-presentación = Server Component cuando se pueda).
- **Server-state:** **TanStack Query** (`useQuery`/`useMutation`) para leer y mutar datos de tu API F3, con
  **invalidación** tras mutar. Prohibido server-state en Zustand o en `useEffect` + `useState` a mano.
- **Formularios:** **React Hook Form + zod**; el schema de zod es la validación (no validar a mano en el submit).
- **Client-state:** **Zustand** solo donde aplique (tema, sidebar, colección activa, toasts). Si no lo necesitas,
  no lo metas (YAGNI).
- **Chat de IA con streaming:** `useChat` de `@ai-sdk/react` + un Route Handler con `streamText`; optimistic UI,
  mensaje de asistente que crece chunk por chunk, estados pensando/streaming/error/cancelar.
- **GATE — estados de primera clase:** **cada vista con datos dibuja empty/loading/error/success** (loading =
  skeleton, no spinner mudo; error = mensaje accionable + reintentar; vacío = call-to-action). El chat dibuja sus
  seis estados (vacío/enviando/streaming/completado/error/cancelado).
- **GATE — accesibilidad WCAG 2.2:** operable solo con teclado; foco visible y manejado (el modal atrapa y
  devuelve el foco); contraste suficiente; `aria-live` que anuncia el texto del chat que llega en vivo; landmarks
  y headings con jerarquía.
- **Seguridad:** la salida del LLM se renderiza como **texto** (o markdown con renderer que sanitiza y prohíbe
  HTML crudo), **nunca** con `dangerouslySetInnerHTML`; secretos/URLs en variables de entorno (la API key del
  modelo es server-only, jamás `NEXT_PUBLIC_`); CORS acotado en el backend (no `*`).
- **Calidad:** tests (componentes + máquina de estados del chat) con **Vitest + Testing Library** y un chequeo de
  a11y con **axe**; lint (ESLint) en CI.
- **Observabilidad:** registra **latencia y tokens por respuesta** del chat (consola/log) — semilla del
  costo/latencia que la Fase 6 formaliza.
- **Comunicación:** README **en inglés** con `pnpm dev`/`pnpm build` y una demo que corre (capturas o GIF);
  write-up de trade-offs; historial 100% **Conventional Commits**.

## ✅ Criterios de "hecho" (Definition of Done — Fase 4)

Este capstone se mide contra el **Definition of Done único** del curso. En la Fase 4 aplican estos puntos (el 5
—eval de IA— y el 6 —agente— se siembran y se exigen en F6):

- [ ] **(DoD 1)** `SPEC.md` existe y se escribió **antes** que el código (su commit precede al primer
  componente), con el **inventario de estados** de cada vista, más al menos un **ADR** real (frontera
  server/client/chat-state, o dónde vive la IA hoy y en F6).
- [ ] **(DoD 2)** Tests verdes + lint en CI; hay tests de componentes (los cuatro estados de una lista) y de la
  máquina de estados del chat. No "se ve bien en mi pantalla".
- [ ] **(DoD 3)** Seguridad aplicada: salida del LLM como texto (sin `dangerouslySetInnerHTML`, test que lo
  prueba); secretos en env (API key server-only); CORS acotado en el backend.
- [ ] **(DoD 4)** Observabilidad: latencia/tokens por respuesta del chat registrados (se ve en la demo o el log).
- [ ] **(DoD 7)** **a11y WCAG 2.2**: navegable solo con teclado, foco manejado en el modal, contraste suficiente,
  `aria-live` en el chat; y los **cuatro estados** en cada vista con datos. **Este es el gate de la fase.**
- [ ] **(DoD 8)** La app **corre** (`pnpm dev`) y hace lo que el README promete (demo con capturas/GIF); README
  **en inglés**; write-up de trade-offs (qué dejaste fuera y por qué, qué fue lo más difícil).
- [ ] **(DoD 9)** Todo el historial usa **Conventional Commits**.
- [ ] **(Gate Primero-Sin-IA)** Diseñaste la frontera de estado y los estados de cada vista sin delegar el
  pensamiento a una IA; puedes explicar **cada decisión sin notas**.

## 📂 Estructura sugerida del entregable

```text
mi-frontend/
├── SPEC.md                  ← copia plantillas/SPEC.md; escríbela PRIMERO (incluye inventario de estados)
├── README.md                ← en inglés: qué es, pnpm dev, demo que corre, trade-offs
├── package.json             ← copia plantillas/package.json (deps con pnpm)
├── .env.local.example       ← copia plantillas/.env.local.example; el .env.local real va gitignored
├── docs/
│   └── ADR-0001-*.md        ← copia plantillas/ADR-0001-frontera-estado.md
├── src/
│   ├── app/
│   │   ├── layout.tsx        ← Server Component: html/body + <Providers>
│   │   ├── providers.tsx     ← "use client": QueryClientProvider (+ tema)
│   │   ├── page.tsx          ← lista de colecciones (los 4 estados)
│   │   ├── chat/page.tsx     ← vista de chat (streaming, 6 estados)
│   │   └── api/chat/route.ts ← Route Handler con streamText (BFF del chat)
│   ├── lib/                  ← cliente de tu API F3 + store de Zustand
│   └── components/           ← ColeccionesList, Chat, EstadoVacio, Skeleton, ErrorState...
├── tests/                   ← Vitest + Testing Library + chequeo axe (ver tests/ aquí como guía)
└── .github/workflows/ci.yml ← lint + test
```

## 🧭 Orden recomendado de construcción (la disciplina ES el orden)

1. **Decide la frontera de estado** (server/client/chat) y dónde vive la IA. 2. **Escribe `SPEC.md`** con el
inventario de estados de cada vista (antes del código). 3. **Escribe el ADR**. 4. **Scaffold + providers**
(QueryClientProvider, Zustand, Tailwind). 5. **Construye por capas verticales:** auth (RHF+zod) → colecciones
(useQuery con sus 4 estados + useMutation con invalidación) → chat (streaming, 6 estados) → gate (a11y + tests +
seguridad). Una feature completa, accesible y con sus estados antes de la siguiente; nunca todos los componentes
primero y los datos después.

> El error #1 es empezar por los componentes y dejar la frontera de estado y los estados "para después". El error
> #2 es dibujar solo el happy path y meter la a11y al final (el gate falla). Verticaliza y teje el gate desde la
> primera feature.

## 💡 Pista (ábrela solo si te trabas con el arranque)

<details>
<summary>Mostrar pista</summary>

Si te paralizas, casi siempre saltaste la frontera de estado o intentas todo a la vez. Vuelve a lo mínimo que
corre: el `providers.tsx` con `QueryClientProvider`, y una página que liste colecciones con `useQuery` dibujando
los cuatro estados (`isPending` → skeleton, `isError` → error + reintentar, `data.length === 0` → vacío, datos →
lista). Esa sola vista, accesible y con sus cuatro caras, te da el patrón de todas las demás. Para el chat, reusa
la máquina de estados del ejercicio `chat-reducer-streaming`. La regla mental de la frontera: "¿la fuente de
verdad de este dato está en mi servidor?" → TanStack Query; "¿es puro estado de UI del cliente?" → Zustand. Esto
es una pista del *proceso*; la frontera y los estados los diseñas tú.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu proyecto completo (este directorio o tu repo), la **rúbrica**
(`.ai/rubricas/fase-4/capstone-frontend-ia.md`) y `.ai/INSTRUCCIONES-CORRECTOR.md`. Pídele:

> "Corrige mi capstone `ejercicios/fase-4/capstone-frontend-ia/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

La **solución de referencia** (un proyecto ejemplar) vive en `.ai/soluciones/fase-4/capstone-frontend-ia/` — es
material del corrector; no la mires antes de cerrar tu intento. En un capstone de diseño **no hay una única
respuesta correcta**: el corrector evalúa tu frontera de estado, tus estados de primera clase, tu accesibilidad y
si puedes defender tus decisiones, no si elegiste "el" layout.
