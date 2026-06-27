---
ejercicio_id: fase-4/frontera-server-client
fase: fase-4
sub_unidad: "4.6"
version: 1
---

# Rúbrica — Decide la frontera servidor/cliente y el modo de render

> Rúbrica analítica atada a los `objetivos`. Es un ejercicio de **diseño**: no hay suite que pase
> o falle, hay razonamiento defendible vs. indefendible. El corrector evalúa el `decisiones.md`:
> ¿clasifica bien?, ¿justifica?, ¿defiende el trade-off de render?, ¿ve la seguridad? Lo que se
> mide es el **juicio**, no que adivine "la" respuesta. Hay un rango de decisiones aceptables.

## Objetivos evaluados
- **O1** — Clasificar cada pieza (Server Component / Client Component / Route Handler / Server Action) con justificación.
- **O2** — Colocar la frontera `'use client'` lo más abajo posible y explicar por qué no en la raíz.
- **O3** — Elegir el modo de render justificando el trade-off de frescura vs. costo/latencia.

## Criterios y niveles

### C1 — Clasificación de las 7 piezas (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Clasifica menos de la mitad bien, o pone todo como "componente" sin distinguir servidor/cliente. |
| **en-progreso** | Acierta las obvias (lista=servidor, búsqueda=cliente) pero confunde Route Handler con Server Action, o trata la pieza 5 igual que la 2. |
| **competente** | Las 7 bien clasificadas con justificación: lista (1) y layout (6) = Server Component; búsqueda (2), tema (3), analítica (7) = Client Component; favorito (4) = Server Action; autocompletado (5) = Client Component que consume un Route Handler. |
| **excelente** | Además matiza: el botón favorito (4) es una **isla cliente** que invoca una Server Action; el autocompletado (5) necesita **ambos** (UI cliente + endpoint servidor); nombra qué prop serializable pasa la página a cada isla. |

### C2 — Frontera `'use client'` (corrección) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Pondría `'use client'` en la página/layout, o no menciona la frontera. |
| **en-progreso** | Sabe que va en las piezas interactivas pero no explica el costo de subirla. |
| **competente** | Coloca `'use client'` solo en las hojas interactivas (búsqueda, tema, favorito, autocompletado, analítica) y explica que en la raíz arrastraría todo el árbol al navegador (más JS, sin SSR). |
| **excelente** | Menciona que todo módulo importado por un Client Component se vuelve cliente, y que por eso conviene componer "servidor afuera, islas adentro"; señala que la lista y el layout no deben pagar JavaScript. |

### C3 — Modo de render y trade-off (corrección + juicio) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige modo, o elige sin justificar ("uso SSR porque sí"). |
| **en-progreso** | Elige un modo razonable pero la justificación no menciona frescura ni costo/latencia. |
| **competente** | Elige un modo defendible (ISR si el catálogo es público y cambia con calma; dinámico si los favoritos por usuario se renderizan en el servidor) y lo justifica con frescura vs. costo. |
| **excelente** | Reconoce que **depende**: el catálogo en sí es ISR-able, pero el estado "es mi favorito" es por-usuario → o se hidrata en el cliente, o la página se vuelve dinámica; discute la tensión en vez de dar una respuesta plana. |

### C4 — Seguridad y comunicación · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona seguridad, o cree que validar en el cliente basta. |
| **en-progreso** | Dice "hay que validar" pero no especifica dónde ni por qué el cliente no basta. |
| **competente** | Señala que la Server Action del favorito (4) y el Route Handler del autocompletado (5) deben validar/autorizar en el servidor, porque el cliente es no confiable (curl se salta el navegador). |
| **excelente** | Explica por qué un secreto en un Client Component se filtra (corre en el navegador; `NEXT_PUBLIC_` lo expone) y conecta con least-privilege: cada endpoint valida su propia entrada. |

## Errores típicos a marcar
- Tratar la pieza 2 (filtra lista en memoria) y la 5 (pide al servidor) como lo mismo: la 2 no necesita endpoint, la 5 sí.
- Confundir Route Handler con Server Action: el favorito (mutación disparada por la UI) es Server Action; el autocompletado (datos bajo demanda) es Route Handler.
- Clasificar el ping de analítica (7) como Server Component: ocurre **en el navegador** al montar (es un efecto del cliente), no en el render del servidor.
- Poner `'use client'` en el layout o la página "para simplificar": anula el SSR de toda la rama.
- Elegir "dinámico" para todo por miedo a servir datos viejos, sin notar el costo (cada petición re-renderiza).
- Creer que validar en el `<input>` del cliente protege el endpoint.
- (transversal) no defender **ningún** trade-off: dar etiquetas sin justificación es lo que la rúbrica penaliza.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tabla perfecta con vocabulario avanzado (RSC payload, streaming, PPR) pero no puede explicar por qué la pieza 2 NO necesita un Route Handler.
- Justificaciones genéricas copiadas ("mejora el rendimiento y el SEO") que no se refieren a la pieza concreta.
- **Verificación sugerida:** pídele que defienda, en vivo, por qué movería `'use client'` del layout a la caja de búsqueda (qué empeora si lo deja arriba). O que prediga qué pasa si lee la clave de la base de datos dentro del componente de la caja de búsqueda. Si entiende, responde al instante; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca dar la tabla resuelta completa.
- **Pista (nivel 1):** "Para cada pieza, pregúntate solo una cosa primero: ¿necesita que el usuario interactúe en el navegador (teclear, hacer clic, leer localStorage)? Eso ya decide servidor vs. cliente."
- **Pregunta socrática (nivel 2):** "La búsqueda (2) y el autocompletado (5) parecen lo mismo. ¿Qué datos tiene cada una a mano? Si una ya tiene la lista en memoria y la otra debe ir a buscar a un índice grande, ¿cuál necesita un endpoint del servidor?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa tu modo de render: ¿el dato 'es MI favorito' es igual para todos los visitantes o cambia por usuario? Si cambia por usuario, ¿puede la página seguir siendo estática/ISR, o necesitas hidratar ese pedazo en el cliente? Defiende una de las dos salidas."

## Conexión con el proyecto / capstone
- Estas exactas decisiones son las que tomarás en el [Capstone F4](/fase-4-frontend/proyecto/): qué parte del chat es servidor, qué isla es cliente, dónde va el endpoint del modelo y con qué modo de render. Un capstone con la frontera mal puesta es lento, caro o inseguro; este ejercicio te entrena a decidirlo antes de escribir una línea.
