---
ejercicio_id: fase-4/landing-semantica-responsive
fase: fase-4
sub_unidad: "4.1"
version: 1
---

# Rúbrica — Landing semántica y responsive (sin frameworks)

> Rúbrica analítica. El test automático (`node --test`) verifica el **esqueleto** (landmarks, un `h1`, `alt`, viewport, grid/flex, media query, `rem`); **pasar el test es necesario pero no suficiente**. Lo que aquí se evalúa, y el test no puede, es la **calidad** de la semántica, del layout responsive y la **justificación** de las decisiones. El corrector da feedback, no una nota.

## Objetivos evaluados
- **O1** — HTML semántico que se lee bien sin CSS (landmarks, un solo `h1`, `alt`, `lang`).
- **O2** — Layout responsive mobile-first con Flexbox + Grid, `rem` y una media query.
- **O3** — Justificar Flexbox (1D) vs. Grid (2D) en el layout construido.

## Criterios y niveles

### C1 — Corrección semántica (¿es HTML que comunica estructura?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | *Div-soup*: landmarks ausentes o todo en `div`; varios `h1` o saltos de nivel; imágenes sin `alt`. Tests rojos. |
| **en-progreso** | Tiene los landmarks (test verde) pero los usa mal: `section` sin encabezado, encabezados fuera de orden, `alt` vacío en imágenes informativas, o `nav` sin contenido real. |
| **competente** | Landmarks correctos, un solo `h1`, jerarquía `h1→h2→h3` ordenada, `alt` descriptivos, `lang`/`viewport` presentes. **Se lee bien sin CSS.** |
| **excelente** | Además: `aria-label` en `nav`, `alt=""` consciente en imágenes decorativas, uso de `article`/`section` que un lector de pantalla recorrería como un índice limpio. |

### C2 — Layout responsive mobile-first · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No es responsive (anchos fijos en `px`), o se rompe al achicar; sin media query. |
| **en-progreso** | Hay media query y grid/flex (test verde), pero es **desktop-first** (usa `max-width`) o el breakpoint deja un estado intermedio roto. |
| **competente** | Mobile-first real: estilos base para móvil + `@media (min-width)` que añade; Grid para las tarjetas, Flexbox para la nav; `rem` en tipografía/espaciado; `border-box`. |
| **excelente** | Grid intrínseco (`repeat(auto-fill, minmax(...))`) que se adapta sin breakpoints extra; imágenes con `max-width: 100%`; layout fluido entre breakpoints, no solo en dos tamaños fijos. |

### C3 — Comprensión demostrada (la decisión calza con el código) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `spec.md` ni justificación; o la explicación no corresponde al código entregado. |
| **en-progreso** | Justifica de forma genérica ("usé grid porque es moderno") sin ligarlo al problema (1D vs 2D). |
| **competente** | Explica por qué Flexbox en la nav (una fila, 1D) y Grid en las tarjetas (rejilla 2D), y por qué mobile-first; el `spec.md` precede al código. |
| **excelente** | Anticipa trade-offs (cuándo Grid sería peor, por qué `rem` y no `px` por accesibilidad) y conecta con el gate WCAG del capstone. |

## Errores típicos a marcar
- *Div-soup* con clases tipo `.header`/`.nav` en vez de las etiquetas semánticas (se ve igual, no comunica nada).
- Más de un `<h1>`, o saltar de `h1` a `h3`.
- `alt` ausente, o `alt="imagen"` / `alt="foto"` que no describe nada.
- **Desktop-first disfrazado**: media query con `max-width` y estilos base pensados para pantalla grande.
- Todo en `px` (rompe el escalado de fuente del usuario).
- Olvidar el `<meta viewport>` (el responsive no funciona en móvil real aunque las queries estén).
- Usar Grid donde basta Flexbox o viceversa **sin** poder justificarlo.
- (transversal) entregar sin `spec.md`: codear sin diseñar primero.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- HTML/CSS muy pulido (variables CSS, animaciones, `clamp()`) impropio de una primera lección, que el alumno no puede explicar línea a línea.
- `spec.md` ausente o escrito *después* (genérico, no calza con el HTML real).
- Justificación que usa términos correctos pero no señala **dónde** en su código está cada decisión.
- **Verificación sugerida:** pedir que, sin IA, mueva el `<aside>` (si lo tiene) o cambie el breakpoint de 700 a 900px y prediga qué pasa; o que explique por qué su grid se reacomoda sin una media query por cada cantidad de columnas. Si construyó de verdad, lo resuelve.

## Feedback sugerido (graduado)
> Nunca entregar el HTML/CSS de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Comenta tu `<link>` al CSS y recarga. ¿El contenido se lee en un orden con sentido? Si no, la estructura semántica todavía no está; el CSS no debe ser lo que da el orden."
- **Pregunta socrática (nivel 2):** "Tu nav, ¿es una fila o una rejilla? ¿Y las tarjetas? Una de esas dos cosas es 1D y la otra 2D. ¿Qué herramienta encaja con cada una y por qué?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Pasa a mobile-first: deja los estilos base para móvil (todo en columna) y mueve los cambios de escritorio dentro de una `@media (min-width: ...)`. Para las tarjetas, `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` te da columnas que se adaptan solas."

## Conexión con el proyecto / capstone
- Este esqueleto semántico + responsive es el cimiento del **Capstone F4 — Frontend de una app de IA**: cuando React genere el HTML, la estructura debe ser igual de limpia para pasar el **gate de accesibilidad (WCAG 2.2)**. Lo que aquí haces a mano, allá lo automatizas — pero solo si lo entendiste primero.
