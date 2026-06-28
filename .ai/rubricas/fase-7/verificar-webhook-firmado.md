---
ejercicio_id: fase-7/verificar-webhook-firmado
fase: fase-7
sub_unidad: "7.2"
version: 1
---

# Rúbrica — Verifica un webhook firmado (HMAC + anti-replay)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay tests automáticos
> (`test_verificador.py`): el verde es condición **necesaria, no suficiente**. El corrector
> evalúa además la **comprensión de seguridad** (¿por qué body crudo? ¿por qué `compare_digest`?
> ¿qué ataque previene el anti-replay?). Un alumno puede pasar los tests copiando el esquema sin
> entender ninguno de los tres riesgos; eso es `competente` a lo sumo, nunca `excelente`.

## Objetivos evaluados

- O1: Verificar la firma HMAC-SHA256 sobre el body crudo, recomputando sobre `t.payload`.
- O2: Comparar en tiempo constante (`hmac.compare_digest`).
- O3: Aplicar anti-replay (rechazar firma válida pero vieja), verificando la firma antes que la frescura.

## Criterios y niveles

### C1 — Corrección de la verificación · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; falta un estado (p. ej. nunca devuelve `MALFORMADO`) o devuelve `VALIDO` con firma incorrecta. |
| **en-progreso** | Pasa la mayoría pero falla un caso (típico: no maneja la cabecera malformada, o confunde `EXPIRADO` con `FIRMA_INVALIDA`). |
| **competente** | Los 10 tests en verde; los cuatro estados correctos; recomputa sobre `f"{t}.".encode() + payload`. |
| **excelente** | Además, verifica la firma **antes** que la frescura con intención explicada, y maneja un caso propio significativo (timestamp futuro fuera de tolerancia). |

### C2 — Seguridad (el corazón del ejercicio) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Usa `==` para comparar firmas, o firma sobre un dict/JSON re-serializado, o no hay anti-replay. |
| **en-progreso** | Usa `compare_digest` pero no sabe explicar qué ataque previene; o tiene anti-replay sin entender que protege contra reenvío, no contra manipulación. |
| **competente** | Body crudo + `compare_digest` + anti-replay, los tres presentes y correctos. |
| **excelente** | Explica con precisión los tres riesgos: re-serializar rompe el HMAC; `==` filtra por timing; sin firmar `t` una captura legítima es reproducible. Distingue integridad (HMAC) de frescura (anti-replay). |

### C3 — Calidad de testing (hilo transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No añadió ningún test propio. |
| **en-progreso** | Añadió un test trivial (repite un caso existente con otros bytes). |
| **competente** | Añadió un caso borde real (timestamp futuro, o `v1` vacío). |
| **excelente** | El caso propio prueba algo que los tests dados no cubren y lo justifica (p. ej. tolerancia simétrica para relojes adelantados). |

## Errores típicos a marcar

- Verificar sobre el JSON parseado/re-serializado en vez del body crudo en `bytes` (la firma nunca coincidiría con un emisor real).
- Comparar firmas con `==` en lugar de `hmac.compare_digest` (timing attack).
- Firmar solo el `payload` sin el `t` → no hay anti-replay posible.
- Comprobar la frescura **antes** que la firma (confía en un `t` que un atacante pudo inventar).
- No envolver el parseo de la cabecera en manejo de errores → revienta con `KeyError`/`ValueError` en vez de devolver `MALFORMADO`.
- (transversal) Pasar los tests sin poder explicar qué ataque concreto previene cada defensa.

## Señales de dependencia-IA

- Verificador impecable y genérico, pero el alumno no puede explicar por qué se firma `t.payload` ni qué es un timing attack.
- Manejo de casos sospechosamente sofisticado (varios esquemas de versión `v1`/`v2`, rotación de secretos) impropio del nivel e indefendible.
- Comentarios que describen *qué* hace cada línea pero no *por qué* el body crudo importa.
- **Verificación sugerida:** pedir que explique, sin notas, por qué `json.dumps(await request.json())` rompería la verificación. Si trazó de verdad, lo explica; si dependió de la IA, se traba.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre mentalmente el caso del payload manipulado: ¿qué bytes entran al HMAC del emisor y cuáles a tu cálculo? ¿De qué tipo es `payload` en tu función?"
- **Pregunta socrática (nivel 2):** "Si un atacante captura un webhook legítimo con su firma válida y lo reenvía mañana, ¿tu función lo aceptaría? ¿Qué le falta a lo que firmas para que no pueda?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Recomputa el HMAC sobre `f"{t}.".encode() + payload` con el secreto, compara con `hmac.compare_digest` (no `==`), y solo si la firma es válida compara `abs(ahora - t)` con la tolerancia. Verifica autenticidad antes de confiar en el timestamp. Revisa la sección 4.4 de la lección."

## Conexión con el proyecto / capstone

- Este verificador es el **guardián de la entrada** del [capstone F7](/fase-7-automatizacion/proyecto/): nadie inyecta un input falso que dispare una acción del agente. Es el punto 6 del Definition of Done (validación antes de ejecutar) aplicado a la frontera del sistema.
