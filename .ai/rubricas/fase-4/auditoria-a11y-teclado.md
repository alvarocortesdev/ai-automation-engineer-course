---
ejercicio_id: fase-4/auditoria-a11y-teclado
fase: fase-4
sub_unidad: "4.4"
version: 1
---

# Rúbrica — Auditoría de accesibilidad: traza el foco y nombra el SC violado

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **a-mano** (razonamiento): no hay
> test ni una única redacción correcta. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una
> nota: es un mapa de qué observar y cómo dar feedback.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Trazar el orden de foco a mano; identificar inalcanzables y trampas.
- **O2** — Nombrar el SC concreto de WCAG 2.2 que viola cada problema.
- **O3** — Distinguir ARIA mal usada de HTML correcto y priorizar por impacto.

## Criterios y niveles

### C1 — Trazado del orden de foco · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No traza el orden, o lo da "en orden de aparición" ignorando los `tabindex` positivos. |
| **en-progreso** | Traza un orden aproximado, pero no detecta que los `tabindex` positivos (1, 2) van **primero**, o no marca el `<div onclick>` como inalcanzable. |
| **competente** | Orden correcto (los `tabindex` positivos primero, luego el DOM), marca el "Ver detalle" (`<div>`) como inalcanzable y el modal como trampa de foco. |
| **excelente** | Además explica *por qué* el `tabindex` positivo es de por sí un problema (desincroniza foco/visual) y cómo el modal debería gestionar el foco (mover al abrir, atrapar a propósito, devolver al cerrar, `Esc` cierra). |

### C2 — Diagnóstico con SC correcto · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Menos de 5 problemas, o "no es accesible" sin nombrar ningún SC. |
| **en-progreso** | Encuentra ≥ 5 problemas pero ata mal los SC (números equivocados) o solo cita uno o dos. |
| **competente** | ≥ 5 problemas, cada uno con el SC correcto (2.1.1, 2.1.2, 2.4.7, 4.1.2, 1.4.3, 1.4.1, 1.1.1...) y una corrección accionable. |
| **excelente** | Cubre los casos difíciles (trampa de foco 2.1.2, foco tapado 2.4.11, error no anunciado 4.1.3, target size 2.5.8, "solo color" 1.4.1) y las correcciones traen valores/regla (≥ 4.5:1, ≥ 24px). |

### C3 — ARIA y priorización · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No detecta el `<div role="button">` como problema, o no prioriza. |
| **en-progreso** | Detecta la ARIA que miente pero no explica por qué empeora; o el top-3 está sin justificar / por orden de aparición. |
| **competente** | Nombra el `<div role="button">` como ARIA que miente (debe ser `<button>` nativo) y prioriza el top-3 por impacto (bloquea vs. molesta). |
| **excelente** | Conecta con la Primera Regla de ARIA ("no ARIA es mejor que mal ARIA") y prioriza con un eje claro: lo que **impide** usar una función va antes que lo que la degrada. |

## Errores típicos a marcar
- **Trazar el foco "en orden de aparición"** ignorando que `tabindex="1"` y `"2"` se tabulan primero.
- **No marcar la trampa de foco** del modal (es el problema más grave y el más fácil de pasar por alto).
- **Confundir 2.4.7 (foco visible) con 2.4.11 (foco no tapado):** son cosas distintas (invisible vs. tapado por el header).
- **Olvidar el "solo color" (1.4.1)** en el error con borde rojo: el más revelador de criterio.
- **Decir "el botón de engranaje no es accesible"** sin nombrar que le falta **nombre accesible** (4.1.2) → `aria-label`, **y** que su target es muy chico (2.5.8).
- **Priorizar "lo que más molesta"** en vez de "lo que bloquea por completo".
- (transversal) tratar `alt="imagen"` como aceptable: es ruido; o no notar que el gráfico de confianza es **informativo** (necesita `alt` que describa el dato, no `alt=""`).

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Lista de SC perfecta y exhaustiva pero el **orden de foco mal trazado**: la parte que requiere razonar
  paso a paso suele ser la que delata copia. Pídele que trace el orden en voz alta sobre la descripción.
- Cita SC que **no aplican** a la pantalla (p. ej. 1.4.5 imágenes de texto) como relleno: pídele que
  justifique dónde está ese problema en la descripción.
- Correcciones genéricas ("mejorar contraste", "agregar ARIA") sin valores ni mención de HTML nativo:
  pídele que diga el umbral exacto y si la solución es ARIA o un elemento nativo.
- **Verificación sugerida:** pedirle que elija el peor problema y explique a quién deja **completamente
  fuera** y por qué.

## Feedback sugerido (graduado)
> Nunca redactar la auditoría por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Vuelve a trazar el orden de foco: ¿qué pasa con los `tabindex='1'` y `'2'`? ¿Se
  tabulan en el lugar donde están en el HTML, o antes? Y el modal: cuando entras, ¿puedes salir con `Tab` o
  `Esc`?"
- **Pregunta socrática (nivel 2):** "Tienes el contraste y el alt, pero te falta el problema más grave para
  un usuario de teclado. ¿Qué pasa si abro el modal y no tengo mouse? ¿Qué SC describe exactamente eso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El modal es una **trampa de foco** (SC 2.1.2):
  hay que mover el foco al abrir, atraparlo *a propósito* mientras está abierto, dejar que `Esc` cierre, y
  devolver el foco al botón que lo abrió. Y 'Confirmar' como `<div role='button'>` viola 4.1.2 y 2.1.1:
  cámbialo por `<button>`. No te doy la lista completa: recórrela con la checklist de SC y vuelve."

## Conexión con el proyecto / capstone
- Auditar con vocabulario de SC es exactamente lo que harás sobre tu propio **Capstone F4** antes de cruzar
  el a11y gate: el modal con trampa de foco y el `<div role="button">` son errores que aparecen apenas
  agregas interactividad en React ([4.5]). Saber nombrarlos te ahorra reescribir la UI al final.
