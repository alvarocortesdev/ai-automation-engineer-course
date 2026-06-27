---
ejercicio_id: fase-4/capstone-frontend-ia
fase: fase-4
sub_unidad: "4.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Capstone Fase 4: Frontend de una app de IA

## Aviso de uso para el corrector

Este capstone **no tiene una única respuesta correcta**: el alumno elige su layout, su diseño visual y su
estructura de carpetas. Lo de abajo es **un** proyecto ejemplar que alcanza el nivel `excelente` —una **vara de
medir**, no la solución a copiar—. **No exijas que el alumno haya hecho *este* layout ni *estos* nombres.**
Evalúa su entrega contra la rúbrica (`.ai/rubricas/fase-4/capstone-frontend-ia.md`) usando este ejemplo solo
para calibrar qué se ve como "producción usable y accesible".

> Lo esencial a verificar no es el layout, sino: **¿la spec con inventario de estados y el ADR de frontera
> llegaron antes del código? ¿el server-state vive en TanStack Query (no en Zustand)? ¿el chat hace streaming
> con optimistic UI? ¿la salida del LLM se renderiza como texto (no HTML)? ¿la app se navega completa con el
> teclado y los cuatro estados están dibujados? ¿la API key del modelo es server-only?** Un proyecto distinto
> que cumpla todo eso es igual de `excelente`.

> Las APIs de abajo se verificaron contra la documentación oficial vigente 2026 (AI SDK v5, TanStack Query v5).

---

## Proyecto ejemplar: `docubase-ui` (frontend de la base de conocimiento)

Login, lista de colecciones (CRUD), y un chat que responde preguntas con streaming. Consume la API `docubase`
de la Fase 3. Diseñado para que en F6 el Route Handler `/api/chat` se reemplace por el endpoint de streaming del
backend RAG sin tocar la UI.

### 1. `SPEC.md` (antes del código)

Pantallas (`/login`, `/`, `/chat`), tabla de rutas, **tabla de frontera de estado** (colecciones → TanStack
Query; mensajes → `useChat`; tema/sidebar → Zustand) y el **inventario de estados**: los cuatro de la lista
(empty/loading/error/success) y los seis del chat. Equivalente a `plantillas/SPEC.md` completada. La spec se lee
como la lista de tests.

### 2. ADR-0001 — frontera de estado y dónde vive la IA

Decisión: server-state en TanStack Query, chat-state en `useChat`, client-state en Zustand; la IA hoy en un
Route Handler con `streamText`. Alternativa descartada: todo en Zustand (server-state obsoleto). Consecuencia
clave: en F6 el Route Handler se reemplaza por el endpoint del backend; la UI no cambia. (Equivalente a
`plantillas/ADR-0001-frontera-estado.md`.)

### 3. Providers (un QueryClient por carga del cliente)

```tsx
// src/app/providers.tsx
"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient());
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
```

### 4. Lista de colecciones — los cuatro estados (la pieza que más se evalúa del gate)

```tsx
// src/components/ColeccionesList.tsx
"use client";
import { useQuery } from "@tanstack/react-query";
import { obtenerColecciones } from "../lib/api";

export function ColeccionesList() {
  const { data, isPending, isError, error, refetch } = useQuery({
    queryKey: ["colecciones"],
    queryFn: obtenerColecciones, // GET /colecciones a la API F3
  });

  if (isPending) return <SkeletonLista />;
  if (isError)
    return (
      <div role="alert">
        <p>{error.message /* viene del detail RFC 9457 del backend */}</p>
        <button onClick={() => refetch()}>Reintentar</button>
      </div>
    );
  if (data.length === 0)
    return (
      <div>
        <p>Aún no tienes colecciones.</p>
        <button>Crear la primera</button>
      </div>
    );
  return (
    <ul>
      {data.map((c) => (
        <li key={c.id}>{c.nombre}</li>
      ))}
    </ul>
  );
}
```

La mutación de crear invalida la key para que la lista se refresque:

```tsx
const qc = useQueryClient();
const crear = useMutation({
  mutationFn: crearColeccion,
  onSuccess: () => qc.invalidateQueries({ queryKey: ["colecciones"] }),
});
```

