---
ejercicio_id: fase-4/frontera-server-client
fase: fase-4
sub_unidad: "4.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un ejercicio de diseño:
> esta solución es **una** respuesta defendible, no la única. Úsala como vara de medir el
> razonamiento, no como plantilla exacta a exigir.

# Solución de referencia — Frontera servidor/cliente y modo de render

## Tabla canónica

| # | Pieza | Categoría | Por qué |
|---|---|---|---|
| 1 | Lista de modelos desde la DB | **Server Component** | Solo lee datos y arma HTML; sin interactividad. El `fetch`/consulta corre en el servidor, cerca de los datos y sin filtrar credenciales. No suma JS al navegador. |
| 2 | Caja de búsqueda (filtra lista en memoria) | **Client Component** | Necesita estado (`useState`) y `onChange`: interactividad = navegador. Filtra una lista que **ya** recibió por props; no necesita servidor. Es estado derivado (como en 4.5). |
| 3 | Botón de tema (localStorage) | **Client Component** | Lee/escribe `localStorage`, una API del navegador que no existe en el servidor. Por definición, cliente. |
| 4 | Botón "marcar favorito" (escribe en DB) | **Server Action** (disparada desde una isla cliente) | Es una **mutación** que la propia UI dispara. La action (`'use server'`) corre en el servidor, valida/autoriza y hace `revalidatePath`. El `<form>`/botón que la invoca es una pequeña isla cliente. |
| 5 | Autocompletado (pide al servidor un índice grande) | **Client Component** que consume un **Route Handler** | La UI (teclear, mostrar sugerencias) es cliente; pero los datos viven en un índice grande del servidor, así que se piden **bajo demanda** a un endpoint (`route.ts`, `GET /api/sugerencias?q=...`). Necesita **ambas** piezas. |
| 6 | Layout (logo + navegación) | **Server Component** | Estático, sin interacción. Es el cascarón; no debe pagar JavaScript ni volverse cliente. |
| 7 | Ping de analítica al abrir | **Client Component** (efecto al montar) | Ocurre en el navegador, una vez, al montar (`useEffect` con deps `[]`). No es render de servidor: es un efecto del cliente. |

## Frontera `'use client'`
La directiva va **solo** en las hojas interactivas: la caja de búsqueda (2), el botón de tema (3), el botón/form del favorito (4), el componente de autocompletado (5) y el componente de analítica (7). **No** va en la página `/modelos` ni en el layout: si la pusiera ahí, todo el árbol descendiente se volvería cliente, el navegador descargaría JavaScript de la lista y el layout que no lo necesitan, y perdería el render en servidor (más lento, peor SEO). El patrón correcto es **"servidor afuera, islas de cliente adentro"**: la página (servidor) obtiene los datos y le pasa props serializables a cada isla. Recordatorio clave: todo módulo que un Client Component **importe** se vuelve también cliente, así que la frontera debe quedar lo más abajo posible.

## Modo de render de la página
**Depende, y reconocerlo es lo correcto.** El catálogo en sí (la lista de modelos) es público y cambia con calma → candidato ideal a **ISR** (`export const revalidate = N`): sirve HTML cacheado, barato y rápido, y se regenera cada N segundos. La tensión está en el estado **"es MI favorito"** (pieza 4), que es **por usuario**: ese pedazo no puede ser estático global. Dos salidas defendibles:
- **(a) ISR + hidratar lo personal en el cliente:** la página es ISR (catálogo cacheado) y el estado de favoritos se carga en el navegador tras montar. Mantiene el catálogo barato; lo personal llega un instante después.
- **(b) Render dinámico (SSR):** si quieres que la página llegue ya personalizada (favoritos marcados desde el primer paint), la vuelves dinámica (`force-dynamic` o un `fetch` con `no-store` / acceso a `cookies()`), pagando un render por petición.

El trade-off es **frescura/personalización vs. costo/latencia**: (a) es más barato y escala mejor; (b) da una primera carga ya personalizada a costa de renderizar en cada petición. Para un catálogo público con un toque personal, (a) suele ganar.

## Seguridad
La validación y autorización deben vivir **en el servidor** en dos piezas:
- **Favorito (4, Server Action):** verificar que el usuario esté autenticado, que el `id` exista y que pueda marcarlo, **antes** de escribir en la DB. El cliente puede mandar cualquier `id`.
- **Autocompletado (5, Route Handler):** acotar y validar la consulta `q` (como en el ejercicio A), porque cualquiera puede llamar al endpoint con `curl`, saltándose el navegador.

Por qué el cliente no basta: la validación del `<input>` es UX, no seguridad — se evade con una petición directa. Y un secreto (clave de API, conexión a la DB) leído en un Client Component **se filtra**, porque ese código corre en el navegador; exponerlo con `NEXT_PUBLIC_` lo entrega a cualquiera que abra las devtools. Los secretos viven solo en Server Components, Route Handlers y Server Actions.

## Rango de respuestas aceptables
- Clasificar el favorito (4) como **Route Handler `POST`** en vez de Server Action es **aceptable** si lo justifica (ambos mutan en el servidor); lo importante es que NO lo deje en el cliente y que valide ahí. La Server Action es la respuesta más idiomática en App Router.
- Para el modo de render, **tanto (a) como (b) son válidos** si defiende el trade-off. Lo que NO es aceptable es "dinámico porque sí" o "estático" ignorando que los favoritos son por usuario.
- Tratar el autocompletado (5) como una sola pieza "Client Component" es **incompleto** si no menciona que necesita un endpoint de servidor para los datos.
- Marcar el ping de analítica (7) como Server Component es **error**: ocurre en el navegador.
