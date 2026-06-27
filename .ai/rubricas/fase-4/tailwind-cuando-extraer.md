---
ejercicio_id: fase-4/tailwind-cuando-extraer
fase: fase-4
sub_unidad: "4.2"
version: 1
---

# Rúbrica — Criterio: utilidades, componente o @apply

> Rúbrica analítica atada a los `objetivos` del contrato. Este ejercicio se corrige por **calidad
> del juicio**, no por "acertar la palabra": un alumno puede escribir "componente" en el escenario 1
> por inercia. La señal de aprendizaje está en la **justificación** (¿controla el marcado?, ¿se
> repite la estructura?) y en la **regla general**. No hay tests; todo el peso está en el write-up.

## Objetivos evaluados
- **O1** — Decidir entre componer utilidades, extraer un componente o usar `@apply` según el caso.
- **O2** — Defender el trade-off usando "¿controlo el marcado?" y "¿se repite la estructura?" como ejes.
- **O3** — Reconocer que usar `@apply` para limpiar HTML propio cargado es un anti-patrón.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): **1 → componente**, **2 → utilidades
> (no abstraer lo único)**, **3 → `@apply`/`@variant` (markup de tercero)**, **4 → `@apply` o el
> patrón de tipografía (markup generado)**. Regla general centrada en "¿es mío el marcado?".

## Criterios y niveles

### C1 — Decisiones correctas por escenario · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan escenarios o las decisiones son aleatorias (p. ej. `@apply` para el botón propio repetido). |
| **en-progreso** | Acierta dos o tres decisiones pero falla el eje (usa `@apply` donde corresponde componente, o abstrae el hero único). |
| **competente** | Las cuatro decisiones correctas: componente / utilidades / @apply / @apply. |
| **excelente** | Además matiza (p. ej. para el 4 menciona el patrón de tipografía/`prose` o estilar por etiqueta como alternativa válida). |

### C2 — Calidad de la justificación (trade-off) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Justifica con "porque sí" o repitiendo el enunciado; no menciona los ejes. |
| **en-progreso** | Menciona un eje (control del marcado **o** repetición) pero no los conecta a la decisión. |
| **competente** | Cada justificación nombra si controla el marcado y si se repite la estructura, y eso explica la decisión. |
| **excelente** | Da el daño concreto de elegir mal (p. ej. "`@apply` en el botón reintroduce CSS global acoplado que nadie limpia"). |

### C3 — Anti-patrón de `@apply` reconocido · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Trata `@apply` como la forma normal de "ordenar" utilidades; no ve el problema. |
| **en-progreso** | Intuye que "mejor componente" pero no sabe por qué `@apply` es peor. |
| **competente** | Explica que `@apply` para HTML propio reintroduce el CSS global/acoplamiento que utility-first elimina. |
| **excelente** | Distingue el caso legítimo (no controlas el marcado) del ilegítimo (limpiar HTML propio feo) con precisión. |

### C4 — Regla general (comunicación) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay regla o es vaga ("usa lo que convenga"). |
| **en-progreso** | Regla razonable pero sin el eje central (control del marcado). |
| **competente** | Regla que pone "¿controlo el marcado?" primero y "¿se repite la estructura?" después. |
| **excelente** | Regla memorable y defendible, aplicable a un caso nuevo sin dudar. |

## Errores típicos a marcar
- Elegir `@apply` en el escenario 1 "para no repetir clases": es el error central; con marcado propio repetido, la salida es **componente**.
- Abstraer el hero único (escenario 2) "por prolijidad": viola YAGNI; lo de una vez se deja en utilidades.
- En 3 y 4 proponer "edita el HTML para agregar clases": no controlas ese marcado, por eso `@apply` es legítimo.
- Justificaciones que solo dicen "es más limpio/ordenado" sin nombrar control del marcado ni repetición.
- Confundir componente con clase CSS: el valor del componente es encapsular **marcado + estilo + comportamiento**, no solo el estilo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Las cuatro decisiones correctas con vocabulario impecable, pero la regla general es genérica y no logra aplicarla a un quinto caso inventado.
- Justificaciones que repiten la documentación palabra por palabra sin un ejemplo propio del daño.
- **Verificación sugerida:** plantéale un **quinto** escenario nuevo (p. ej. "tres tarjetas con la misma estructura en la misma página, marcado tuyo") y pídele la decisión + el porqué. Si entiende el eje, responde "componente" al instante; si copió, duda.

## Feedback sugerido (graduado)
> Nunca entregar la tabla de respuestas completa.
- **Pista (nivel 1):** "Antes de decidir, hazte UNA pregunta primero: ¿el HTML es tuyo o de un tercero/generado? Esa respuesta ya descarta una de las tres salidas."
- **Pregunta socrática (nivel 2):** "Si pones `@apply .btn` en tu botón propio repetido, ¿qué vuelves a tener que no querías: una capa de nombres CSS globales que mantener y que se puede acoplar? ¿No era justo eso lo que utility-first elimina?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa: 1 es marcado tuyo repetido → componente; 2 es único → utilidades; 3 y 4 no son tu marcado → `@apply`. Tu regla debe poner 'control del marcado' como primer filtro. No te doy las frases."

## Conexión con el proyecto / capstone
- Este criterio es el que aplicarás en el [Capstone F4](/fase-4-frontend/proyecto/) cada vez que un elemento se repita: `<Boton>`, `<Mensaje>`, `<Avatar>` serán componentes extraídos, no clases con `@apply`. Es el embrión del razonamiento de [4.9 Design systems](/fase-4-frontend/4-9-design-systems/).
