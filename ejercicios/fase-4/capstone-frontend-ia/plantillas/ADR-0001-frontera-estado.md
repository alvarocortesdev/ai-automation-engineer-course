# ADR-0001 — Frontera de estado y dónde vive la IA

> Un ADR (Architecture Decision Record) registra una decisión y *por qué*. Mantenlo corto y honesto. Borra estas
> citas al completarlo. Formato: Contexto · Decisión · Alternativas · Consecuencias.

- **Estado:** aceptado
- **Fecha:** <YYYY-MM-DD>

## Contexto

La app tiene tres clases de estado con orígenes distintos: datos del servidor (colecciones/documentos de la API
F3), el estado del chat de IA (mensajes, streaming) y estado de UI del cliente (tema, sidebar). Mezclarlos lleva
a datos obsoletos, re-renders innecesarios y código que reinventa caché. Además, el backend de la Fase 3 todavía
no tiene IA: hay que decidir dónde vive el endpoint de chat *hoy*, sin pintarse para la Fase 6.

## Decisión

1. **Server-state → TanStack Query.** Toda lectura/mutación de la API F3 usa `useQuery`/`useMutation` con
   invalidación. Razón: caché, loading/error de primera clase y refetch sin reimplementarlos.
2. **Chat-state → `useChat` del AI SDK.** Streaming y optimistic UI vienen cableados.
3. **Client-state → Zustand**, solo para tema/sidebar/colección activa. Razón: estado de UI global mínimo.
4. **La IA vive hoy en un Route Handler de Next (`/api/chat`) con `streamText`.** Razón: el backend F3 aún no
   tiene IA; el Route Handler habla directo con el modelo y devuelve un stream que `useChat` entiende.

## Alternativas consideradas

- **Todo en Zustand (o Redux):** descartado — el server-state queda obsoleto sin invalidación y reimplementa lo
  que TanStack Query ya da.
- **`useEffect` + `useState` para fetch:** descartado — sin caché, sin estados de primera clase, propenso a
  condiciones de carrera.
- **Llamar al modelo desde el cliente:** descartado — expondría la API key del modelo en el navegador.

## Consecuencias

- **Positivas:** cada dato tiene un único hogar; las vistas son simples (consumen un hook, no orquestan caché).
- **Costo aceptado:** dos sistemas de estado que aprender (Query + Zustand), pero con responsabilidades claras.
- **Mirando a F6:** el Route Handler `/api/chat` se reemplazará por un endpoint de streaming del backend FastAPI
  (RAG/agente). **La UI no cambia** porque el contrato del stream es el mismo. Esa es la ganancia de esta
  frontera.
