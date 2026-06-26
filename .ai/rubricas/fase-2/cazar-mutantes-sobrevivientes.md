---
ejercicio_id: fase-2/cazar-mutantes-sobrevivientes
fase: fase-2
sub_unidad: "2.9"
version: 1
---

# Rúbrica — Caza los mutantes que tu coverage no ve

> Rúbrica **analítica** atada a los `objetivos`. El producto no es "todos los mutantes
> muertos": es la **predicción razonada** (¿supo el alumno, sin ejecutar, dónde estaba
> el agujero?) y los **tests de borde** que lo cierran sin tocar el fuente. Evalúa el
> `mutantes.md` tanto como el `test_descuento.py`. Un alumno puede matar todo copiando
> la pista y seguir sin entender; otro puede dejar un equivalente vivo y haber entendido
> perfectamente. La rúbrica distingue ambos.

## Objetivos evaluados
- **O1** — Predecir, sin ejecutar, qué mutantes sobreviven y por qué viven en los bordes.
- **O2** — Ejecutar mutation testing, leer el score y distinguir killed / survived / equivalente.
- **O3** — Fortalecer la suite con tests de borde que matan a los sobrevivientes sin tocar el fuente.

> Resultado de referencia (el corrector lo sabe; **no se lo da al alumno** salvo al cerrar):
> con la suite débil, **sobreviven M1, M3, M4** (los `>=` → `>` en los bordes 100 y 50) y
> **mueren M2, M5, M6, M7**. Mutation score de partida ≈ **4/7**. Los tres tests de borde
> `descuento(100, True)==30`, `descuento(100, False)==20`, `descuento(50, False)==10` matan
> a los tres sobrevivientes.

## Criterios y niveles

### C1 — Predicción razonada (sin ejecutar) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay predicción en `mutantes.md`, o se corrió `mutmut` primero y se copió su salida (la "predicción" es el resultado). |
| **en-progreso** | Predice algunos mutantes, pero confunde cuáles sobreviven (p. ej. cree que M5/M6/M7 sobreviven), o no explica *por qué* (qué caso los distingue). |
| **competente** | Predice correctamente que M1, M3, M4 sobreviven y M2, M5, M6, M7 mueren, ligando cada sobreviviente al **borde no probado** (100, 50). |
| **excelente** | Además articula la regla general: "un mutante de comparación solo muere con un test en el borde exacto; uno de valor de retorno muere con cualquier aserción del retorno". |

### C2 — Lectura del mutation testing · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió `mutmut`, o no reporta el resultado real. |
| **en-progreso** | Corrió `mutmut` pero no contrasta con su predicción, o no entiende el score (lo confunde con coverage). |
| **competente** | Reporta el score real, contrasta con su predicción y nombra dónde acertó/falló. Entiende que `mutmut` genera más mutantes que los 7 y que eso no invalida nada. |
| **excelente** | Identifica si quedó algún mutante **equivalente** y argumenta por qué no se puede matar, en vez de forzar una aserción absurda para "llegar a 100%". |

### C3 — Tests de borde que matan (corrección) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó tests, o modificó `descuento.py`, o debilitó/borró tests existentes. |
| **en-progreso** | Agregó tests pero no en el borde exacto (p. ej. `descuento(101, ...)` en vez de `100`), así que algún sobreviviente sigue vivo. |
| **competente** | Agregó los tres tests de borde (100 socio, 100 no-socio, 50); `mutmut` ya no reporta sobrevivientes no-equivalentes; `descuento.py` intacto. |
| **excelente** | Tests de borde con nombres que explican qué distinguen (`test_borde_100_socio_vs_no_socio`), y nota explícita de que el line coverage no cambió (sigue 100%). |

## Errores típicos a marcar
- **Correr `mutmut` antes de predecir**: invalida O1 aunque el resto esté bien. La predicción es el músculo.
- **Modificar `descuento.py`** para "arreglar" algo: el código está correcto; el agujero está en los tests.
- **Agregar tests fuera del borde** (`99`, `101`, `51`) creyendo que matan el mutante `>=`→`>`: solo el valor **exacto** del umbral lo distingue.
- **Confundir coverage con mutation score**: "subí el coverage" cuando ya estaba en 100%; lo que subió fue el score.
- **Perseguir 100% de mutation score** matando mutantes equivalentes con aserciones artificiales.
- (transversal testing) agregar un test que llama a `descuento` sin afirmar el resultado para "cubrir" — no mata ningún mutante.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `mutantes.md` con la tabla perfecta pero `test_descuento.py` sin los tests de borde (o al revés): la explicación no calza con el código.
- Predicción correctísima de los 7 sin ningún error ni duda, junto a un alumno que no puede decir qué caso distingue `>=` de `>`.
- Tests con abstracciones impropias del nivel (fixtures elaboradas, hypothesis) que el ejercicio no pide.
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué pasa si el umbral fuera `puntos > 50` (en vez de `>=`) y qué test cambiaría. Si trazó de verdad, lo resuelve al instante.

## Feedback sugerido (graduado)
> Nunca dar los tests de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tus tests usan 150, 70, 10 puntos. ¿Alguno usa *exactamente* 100 o 50? El mutante `>=` → `>` solo se nota en ese punto exacto."
- **Pregunta socrática (nivel 2):** "Con el código correcto, ¿cuánto da `descuento(100, False)`? ¿Y si cambio `>= 100` por `> 100` en la segunda línea? Si esos dos números difieren, ¿qué test los separaría?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Los sobrevivientes son los tres `>=` en los bordes 100 y 50. Agrega un test por cada borde exacto: `descuento(100, True)`, `descuento(100, False)`, `descuento(50, False)`, con el valor que devuelve el código **correcto**. Re-corre `mutmut`. Repasa la sección 4.3 de la lección."

## Conexión con el proyecto / capstone
- Es el ensayo en pequeño del **Capstone F2 (Refactor + suite de tests)**, cuyo DoD exige medir calidad por **mutation score / aserciones reales, no por % de coverage**. Y es el mismo músculo que en la Fase 6 te hará exigir un **eval harness** antes de confiar en una salida de LLM: medir la fuerza real, no el teatro de la métrica.
