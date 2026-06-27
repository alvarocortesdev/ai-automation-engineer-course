---
ejercicio_id: fase-4/formulario-accesible
fase: fase-4
sub_unidad: "4.4"
version: 1
---

# Rúbrica — Haz accesible un formulario y deja el test de a11y en verde

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **mixto**: una parte es objetiva
> (el test de a11y pasa o no) y otra es de criterio (foco visible, prueba real con teclado/lector, ARIA
> usada con disciplina). El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota: es un mapa
> de qué observar y cómo dar feedback.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Interfaz operable solo con teclado (orden de foco lógico, foco visible, sin trampas) con HTML
  semántico.
- **O2** — ARIA solo donde el HTML no llega (Primera Regla de ARIA).
- **O3** — Formulario accesible (labels, error anunciado, contraste AA, alt) mapeado a SC de WCAG 2.2.

## Criterios y niveles

### C1 — Semántica y teclado · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sigue habiendo `<div onclick>` como botón; no hay landmark/encabezado; no se puede operar con teclado. |
| **en-progreso** | Hay `<button>` y landmark, pero queda un `tabindex` positivo, o el foco no es visible (`outline: none` sin reemplazo), o el orden de foco no es lógico. |
| **competente** | `<main>` + `<h1>` + `<button>`; orden de foco sigue el DOM; `:focus-visible` con contraste ≥ 3:1; se navega y activa todo con teclado, sin trampas. |
| **excelente** | Además cuida target size (≥ 44px o al menos los 24px de SC 2.5.8), y el alumno demuestra que **probó con teclado de verdad** (lo describe en `decisiones.md`). |

### C2 — ARIA con criterio · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | ARIA ausente donde hace falta (error no anunciado), o ARIA que miente (`<div role="button">`). |
| **en-progreso** | El error se anuncia, pero hay ARIA redundante (`role="navigation"` sobre `<nav>`, `role="button"` sobre `<button>`) o un `aria-label` que pisa el texto visible. |
| **competente** | `role="alert"` + `aria-describedby` en el error (uso legítimo); el `<button>` y los landmarks **sin** ARIA redundante. Aplica la Primera Regla. |
| **excelente** | Sabe nombrar *por qué* cada ARIA está (anuncio dinámico, descripción asociada) y por qué el resto no la lleva; menciona "no ARIA es mejor que mal ARIA" con un ejemplo propio. |

### C3 — Formulario, contraste y alt (DoD punto 7) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Algún campo sin `<label>` asociado (o "label" = placeholder); imagen sin `alt`; error que depende solo del color; test en rojo. |
| **en-progreso** | El test pasa, pero el contraste no se verificó, o la imagen lleva `alt="check"` siendo decorativa (ruido), o el error sigue siendo solo color (sin texto/ícono además). |
| **competente** | Cada control con label asociado; imagen con `alt` correcto según su tipo (decorativa → `alt=""`); error con texto + no solo color; contraste AA verificado. Test verde. |
| **excelente** | El alumno distingue informativa/decorativa/funcional y lo justifica; el error usa ícono **y** texto **y** color (defensa en capas), no solo uno. |

### C4 — Comprensión demostrada (decisiones.md mapea a SC) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `decisiones.md`, o no menciona ningún SC. |
| **en-progreso** | Describe qué hizo pero sin atarlo al SC correcto, o cita SC sin entenderlos. |
| **competente** | Mapea cada arreglo a su SC de WCAG 2.2 con el número correcto (label → 1.3.1; foco → 2.4.7; alt → 1.1.1; error anunciado → 4.1.3...). |
| **excelente** | Conecta los SC con el *por qué* humano (a quién beneficia cada uno) y reconoce alguna tentación de "resolver con ARIA" que evitó. |

## Errores típicos a marcar
- **ARIA que miente:** `<div role="button">` sin foco ni manejo de teclado — el error central de la lección.
- **ARIA redundante:** `role="main"` en `<main>`, `role="navigation"` en `<nav>`, `role="button"` en `<button>`.
- **`placeholder` como label:** campo sin `<label>` asociado (falla 1.3.1 / 4.1.2 aunque "se vea" etiquetado).
- **`outline: none`** sin reemplazo, o `:focus-visible` con un anillo que no contrasta.
- **`tabindex` positivo** para "ordenar" el foco (antipatrón; el orden lo da el DOM).
- **`alt="icono"`** en imagen decorativa (debería ser `alt=""`), o `<img>` sin `alt`.
- **Error solo por color** (borde rojo sin texto ni ícono) — viola SC 1.4.1.
- (transversal seguridad) confiar en `required`/validación del cliente como única barrera: la validación real va también en el servidor (no se pide aquí, pero un "excelente" lo menciona).

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- `decisiones.md` con prosa pulida que cita SC perfectos pero el HTML tiene ARIA redundante: pídele que
  explique, sin mirar, por qué `<nav>` no necesita `role="navigation"`.
- Solución con ARIA sofisticada (`aria-activedescendant`, roles compuestos) impropia del nivel y sin que
  el resto lo justifique: señal de copia. Pídele que diga qué pasa si quita ese atributo.
- Test verde pero no sabe **probar con teclado**: pídele que navegue su propia tarjeta con `Tab` en vivo y
  diga en qué orden recibe foco cada elemento. Si interiorizó la lección, lo hace en segundos.
- **Verificación sugerida:** pedirle que justifique por qué el `<button>` NO lleva `role="button"`.

## Feedback sugerido (graduado)
> Nunca redactar el HTML por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Desenchufa el mouse y navega tu tarjeta con `Tab`. ¿Llegas al botón? ¿Lo activas
  con `Enter`? ¿Ves dónde está el foco? Lo que no puedas hacer con teclado es lo que falta."
- **Pregunta socrática (nivel 2):** "Tu test marca rojo en 'cada campo tiene nombre accesible'. El
  `placeholder` se ve como etiqueta, pero ¿qué pasa cuando el usuario escribe? ¿Qué elemento HTML existe
  justo para dar nombre a un campo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El error no se anuncia porque es un `<div>`
  suelto. Dale un `id` y `role='alert'`, y desde el campo apúntalo con `aria-describedby='ese-id'`. Y el
  `<div class='btn'>` cámbialo por `<button>`: te da foco, teclado, rol y nombre gratis. No te doy el
  código completo: hazlo capa por capa y vuelve a correr el test."

## Conexión con el proyecto / capstone
- Este formulario es un microcosmos del **a11y gate del Capstone F4**: teclado, ARIA quirúrgica y errores
  anunciados son justo lo que su UI de chat/RAG necesita para que **cualquiera** la pueda operar. El
  `decisiones.md` con SC es el germen del checklist de accesibilidad que aplicarás al capstone, y se conecta
  con los estados de primera clase de [4.10] (un error que no se anuncia no es un estado de error útil).
