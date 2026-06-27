# SPEC — <nombre de tu app> (frontend de una app de IA)

> Escribe esto **antes** del primer componente. Su commit debe preceder al código (DoD 1). Un frontend serio
> especifica **estados**, no solo "pantallas felices". Borra estas citas al completarla.

## 1. Resumen en una frase

<Qué hace la app y para quién. Ej.: "UI para que un usuario consulte y gestione su base de conocimiento de
documentos, y converse con un asistente de IA sobre ellos, sobre la API de la Fase 3.">

## 2. Backend que consume

- **API base:** `NEXT_PUBLIC_API_URL` (tu API de la Fase 3).
- **Endpoints usados:** <p. ej. `POST /auth/token`, `GET /colecciones`, `POST /colecciones`,
  `GET /documentos?coleccion_id=...`>.
- **Contrato de error:** RFC 9457 (`type`/`title`/`status`/`detail`). El frontend lee `detail` para los estados
  de error.
- **IA / chat:** hoy vía Route Handler de Next con `streamText`; en F6 migrará a un endpoint de streaming del
  backend (anótalo en el ADR).

## 3. Pantallas y rutas

| Ruta | Pantalla | Server o Client | Datos que consume |
|---|---|---|---|
| `/login` | Login | Client (form) | `POST /auth/token` |
| `/` | Lista de colecciones | <Server/Client> | `GET /colecciones` |
| `/chat` | Chat de IA | Client | Route Handler `/api/chat` (stream) |

## 4. Frontera de estado (la decisión clave)

| Dato | Tipo | Dónde vive | Por qué |
|---|---|---|---|
| Lista de colecciones | server-state | TanStack Query | fuente de verdad en el backend; necesita caché + invalidación |
| Mensajes del chat | chat-state | `useChat` (AI SDK) | streaming + optimistic UI |
| Tema, sidebar, colección activa | client-state | Zustand | puro estado de UI del cliente |

## 5. Inventario de estados (GATE — no opcional)

Para **cada vista con datos**, define las cuatro caras:

### Vista: lista de colecciones
- **empty:** <qué se ve cuando no hay ninguna; call-to-action para crear la primera>
- **loading:** <skeleton, no spinner mudo>
- **error:** <mensaje accionable leyendo el `detail` + botón Reintentar>
- **success:** <la lista>

### Vista: chat (seis estados, de la lección 4.11)
- vacío · enviando · streaming · completado · error · cancelado → <qué ve el usuario en cada uno>

## 6. Formularios (RHF + zod)

| Formulario | Schema zod (campos + reglas) | Acción |
|---|---|---|
| Login | `{ email: string().email(), password: string().min(8) }` | `POST /auth/token` |
| Crear colección | <...> | `POST /colecciones` + invalidar `["colecciones"]` |

## 7. Accesibilidad (GATE — WCAG 2.2)

- [ ] Toda la app operable solo con teclado (orden de tab lógico, foco visible).
- [ ] El modal de crear colección atrapa el foco y lo devuelve al cerrar.
- [ ] Contraste de texto/controles cumple el mínimo de WCAG 2.2.
- [ ] El contenedor del chat usa `aria-live="polite"` para anunciar el texto en streaming.
- [ ] Landmarks (`header`/`main`/`nav`) y jerarquía de headings correctas.

## 8. Seguridad

- [ ] La salida del LLM se renderiza como texto (o markdown sanitizado). Nada de `dangerouslySetInnerHTML`.
- [ ] La API key del modelo es **server-only** (no `NEXT_PUBLIC_`).
- [ ] CORS acotado en el backend (no `*`).
- [ ] Decisión sobre el token (cookie `HttpOnly` vs `localStorage`) + su trade-off, anotada.

## 9. Fuera de alcance (qué NO hago en este capstone)

<Lista honesta. Ej.: "sin paginación infinita, sin multi-idioma, sin tema oscuro persistido en servidor.">
