---
ejercicio_id: fase-2/index
fase: fase-2
sub_unidad: "2.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio no
> tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de qué
> observar. Úsalo como vara de medir honestidad/realismo/agudeza, nunca como
> plantilla a copiar (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico de hábitos y plan de Fase 2

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier conjunto
de tres archivos que sea **honesto, concreto y agudo**: diagnóstico defendible,
plan sostenible, y *gap report* que **ve** los hábitos faltantes sin reescribir el
código. La calidad se mide por proceso, no por contenido específico.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar (alumno cero real)
Tabla con las 13 sub-unidades. En un cero real en ingeniería de software, lo
esperable es mayoría de `nuevo` con algún `lo reconozco` (p. ej. quien ya escribió
algún test suelto en la Fase 1). La señal de calidad es la **razón por fila** y la
aplicación consistente de la prueba "¿podría resolverlo sin notas ahora?".

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 2.1 DSA nivel trabajo | nuevo | Nunca razoné Big-O ni resolví problemas tipo entrevista. |
| 2.2 Clean code | lo reconozco | Intuyo "buenos nombres", pero sin criterio explícito. |
| 2.3 Code smells + refactoring | nuevo | No conozco el catálogo de Fowler. |
| 2.4 SOLID con crítica | nuevo | Escuché las siglas, no las apliqué. |
| 2.5 Patrones de diseño | nuevo | Sé que existen, no los he usado. |
| 2.6 Testing fundamentos | lo reconozco | Escribí un test en pytest en la 1.6, nada más. |
| 2.7 TDD obligatorio | nuevo | Nunca escribí el test *antes* del código de forma sistemática. |
| 2.8 Diseño de tests | nuevo | No distingo mock/stub/spy/fake. |
| 2.9 Coverage vs mutation | nuevo | Creía que más coverage = mejor. |
| 2.10 Playwright e2e | nuevo | Nunca automaticé el navegador. |
| 2.11 Testing de código LLM | nuevo | No sé cómo mockear una respuesta de modelo. |
| 2.12 Debugging y legado | lo reconozco | Uso `print`; nunca un debugger en serio. |
| 2.13 Colaboración + ADRs | lo reconozco | Hago commits; nunca escribí un ADR. |

> Para un perfil **oxidado-con-experiencia**, lo esperable es más `lo reconozco` y
> algún `lo sé hacer sin notas` — pero solo si lo puede defender. La trampa a
> detectar es "lo sé hacer" en TDD o mutation testing sin evidencia (clásico:
> "escribí tests" ≠ "hago TDD" ≠ "mido mutation score").

### `plan-fase-2.md` — exemplar
Un plan creíble, p. ej.:
- **Lun/Mié/Vie 20:00–20:45** (3 bloques × 45 min) + **Sáb 10:00–11:30** (sesión larga).
- **Interleaving de DSA:** 1 problema de DSA al inicio de cada bloque (calentamiento),
  no las 15–20 piezas seguidas en una semana. Distribuidos también con fases posteriores.
- **Orden con sentido:** la red de tests (2.6) antes de los refactors (2.3) y del capstone.
- **Ritual de repaso:** cada sesión arranca con 5 min reescribiendo de memoria lo
  del bloque anterior; los sábados, repaso de toda la semana.

La señal de calidad: **día/hora concretos**, **interleaving explícito de DSA** y un
**ritual de repaso**, no "estudiaré ~10 h por semana".

### `habitos-faltantes.md` — exemplar del *gap report*
Lo importante: **nombra el hueco, no lo arregla**. Un *gap report* `competente`
para `def calc(x, y)` cubre al menos cuatro de estos, cada uno mapeado:

| Hábito faltante | Por qué importa | Sub-unidad |
|---|---|---|
| Nombres opacos (`calc`, `x`, `y`) | No se entiende qué hace sin leer el cuerpo. | 2.2 |
| *Magic numbers* (`100`, `50`, `0.1`, `0.05`) | Significado solo en la cabeza del autor; cambio frágil. | 2.3 |
| Sin tests | No hay forma de saber si es correcto ni de refactorizar con seguridad. | 2.6–2.7 |
| Frontera ambigua (`y == 100`, `y == 50`) | ¿`>` o `>=`? Solo un test lo fija; hoy es una apuesta. | 2.8–2.9 |
| Sin spec/ADR de los umbrales | *Por qué* 100 y 0.1 se pierde cuando el autor se va. | 2.13 |
| (extra) Sin manejo de borde (`x` negativo, `y` no-entero) | Entradas inesperadas → resultado silenciosamente raro. | 2.8 (property-based) |

Un *gap report* `excelente` añade la observación meta: **no se puede refactorizar
esto con seguridad hasta tener la red de tests**, porque refactorizar es cambiar la
estructura sin cambiar el comportamiento, y eso solo se afirma con tests verdes.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Reescribir en vez de diagnosticar.** Es el error central. Si el alumno entregó
   una versión "arreglada" de `calc`, hizo el ejercicio equivocado: el objetivo es
   *ver* el hueco, no taparlo (y menos sin tests). Marcar y reconducir.
2. **Sobreconfianza en el diagnóstico.** "Lo sé hacer" en TDD/mutation sin evidencia.
   Verificación: que justifique una fila en voz alta.
3. **Gap report superficial.** Solo "faltan tests". Falta ver nombres, magic numbers,
   frontera y ADR. Empujar con la pista nivel 1.
4. **Plan sin interleaving ni repaso.** El curso vive del *spacing* y del *interleaving*
   de DSA; un plan sin ambos no cumple O2.
5. **Mapeo incorrecto de sub-unidades.** P. ej. mandar "magic numbers" a testing en vez
   de a code smells (2.3). Corregir el mapa, no penalizar de más si el hueco está bien visto.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables están
  y son honestos/concretos/agudos. No exigir la tabla exacta de arriba.
- El *gap report* no necesita los seis huecos: **cuatro distintos, bien mapeados y sin
  reescribir** ya es `competente`. Detectar la frontera `>`/`>=` o la dependencia
  refactor↔tests lo lleva a `excelente`.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se evalúa la **calidad
  del proceso** (autoevaluación + planificación + ver-el-hueco), no el nivel de partida.
- Un plan **modesto pero sostenible** es preferible (y mejor calificado) que uno
  ambicioso e irreal. Premiar realismo.
- Es válido —y `excelente`— que un perfil oxidado marque varias sub-unidades como
  dominadas, **si** acompaña con cómo lo va a *validar* (resolver un ejercicio sin IA),
  no con saltarlas a ciegas.