### 5. Formulario de login — RHF + zod (el schema es la validación)

```tsx
"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email("Email inválido"),
  password: z.string().min(8, "Mínimo 8 caracteres"),
});
type Datos = z.infer<typeof schema>;

export function LoginForm() {
  const { register, handleSubmit, formState } = useForm<Datos>({ resolver: zodResolver(schema) });
  return (
    <form onSubmit={handleSubmit(async (d) => { /* POST /auth/token; guarda el token */ })}>
      <label htmlFor="email">Email</label>
      <input id="email" {...register("email")} aria-invalid={!!formState.errors.email} />
      {formState.errors.email && <p role="alert">{formState.errors.email.message}</p>}
      {/* password análogo */}
      <button type="submit" disabled={formState.isSubmitting}>Entrar</button>
    </form>
  );
}
```

### 6. Chat con streaming + a11y + anti-XSS (verificado AI SDK v5)

```tsx
// src/app/chat/page.tsx
"use client";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { useState } from "react";

export default function ChatPage() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, stop, error, regenerate } = useChat({
    transport: new DefaultChatTransport({ api: "/api/chat" }),
  });

  return (
    <main>
      {messages.length === 0 && <p>Pregúntame algo sobre tus documentos.</p>}
      <ul aria-live="polite">
        {messages.map((m) => (
          <li key={m.id} data-rol={m.role}>
            <strong>{m.role === "user" ? "Tú" : "Asistente"}: </strong>
            {/* Salida del LLM como TEXTO (React escapa). NUNCA dangerouslySetInnerHTML. */}
            {m.parts.map((p, i) => (p.type === "text" ? <span key={i}>{p.text}</span> : null))}
          </li>
        ))}
      </ul>

      {(status === "submitted" || status === "streaming") && (
        <p>
          {status === "submitted" ? "Pensando…" : "Escribiendo…"}{" "}
          <button type="button" onClick={() => stop()}>Detener</button>
        </p>
      )}
      {error && (
        <p role="alert">
          Algo falló. <button type="button" onClick={() => regenerate()}>Reintentar</button>
        </p>
      )}

      <form onSubmit={(e) => { e.preventDefault(); if (input.trim()) { sendMessage({ text: input }); setInput(""); } }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} disabled={status !== "ready"} />
        <button type="submit" disabled={status !== "ready"}>Enviar</button>
      </form>
    </main>
  );
}
```

### 7. Route Handler — `streamText` (server-only; la API key no toca el cliente)

```ts
// src/app/api/chat/route.ts
import { streamText, convertToModelMessages, type UIMessage } from "ai";
import { openai } from "@ai-sdk/openai"; // o el proveedor que use el alumno; la key se lee de env server-only

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({
    model: openai("gpt-4o"), // intercambiable en una línea
    messages: convertToModelMessages(messages),
  });
  return result.toUIMessageStreamResponse();
}
```

> En F6 este handler se reemplaza por un `fetch` (o proxy) al endpoint de streaming del backend FastAPI con
> RAG; el componente `ChatPage` no cambia.

### 8. Zustand — solo client-state

```ts
// src/lib/store.ts
import { create } from "zustand";

interface UIState {
  sidebarAbierto: boolean;
  coleccionActiva: string | null;
  toggleSidebar: () => void;
  setColeccionActiva: (id: string | null) => void;
}
export const useUI = create<UIState>((set) => ({
  sidebarAbierto: true,
  coleccionActiva: null,
  toggleSidebar: () => set((s) => ({ sidebarAbierto: !s.sidebarAbierto })),
  setColeccionActiva: (id) => set({ coleccionActiva: id }),
}));
```

### 9. Accesibilidad (el gate)

Navegable solo con teclado (orden de tab lógico, foco visible vía `:focus-visible`); el modal de crear colección
atrapa el foco (focus trap) y lo devuelve al disparador al cerrar; contraste WCAG 2.2 verificado; `aria-live`
en el contenedor del chat; landmarks (`header`/`main`/`nav`) y headings jerárquicos. El `excelente` corre un
chequeo `jest-axe` en CI **y** documenta la pasada manual de teclado.

