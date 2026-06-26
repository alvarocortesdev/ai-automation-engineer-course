---
ejercicio_id: fase-2/depurar-con-stack-trace-y-pdb
fase: fase-2
sub_unidad: "2.12"
version: 1
---

# Rúbrica — Caza el bug con método: stack trace → pdb → test de regresión

> Rúbrica **analítica** atada a los `objetivos`. El núcleo de este ejercicio NO es el
> fix (es una línea): es el **método**. Evaluar que el alumno (1) leyó el stack trace,
> (2) confirmó la causa con el debugger en vez de adivinar, (3) escribió un test de
> regresión que falló ANTES del fix, y (4) arregló la causa raíz sin "arreglar de paso"
> el comportamiento del `tipo` desconocido. La evidencia vive en `traza.md`.

## Objetivos evaluados
- **O1** — Leer un stack trace de abajo hacia arriba: tipo+mensaje de la excepción y frame exacto del propio código.
- **O2** — Depurar con método: reproducir, hipótesis, confirmar con pdb inspeccionando estado; test de regresión rojo primero.
- **O3** — Arreglar solo la causa raíz; registrar el comportamiento raro (`tipo` desconocido) como deuda separada (dos sombreros).

## Criterios y niveles

### C1 — Lectura del stack trace · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `traza.md` no contiene el trace, o lo "arregló" sin nombrar el tipo de excepción ni la línea. |
| **en-progreso** | Pegó el trace pero no identifica el frame exacto de `solucion.py` ni qué significa `ValueError: max() ... is empty`. |
| **competente** | Identifica tipo (`ValueError`), mensaje (secuencia vacía a `max()`) y el frame exacto (`resumen_cuenta`, la línea de `max(cargos)`); distingue el DÓNDE (su frame) del contexto (quién llamó). |
| **excelente** | Además explica explícitamente que se lee de abajo hacia arriba y por qué `app.py`/el caller es contexto y no causa. |

### C2 — Método de depuración + test de regresión rojo · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay rastro de pdb ni de hipótesis; "lo arreglé" sin proceso. O el fix llegó antes que cualquier test. |
| **en-progreso** | Hay hipótesis pero la confirmó con `print`, no con el debugger; o el test de regresión existe pero nunca lo vio fallar (lo escribió ya verde). |
| **competente** | Hipótesis falsable + sesión de pdb con comandos (`p cargos` → `[]`, `w`) en `traza.md`; test de regresión que **falló primero** y ahora pasa; `test_caso_normal_funciona` sigue verde. |
| **excelente** | Usa post-mortem (`-c continue` / `pdb.pm()`) o breakpoint con criterio; declara la decisión de diseño `0` vs `None` con su razón; el test fija esa decisión. |

### C3 — Causa raíz y dos sombreros · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Arregló" con `try/except` que traga el error (parche de síntoma), o reescribió la función, o "corrigió" de paso el `tipo` desconocido (cambió comportamiento ajeno). |
| **en-progreso** | Fix de causa raíz correcto, pero no menciona la deuda del `tipo` desconocido en `traza.md`. |
| **competente** | Fix mínimo de causa raíz (`max(..., default=...)` o equivalente); deja la deuda del `tipo` desconocido **anotada** (xfail + nota en `traza.md`), sin tocarla. |
| **excelente** | Articula los dos sombreros como flujo: el bug #412 va en este commit; la deuda del desconocido va con su propio ticket y test futuro. |

## Errores típicos a marcar
- **Parchear el síntoma**: `try/except ValueError: return 0` apaga el error pero se traga cualquier otro `ValueError` real → bug silencioso peor que el original.
- **Adivinar en vez de confirmar**: arreglar apenas se lee el mensaje, sin inspeccionar que `cargos == []`. (A veces aciertas; el hábito te traiciona en el bug difícil.)
- **Test de regresión escrito ya verde**: si nunca lo vio fallar, no prueba que entendió el bug.
- **Leer el trace al revés** (de arriba hacia abajo) y culpar a `app.py`/al caller en vez de al frame del fallo.
- **"Arreglar" el `tipo` desconocido** dentro de este ticket: cambia comportamiento que nadie pidió (sombrero equivocado).
- (transversal observabilidad) no dejar el test de regresión en la suite → el bug puede volver sin que nadie se entere.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `solucion.py` arreglado y test "perfecto" entregados juntos, con `traza.md` vacío o genérico (sin el valor real de `cargos`, sin comandos de pdb): la IA encontró el bug, el alumno no.
- `traza.md` con jerga impecable ("post-mortem", "root cause") pero sin un solo dato observado del estado real.
- Fix sofisticado (refactor entero, manejo elaborado) impropio de un cambio de una línea: olor a "que la IA lo reescriba".
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué imprime `p cargos` en el frame del crash, y qué devuelve hoy `resumen_cuenta` con un movimiento `{"tipo": "comision", "monto": 200}` (debe razonar que el monto simplemente no se suma a ningún lado).

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Lee la última línea del trace: ¿qué tipo de excepción es y qué le pasó a `max()`? Antes de arreglar, párate en ese frame con pdb y mira el valor de `cargos`."
- **Pregunta socrática (nivel 2):** "Si envuelves `max()` en un `try/except` que devuelve 0, ¿qué pasa el día que `cargos` tenga un dato corrupto que también lance `ValueError`? ¿Estás arreglando la causa o escondiendo el síntoma?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "La causa es `max([])`, que no tiene valor. Python da un mecanismo para 'máximo, o un default si está vacío' — búscalo en la firma de `max`. Escribe primero el test que reproduce #412 y míralo fallar; recién entonces aplica el fix de una línea. El `tipo` desconocido NO es este ticket: déjalo anotado. Repasa las secciones 4.2–4.5 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el método con el que entrarás a tu propio código viejo en el **Capstone F2**: reproducir, localizar, confirmar, test de regresión, fix de causa raíz. El test que dejas en la suite es la evidencia de calidad que el capstone pide, y el ensayo de la observabilidad de la Fase 5.
