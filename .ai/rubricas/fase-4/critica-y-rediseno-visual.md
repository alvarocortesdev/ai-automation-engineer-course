---
ejercicio_id: fase-4/critica-y-rediseno-visual
fase: fase-4
sub_unidad: "4.3"
version: 1
---

# Rúbrica — Crítica de diseño: nombra la heurística, no el gusto

> Rúbrica **analítica** para un ejercicio de **razonamiento/diseño** (sin tests). Lo que se evalúa es la
> **precisión del diagnóstico** y la **calidad de la priorización**, no que coincida palabra por palabra
> con la solución de referencia. Dos alumnos pueden redactar críticas distintas y ambos estar `excelente`
> si nombran la heurística correcta y proponen una corrección defendible. El corrector busca **criterio**,
> no conformidad.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Diagnosticar nombrando palanca + heurística concreta por problema (no juicio de gusto).
- **O2** — Proponer una corrección accionable por problema (valor o regla).
- **O3** — Priorizar por impacto en legibilidad y accesibilidad.

## Criterios y niveles

### C1 — Cobertura y precisión del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 5 problemas, o juicios de gusto ("se ve feo", "no me gusta") sin nombrar heurística. |
| **en-progreso** | 5+ problemas pero algunos sin la heurística exacta (dice "espaciado raro" en vez de "ley de proximidad"), o no cubre las cinco palancas. |
| **competente** | ≥ 5 problemas, cada uno con palanca + heurística concreta correcta; entre todos cubre las cinco palancas. |
| **excelente** | Además distingue varias violaciones dentro de una misma palanca (p. ej. en color: contraste insuficiente **y** "información solo por color" **y** demasiados acentos), y las separa con nitidez. |

### C2 — Correcciones accionables · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Arreglar el espaciado" sin decir cómo; correcciones vagas. |
| **en-progreso** | Corrige pero sin valores ni reglas ("poner más contraste" sin el umbral 4.5:1). |
| **competente** | Cada corrección es concreta y verificable (un valor, una regla, un umbral): "subir el contraste del texto de ayuda a ≥ 4.5:1, p. ej. #595959". |
| **excelente** | Las correcciones son coherentes entre sí (proponen un sistema: una escala, una jerarquía de acciones), no parches sueltos. |

### C3 — Priorización por impacto · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay top-3, o es el orden de aparición de la lista. |
| **en-progreso** | Hay top-3 pero la justificación es débil o subjetiva ("este me molesta más"). |
| **competente** | Top-3 justificado por impacto en legibilidad/accesibilidad; al menos uno es de contraste/accesibilidad. |
| **excelente** | Pondera explícitamente los dos ejes (¿rompe la jerarquía? ¿rompe la accesibilidad?) y pone primero lo que falla ambos. |

## Errores típicos a marcar
- **Juicio de gusto en vez de heurística:** "se ve desordenado" sin nombrar proximidad/alineación/escala.
- **Confundir síntoma con causa:** "el texto se pierde" (síntoma) sin nombrar la longitud de línea sin
  `max-width` o el `line-height: 1.0` (causa).
- **Pasar por alto el contraste:** no detectar que `#c4c4c4` sobre blanco no pasa AA, o que `#dcdcdc`/`#9a9a9a` del botón primario es ilegible.
- **No ver la "información solo por color":** el error que se comunica únicamente con borde rojo (sin
  ícono ni texto) es una falla de accesibilidad clásica; si no la marca, falta criterio.
- **Top-3 por orden de aparición** en vez de por impacto.
- **No notar la jerarquía de acciones rota:** el botón primario "Guardar" se ve deshabilitado.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Lista exhaustiva y "perfecta" con vocabulario de heurísticas que el alumno no puede ejemplificar con
  *otra* pantalla: pídele que critique en voz alta una interfaz nueva (su correo, su banco) en 2 minutos.
- Correcciones con valores hex/px sospechosamente precisos pero sin relación entre sí (parches, no
  sistema): pregunta por qué eligió esos valores.
- Top-3 con justificación genérica que no menciona los dos ejes concretos.

## Feedback sugerido (graduado)
> Nunca redactar la crítica por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Recorre la pantalla palanca por palanca con la checklist. En 'color' hay más de un
  problema: ¿cuántos distingues?"
- **Pregunta socrática (nivel 2):** "El error se muestra solo con un borde rojo. ¿Qué pasa con alguien que
  no distingue el rojo? ¿Qué heurística de accesibilidad cubre eso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu diagnóstico nombra 'espaciado raro', pero
  el problema preciso es que la etiqueta está más cerca del campo de abajo que del suyo: eso es la **ley de
  proximidad** invertida. Renómbralo así y propón la corrección en términos de la escala de espaciado."

## Conexión con el proyecto / capstone
- Diagnosticar con precisión es lo que el alumno hará al revisar su propia UI del **Capstone F4** contra el
  a11y gate de [4.4] y al pedir mejoras a la IA. Nombrar el problema es el prerrequisito de arreglarlo.