### 10. Seguridad, observabilidad, CI

- **Seguridad:** salida del LLM como texto (test que prueba el escapado de un `<script>`); API key server-only;
  CORS acotado en el backend; decisión del token (cookie `HttpOnly` recomendada) argumentada.
- **Observabilidad:** registra latencia y tokens por respuesta (de `onFinish` del stream o midiendo en el cliente).
- **CI (`.github/workflows/ci.yml`):** `eslint` → `vitest run` (incluye axe). Falla si hay violaciones de a11y.

### 11. README (en inglés) + write-up de trade-offs

`pnpm install && pnpm dev` → demo con GIF (login → crear colección → chat con streaming → estado de error al
apagar el backend). Write-up: *"Kept server-state in TanStack Query and only UI state in Zustand so the
collection list never goes stale. The AI lives in a Next Route Handler for now; in Phase 6 it moves to the
FastAPI streaming endpoint with no UI change. Stored the token in an HttpOnly cookie over localStorage to avoid
XSS token theft; the trade-off is a bit more backend setup."*

---

## Mapeo al Definition of Done (lo que el corrector verifica)

| Punto del DoD (§B) | Evidencia en el ejemplar | Aplica en F4 |
|---|---|---|
| **1. Spec + ADRs** | `SPEC.md` (con inventario de estados) antes del 1er componente + ADR de frontera | ✅ Obligatorio |
| **2. Tests + lint en CI** | componentes (4 estados) + máquina del chat + axe; `eslint` en CI | ✅ Obligatorio |
| **3. Seguridad (frontend)** | salida del LLM como texto (test); API key server-only; CORS acotado | ✅ Obligatorio |
| **4. Observabilidad** | latencia/tokens por respuesta registrados | ✅ (semilla de costo/latencia) |
| **7. a11y (WCAG 2.2) + estados** | teclado/foco/contraste/aria-live + 4 estados por vista | ✅ **El gate de la fase** |
| **8. Demo + README inglés + write-up** | `pnpm dev` + GIF + trade-offs | ✅ Obligatorio |
| **9. Conventional Commits** | historial spec→ADR→providers→features→gate→docs | ✅ Obligatorio |
| 5. Eval harness (IA) | — la IA real llega en F6 | 🌱 semilla → F6 |
| 6. Validación/least-privilege de agente | — no hay agente | 🌱 semilla → F6/F7 |

## Rango de soluciones aceptables (para no penalizar lo correcto)
- **Cualquier layout/diseño** sirve si tiene las tres superficies (datos del servidor, chat con streaming, un formulario validado) y pasa el gate de a11y + estados. No exigir `docubase-ui`.
- **El proveedor del modelo** puede ser cualquiera del AI SDK (OpenAI, Anthropic, etc.); lo que importa es que sea server-only y el chat haga streaming. Aceptar también consumir el stream a mano (leer el `ReadableStream`) si está bien hecho, aunque `useChat` es lo recomendado.
- **El estado global** puede ser Zustand, Context o incluso ninguno si la app no lo necesita (YAGNI es válido). Lo que **no** se acepta es server-state en un store global.
- **El markdown del chat** es opcional; si lo hay, debe sanitizar y prohibir HTML crudo. Texto plano también es `competente`.
- **El almacenamiento del token** puede ser cookie `HttpOnly` (mejor) o `localStorage` **si** el alumno nombra el trade-off de XSS. Hacerlo en piloto automático sin mención = `en-progreso` en seguridad.
- **Otro framework** (Vite + React Router, Remix, etc.) es válido si cumple el mismo DoD: spec, ADR, server-state cacheado, formularios validados, chat con streaming, a11y + estados, tests, secretos fuera, Conventional Commits. La Fase 4 marca Next.js como troncal, pero el capstone evalúa el DoD, no el framework.
- Para el gate Primero-Sin-IA: lo decisivo es que **defienda su frontera de estado y sus decisiones de a11y sin notas**. Un frontend más simple pero entendido y accesible supera a uno vistoso que no puede explicar.
