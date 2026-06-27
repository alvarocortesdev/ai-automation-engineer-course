---
ejercicio_id: fase-4/tailwind-tarjeta-responsive
fase: fase-4
sub_unidad: "4.2"
version: 1
---

# Rúbrica — Tarjeta responsive con estados y dark mode (utility-first)

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests verifican el **método**
> (utilidades, escala, variantes, cero CSS propio), no la estética. El corrector contrasta el
> `tarjeta.html` del alumno con el método correcto y la solución de referencia, y evalúa también
> si el alumno **entiende** lo que escribió (no solo si el test pasa en verde).

## Objetivos evaluados
- **O1** — Construir un componente con utility-first usando la escala de espaciado y de color.
- **O2** — Aplicar variantes responsive (`sm:`/`md:`/`lg:`), de estado (`hover:`/`focus:`) y dark mode (`dark:`).
- **O3** — Estilar sin CSS propio: sin `style=` inline ni `@apply`.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): una `<article>` con `flex/grid` +
> `gap-*`/`p-*`, al menos un cambio `md:`, un `hover:` en el botón, y pares `dark:` para fondo y
> texto; sin estilos inline ni `@apply`.

## Criterios y niveles

### C1 — Utility-first y escala (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sin layout (todo apilado por defecto) o con valores arbitrarios/inline; no usa la escala. |
| **en-progreso** | Usa algunas utilidades pero mezcla con CSS propio, o el espaciado es inconsistente (a ojo, no desde la escala). |
| **competente** | Layout con `flex`/`grid`, espaciado desde la escala (`gap-*`, `p-*`), `rounded-*`/`shadow-*`; tarjeta completa (imagen/color, título, descripción, precio, botón). |
| **excelente** | Además compone con orden y mobile-first claro; nombra por qué la escala restringida da consistencia (mini design system). |

### C2 — Variantes: responsive, estado, dark mode · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin prefijos responsive, sin `hover:`, sin `dark:`. |
| **en-progreso** | Tiene una o dos de las tres (p. ej. responsive pero sin dark mode), o `dark:` solo en un elemento sin coherencia. |
| **competente** | Las tres presentes: al menos un `md:` que cambia disposición/tamaños, un `hover:` real, y `dark:` en fondo + texto. |
| **excelente** | Apila variantes con criterio (p. ej. `dark:md:hover:`) y explica en voz alta qué condiciones deben cumplirse para que aplique. |

### C3 — Cero CSS propio (disciplina utility-first) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Hay `style="..."` inline o un bloque de CSS propio escrito a mano para la tarjeta. |
| **en-progreso** | Sin inline, pero usó `@apply` para "limpiar" su propio marcado. |
| **competente** | Todo el aspecto sale de utilidades: ningún `style=` inline, ningún `@apply`. |
| **excelente** | Articula por qué `style=` inline no podría lograr `hover:`/`md:`/`dark:` y por qué no necesitó `@apply`. |

### C4 — Comprensión demostrada · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar qué hace `md:p-8` ni por qué el base es móvil. |
| **en-progreso** | Explica a medias (sabe que "md es responsive" pero no que solo sobre-escribe desde el breakpoint). |
| **competente** | Explica mobile-first: el base aplica siempre y `md:` sobre-escribe desde 768px hacia arriba. |
| **excelente** | Explica además la diferencia conceptual con estilos inline y el rol del escaneo/purga de Tailwind. |

## Errores típicos a marcar
- `style="..."` inline o un `<style>` con CSS a mano para la tarjeta (rompe O3; el test lo atrapa el inline, el CSS a mano lo ve el corrector).
- `@apply` para ordenar HTML propio cargado (anti-patrón central de la lección).
- Valores fuera de escala simulados con utilidades arbitrarias sin necesidad, o números mágicos vía inline.
- Poner `dark:` solo en un elemento → en modo oscuro queda texto invisible o fondo a medias (incoherente).
- Confundir mobile-first: escribir `md:flex-col` pensando que "md es lo chico" (es al revés: base = móvil).
- Borrar los comentarios marcadores (el test no encuentra la región) o dejar el placeholder "Reemplázame".
- (transversal) usar material de v3 (`tailwind.config.js`) sin notar que v4 es CSS-first.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tarjeta impecable con utilidades exóticas y bien apiladas, pero el alumno no sabe explicar por qué `md:` no afecta al móvil (sofisticación impropia del primer contacto con Tailwind).
- Mezcla de convenciones v3 y v4 que delata copiar/pegar de fuentes distintas sin entender.
- **Verificación sugerida:** pídele que, en vivo, **quite** el dark mode de un elemento y prediga qué se verá mal en tema oscuro; o que cambie el breakpoint de `md:` a `lg:` y diga qué cambia. Si entiende, responde al instante; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el marcado completo.
- **Pista (nivel 1):** "Una variante es un prefijo que condiciona *cuándo* aplica la utilidad. ¿Cuántas de las tres variantes pedidas (responsive, hover, dark) están en tu tarjeta? Cuenta los prefijos."
- **Pregunta socrática (nivel 2):** "Si tu base es `flex-col` y agregas `md:flex-row`, ¿qué ve un teléfono y qué ve una laptop? ¿Por qué el teléfono no necesita prefijo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Por cada utilidad de color que tienes (`bg-white`, `text-gray-900`), agrega su gemela con prefijo `dark:`. Para el botón, agrega un `hover:bg-...`. Elige UNA cosa que cambie en `md:`. No te doy el marcado."

## Conexión con el proyecto / capstone
- Esta tarjeta es el patrón de cada panel y burbuja del [Capstone F4](/fase-4-frontend/proyecto/); el dark mode con `dark:` y los estados de foco se cruzan con la [4.4 Accesibilidad](/fase-4-frontend/4-4-accesibilidad-wcag/), que es gate del capstone.
