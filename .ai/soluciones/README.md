# `.ai/soluciones/` — Soluciones de referencia (SPOILER)

> ⚠️ **Material para el CORRECTOR, no para el alumno.** Cada archivo aquí es la solución de referencia de un ejercicio: la **vara de medir** que el corrector usa para detectar errores y graduar pistas. El alumno **no** debe leerlas hasta haber cerrado su intento.

## Para qué sirven

- Le dan al corrector un **patrón correcto** contra el cual contrastar la entrega del alumno.
- Documentan **el porqué** (no sólo el qué): el razonamiento, los trade-offs, los puntos resbalosos. Eso permite al corrector explicar, no sólo marcar.
- Hacen la corrección **consistente entre IAs distintas**: cualquier modelo llega al mismo veredicto.

## Reglas (las hace cumplir `INSTRUCCIONES-CORRECTOR.md`)

1. El corrector lee la solución de referencia **al final**, cuando ya formó su propio juicio —para no anclarse ni filtrarla.
2. **Prohibido** pegar, parafrasear de forma reconstruible, o mostrar el código de la solución al alumno.
3. Se usa sólo para: detectar el error, nombrar la misconception, y calibrar las pistas graduadas.
4. Si el alumno exige la solución, ver §6 de las instrucciones: nunca el archivo completo; a lo sumo el fragmento conceptual mínimo, y sólo tras un intento genuino documentado.

## Convención y formato

- Una solución por ejercicio: `.ai/soluciones/<fase>/<slug>.md` (mismo `<slug>` que la rúbrica y el enunciado).
- Cada solución abre con un banner `> 🚫 SPOILER` y su `ejercicio_id` en el frontmatter.
- Estructura recomendada: **respuesta canónica** → **razonamiento paso a paso** → **puntos resbalosos / variantes** → **rango de soluciones aceptables** (qué enfoques distintos también son correctos, para que el corrector no penalice un camino válido).
- Si un ejercicio no necesita solución de referencia (p. ej. reflexión abierta), se marca en el contrato con `paths: { solucion_referencia: null }` y no se crea archivo.
