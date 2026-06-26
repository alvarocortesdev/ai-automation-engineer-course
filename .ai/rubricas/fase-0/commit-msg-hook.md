---
ejercicio_id: fase-0/commit-msg-hook
fase: fase-0
sub_unidad: "0.6"
version: 1
---

# Rúbrica — Construye el hook commit-msg (Conventional Commits)

> Rúbrica analítica para un ejercicio de **código** con tests. Se evalúa que el hook cumpla el contrato (los tests), pero sobre todo que el alumno **entienda su regex** y el mecanismo del hook. Un hook que pasa los tests pero que el alumno no puede explicar pieza por pieza es una bandera roja (probable IA-generado).

## Objetivos evaluados
- **O1** — El hook acepta/rechaza correctamente vía código de salida (cumple los tests).
- **O2** — La regex codifica fielmente la spec (type, scope opcional, breaking `!`, descripción).
- **O3** — Trabaja con tests como contrato (verde) y añade un caso borde propio.

> El corrector conoce la solución de referencia (`.ai/soluciones/fase-0/commit-msg-hook.md`). **No la pega**; la usa para calibrar.

## Criterios y niveles

### C1 — Corrección (cumple el contrato) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El hook no corre, sale siempre 0 (acepta todo) o siempre ≠0 (rechaza todo); tests en rojo. |
| **en-progreso** | Pasa algunos tests pero falla casos clave (no deja pasar `Merge`/`Revert`, o acepta `feat:` sin descripción, o rechaza un scope válido). |
| **competente** | Todos los tests pasan: válidos→0, inválidos→≠0, `Merge`/`Revert`→0, ayuda a stderr. |
| **excelente** | Además maneja bordes no exigidos con criterio (mensaje vacío, solo comentarios, espacios) y la ayuda de error es genuinamente útil (formato + ejemplos). |

### C2 — Calidad de la regex y del script · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa regex (compara strings sueltos) o la regex no está anclada (`^…$`) y "valida" por coincidencia parcial. |
| **en-progreso** | Regex anclada pero floja: tipos incompletos, scope mal escapado (`(` literal sin `\(`), o no exige la descripción tras `: `. |
| **competente** | Regex ERE anclada que cubre tipos válidos, scope opcional escapado, `!` opcional y descripción no vacía; script con `set -euo pipefail` y salida limpia. |
| **excelente** | Script legible y comentado; separa "dejar pasar autogenerados" de "validar formato"; sin dependencias frágiles (extrae la cabecera sin pipes que rompan con cuerpos multilínea). |

### C3 — Disciplina de tests (TDD) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió los tests, o "ajustó los tests" para que pasen en vez de arreglar el hook. |
| **en-progreso** | Usa los tests dados pero no añadió ninguno propio, o el añadido es trivial (duplica un caso existente). |
| **competente** | Tests verdes + **un caso borde propio real** (scope con guion, descripción larga, `feat:x` sin espacio). |
| **excelente** | El caso propio revela una decisión de diseño defendida (ej. ¿se permite scope vacío `feat(): x`? lo prueba y justifica). |

### C4 — Seguridad / criterio (transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **en-progreso** | No considera que el hook se comparte vía `core.hooksPath` (lo deja solo en `.git/hooks`, que no se versiona). |
| **competente** | Entiende que el hook va a `.githooks/` versionado + `git config core.hooksPath .githooks`. |
| **excelente** | Comenta que un hook se puede saltar con `--no-verify`, por lo que la validación **real** debe repetirse en CI (no confiar solo en el hook local). |

## Errores típicos a marcar
- **Regex sin anclar:** `grep -E 'feat'` da match con "manifeats algo"; falta `^…$`.
- **Paréntesis del scope sin escapar:** en ERE `(` es grupo; el literal es `\(`.
- **Aceptar `feat:` vacío:** olvidar exigir `: ` + al menos un carácter (`.+` o `.{1,N}`).
- **Bloquear merges:** no exceptuar `Merge `/`Revert ` autogenerados rompe `git merge`.
- **Ayuda a stdout en vez de stderr:** los mensajes de error van a `>&2`.
- **Leer `$1` como el texto del mensaje:** Git pasa la **ruta** del archivo, hay que leerlo.
- (transversal) **Editar los tests** para forzar verde en lugar de arreglar el hook.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Regex correcta y sofisticada que el alumno no puede desglosar (no sabe por qué `\(` o por qué `^…$`).
- Comentarios o estilo muy por encima del nivel F0 (manejo de `trap`, validación de footers BREAKING CHANGE no pedida) sin poder explicarlos.
- Tests propios ausentes o genéricos pese a un hook "perfecto".
- **Verificación sugerida:** pedir que, sin IA, modifique la regex para **también** aceptar el footer `BREAKING CHANGE:` en el cuerpo, o que explique qué hace `(!)?`. Si entendió, lo resuelve; si dependió de IA, se traba.

## Feedback sugerido (graduado)
> Nunca pegar la regex de la solución de referencia.
- **Pista (nivel 1):** "Corre solo el test que falla y mira el mensaje que recibió el hook. ¿Tu patrón está anclado al inicio y al final de la línea?"
- **Pregunta socrática (nivel 2):** "¿Qué carácter, en `grep -E`, hace que `(` signifique 'grupo' en vez de 'paréntesis literal'? ¿Cómo afecta eso a tu scope `(parser)`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa el problema en dos: primero un `if` que deje pasar `Merge `/`Revert `; luego una única regex anclada con `^(tipos)(scope opcional)(! opcional): descripción$`. Prueba la regex aislada con `echo 'feat: x' | grep -E '...'` antes de meterla al hook."

## Conexión con el proyecto / capstone
- Este hook es un **entregable directo** del Definition of Done del **Capstone F0 — CLI sin IA**: "Conventional Commits en todo el historial", aquí forzado por una máquina. Reaparece como gate de calidad en cada capstone posterior y conecta con los gates de CI de la Fase 5.
