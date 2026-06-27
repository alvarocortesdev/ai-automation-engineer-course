---
ejercicio_id: fase-4/adoptar-design-system
fase: fase-4
sub_unidad: "4.9"
version: 1
---

# Rúbrica — ¿Tailwind directo, shadcn/ui o design system? (mini-ADR)

> Rúbrica analítica para un ejercicio de **razonamiento/diseño** (sin tests). El corrector evalúa el
> `decision-ds.md`: las 4 decisiones, la calidad del trade-off en cada justificación, y las dos
> respuestas trampa. No importa la letra elegida, sino **el porqué** y el costo que el alumno acepta.

## Objetivos evaluados
- **O1** — Decidir y justificar, por escenario, la estrategia de UI según el trade-off costo-de-montar vs costo-de-inconsistencia.
- **O2** — Explicar por qué shadcn/ui no es una dependencia (modelo "open code": código que posees).
- **O3** — Explicar qué da Radix por defecto (accesibilidad) y por qué no reimplementar un modal/menú accesible a mano.

> Decisiones esperadas (el corrector las sabe; NO se las entrega): 1=Tailwind directo · 2=shadcn/ui+tokens · 3=shadcn/ui+tokens (ambiguo, Tailwind directo también defendible) · 4=design system publicado.

## Criterios y niveles

### C1 — Decisiones correctas por escenario (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan escenarios, o invierte los extremos (DS publicado para el portafolio, Tailwind crudo para la empresa multi-equipo). |
| **en-progreso** | Acierta los extremos (1 y 4) pero trata el 2/3 sin criterio (p. ej. 2 como Tailwind directo ignorando los interactivos accesibles). |
| **competente** | Las 4 razonables: 1 Tailwind directo, 2 shadcn, 4 DS publicado; 3 con cualquiera de las dos defendibles **bien justificada**. |
| **excelente** | Además trata el 3 explícitamente como ambiguo y nombra el disparador para "subir de peldaño" (más productos/equipos). |

### C2 — Calidad del trade-off en las justificaciones (comprensión demostrada) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Justificaciones ausentes, circulares ("es lo mejor") o de moda ("porque shadcn es lo moderno"). |
| **en-progreso** | Da el beneficio pero **no nombra el costo** que acepta (media decisión de ingeniería). |
| **competente** | Cada decisión nombra beneficio **y** costo, apelando al eje "costo de montar/mantener vs costo de la inconsistencia". |
| **excelente** | Conecta con consecuencias concretas (tiempo, divergencia entre devs, mantenimiento del paquete) y reconoce que sub-ingeniería y sobre-ingeniería son ambos errores. |

### C3 — shadcn no es una dependencia (T1) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Está de acuerdo con el compañero, o no ve la diferencia. |
| **en-progreso** | Intuye que "es distinto" pero no nombra el modelo ni la consecuencia. |
| **competente** | Nombra "open code": el CLI copia el código en tu repo; lo posees y no se actualiza solo. |
| **excelente** | Deriva ambas consecuencias (control total para editar/extender **y** mantenimiento propio como costo) y contrasta con una librería tradicional en `node_modules`. |

### C4 — Accesibilidad del modal/menú (T2, seguridad/calidad) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que basta mostrar/ocultar con `onClick`; no menciona accesibilidad. |
| **en-progreso** | Dice "es mejor usar una librería" pero sin el porqué (no nombra foco/teclado/ARIA). |
| **competente** | Nombra al menos foco atrapado, `Esc` y ARIA, y por qué hacerlo a mano rompe WCAG; menciona que Radix lo resuelve. |
| **excelente** | Detalla la gestión de foco (atrapar + devolver al disparador), navegación por teclado del menú y roles/`aria-*`, y conecta explícitamente con el gate de [4.4](/fase-4-frontend/4-4-accesibilidad-wcag/). |

## Errores típicos a marcar
- Montar un DS publicado (Storybook, paquete) para el portafolio personal → sobre-engineering.
- Elegir Tailwind directo para el capstone ignorando que necesita modales/menús/select **accesibles**.
- Justificar por moda ("porque todos usan shadcn") en vez de por el trade-off.
- Dar solo el beneficio y omitir el costo de cada decisión.
- Decir que shadcn "se actualiza solo" como cualquier dependencia (no entendió "open code").
- Proponer construir interactivos accesibles a mano "para tener control" (el antipatrón de T2).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tabla con vocabulario impecable ("atomic design", "design tokens W3C") pero justificaciones genéricas que no aterrizan en los escenarios concretos ni nombran un costo.
- Respuestas T1/T2 que suenan a blog (mencionan herramientas que la lección no usó) sin poder defenderlas.
- **Verificación sugerida:** pídele mover un escenario (p. ej. "¿y si el portafolio fueran 40 páginas con 6 devs?") y que prediga cómo cambia su decisión y por qué. Si entiende, ajusta el peldaño con criterio; si copió, repite la respuesta genérica.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia.
- **Pista (nivel 1):** "Para cada escenario, hazte la pregunta que decide: ¿el costo de la inconsistencia ya supera el costo de montar la herramienta? Y mira el escenario 2: ¿qué tiene que el 1 no tiene?"
- **Pregunta socrática (nivel 2):** "Si construyes el modal del capstone a mano, ¿qué pasa cuando el usuario presiona `Esc` o `Tab` dentro del modal? ¿Quién gestiona el foco al cerrarlo? ¿Y dónde vive el código que copió el CLI de shadcn?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa el escenario 4: varios equipos + varios productos con una marca compartida es la señal de un DS publicado (tokens versionados + paquete). Y reescribe T1 centrándote en *dónde vive el código*: en tu repo, no en `node_modules`."

## Conexión con el proyecto / capstone
- Esta decisión es el **plano visual** del [Capstone F4](/fase-4-frontend/proyecto/): define si lo construyes con Tailwind directo o adoptas shadcn/ui, y por qué. Tomarla con criterio (y dejarla como mini-ADR) es justo el tipo de decisión que se evalúa en entrevista.
