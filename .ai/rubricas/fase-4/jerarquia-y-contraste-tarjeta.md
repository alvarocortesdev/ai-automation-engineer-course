---
ejercicio_id: fase-4/jerarquia-y-contraste-tarjeta
fase: fase-4
sub_unidad: "4.3"
version: 1
---

# Rúbrica — Rediseña una tarjeta de IA: jerarquía, escala y contraste AA

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **mixto**: una parte es objetiva
> (el test de contraste pasa o no) y otra es de criterio (jerarquía, espaciado, tipografía), que se juzga
> con el *squint test* y la coherencia de las decisiones. El corrector la usa con
> `INSTRUCCIONES-CORRECTOR.md`. No es una nota: es un mapa de qué observar y cómo dar feedback.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Rediseñar con jerarquía visual (tamaño + peso + contraste): tres niveles distinguibles con el
  squint test.
- **O2** — Aplicar una escala de espaciado consistente y una escala tipográfica, agrupando por proximidad.
- **O3** — Verificar que la paleta cumple WCAG 2.2 AA (texto 4.5:1, UI 3:1).

## Criterios y niveles

### C1 — Jerarquía visual · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Todo el texto sigue pesando casi igual; el squint test no distingue niveles. |
| **en-progreso** | Hay dos niveles (p. ej. solo título grande), pero la metadata no se diferencia del cuerpo, o la jerarquía se logra "haciendo todo grande/bold". |
| **competente** | Tres niveles claros (título / cuerpo / metadata) construidos con tamaño + peso + contraste; el squint test los separa; lo secundario está deliberadamente atenuado. |
| **excelente** | Además la jerarquía de **acciones** es correcta (el botón primario destaca como el CTA), y el alumno explica *por qué* bajó el volumen de lo secundario, no solo subió lo principal. |

### C2 — Escala de espaciado y tipografía · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Espacios arbitrarios (10px, 7px…) sin escala; tamaños de fuente al azar; sin `line-height` ni control de ancho. |
| **en-progreso** | Hay tokens de escala pero se mezclan con valores sueltos; o la escala existe pero la **proximidad** no agrupa (mismo espacio entre todo). |
| **competente** | Escala de espaciado base consistente (todos múltiplos de la base) usada en todo; escala tipográfica de ≤ 3 tamaños; cuerpo con `line-height` ~1.5 y `max-width` en `ch`; proximidad agrupa (menos intra-grupo, más inter-grupo). |
| **excelente** | Las escalas viven en custom properties con nombres que son decisiones (design tokens); el alumno justifica la base y la razón elegidas; el ritmo es impecable. |

### C3 — Contraste / accesibilidad (DoD punto 7) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El test de contraste está en rojo; algún par no cumple su umbral. |
| **en-progreso** | El test pasa pero "por suerte" (no sabe explicar qué umbral aplica a qué par, o no verificó con herramienta). |
| **competente** | Los cuatro pares pasan (texto/fondo 4.5:1, tenue/fondo 4.5:1, sobre-acento/acento 4.5:1, acento/fondo 3:1) y el alumno sabe qué SC aplica. |
| **excelente** | Además entiende que el "tenue" tiene un piso AA, no usa solo color para comunicar estados, y deja registro de cómo verificó (herramienta + valores). |

### C4 — Comprensión demostrada (decisiones.md calza con el CSS) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `decisiones.md`, o repite definiciones de la lección sin referirse a su propio diseño. |
| **en-progreso** | Describe qué hizo pero no *por qué* (sin trade-offs ni criterio). |
| **competente** | Justifica tamaños, base de espaciado y colores con criterio propio; explica cómo verificó el contraste. |
| **excelente** | Conecta sus tokens con el concepto de design system y nombra alguna tentación de exceso que resistió. |

## Errores típicos a marcar
- **Jerarquía por "todo grande y bold"**: si todo grita, nada resalta (la metadata debe atenuarse).
- **Escala rota**: un `margin: 18px` o `13px` colado entre valores de la escala base-4.
- **"Tenue" por debajo de AA**: gris claro tipo `#aaaaaa`/`#b0b0b0` que no pasa 4.5:1 — el error central que rompe el gate de 4.4.
- **Texto de cuerpo bajo 16px** o `line-height` apretado (~1) que mata la legibilidad.
- **Sin `max-width`**: párrafo a todo el ancho, longitud de línea ingobernable.
- **Acento decorativo, no funcional**: el botón primario no destaca como acción.
- (transversal spec-driven) tokens sin nombre semántico (`--azul1`, `--gris2`) en vez de roles (`--color-acento`, `--color-texto-tenue`).

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- `decisiones.md` con prosa pulida sobre "modular scale" y "8-point grid" que el alumno **no puede
  defender**: pídele que justifique por qué eligió SU base y SU razón, o que prediga el siguiente peldaño.
- CSS sofisticado (clamp, fluid type, container queries) impropio del nivel básico y sin explicación
  coherente con el resto.
- El test pasa con colores "exactos de una paleta famosa" pero no sabe qué umbral aplica a cada par:
  pídele que diga, sin mirar, qué pasa si baja el acento un tono.
- **Verificación sugerida:** pedirle que haga el squint test en voz alta sobre su propia tarjeta y nombre
  qué resalta y por qué. Si interiorizó las palancas, lo hace en segundos.

## Feedback sugerido (graduado)
> Nunca redactar el CSS por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Entrecierra los ojos mirando tu tarjeta: ¿se distinguen tres niveles, o todo pesa
  parecido? Si no, ¿qué palanca te falta aplicar a la metadata?"
- **Pregunta socrática (nivel 2):** "Tu test de contraste está rojo en el par tenue/fondo. ¿Qué umbral
  exige AA para texto normal, y tu gris lo cumple? ¿'Tenue' puede estar por debajo de ese piso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tus espacios mezclan 10px y 24px: elige una
  base (4 u 8) y exprésalo todo como múltiplos. Y oscurece el acento hasta que el texto blanco encima dé
  ≥ 4.5:1; mídelo con WebAIM, no a ojo. No te doy los valores: pruébalos y vuelve a correr el test."

## Conexión con el proyecto / capstone
- Esta tarjeta es un microcosmos del **Capstone F4**: jerarquía, tokens y contraste AA son justo lo que su
  UI de chat/RAG necesita para verse como producto y pasar el a11y gate de [4.4]. El `decisiones.md` es el
  germen del razonamiento de design tokens que formaliza [4.9].
