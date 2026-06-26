---
ejercicio_id: fase-3/verificar-jwt-a-mano
fase: fase-3
sub_unidad: "3.12"
version: 1
---

# Rúbrica — Verifica un JWT a mano

> Rúbrica analítica para un ejercicio de **código de seguridad**. Lo que se evalúa no es solo que `pytest`
> pase, sino el **orden de defensa** y las dos decisiones que separan un verificador correcto de uno
> peligroso: fijar el algoritmo (no confiar en el token) y comparar la firma en tiempo constante. Un alumno
> puede pasar todos los tests y aun así tener un modelo mental roto (p. ej. comparar con `==`): la bitácora
> lo revela.

## Objetivos evaluados
- **O1** — Implementar la verificación HS256 a mano (estructura → algoritmo → firma → exp), sin PyJWT.
- **O2** — Explicar que la firma da integridad/autenticidad, no confidencialidad; y que el `alg` se fija al validar.
- **O3** — Comparar firmas en tiempo constante y verificar la firma antes de confiar en los claims.

> Los 9 tests pasan con la solución de referencia. El corrector conoce el resultado; **no se lo adelanta** al alumno.

## Criterios y niveles

### C1 — Corrección de la verificación · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No verifica firma, o devuelve los claims sin validar nada; varios tests en rojo. |
| **en-progreso** | Pasa algunos tests pero falla casos clave: no rechaza `alg: none`, o no maneja la estructura malformada/base64 inválido. |
| **competente** | Los 9 tests en verde; las cuatro defensas presentes (estructura, alg, firma, exp). |
| **excelente** | Además ordena bien las defensas (firma antes de exp), maneja header/claims no-dict sin reventar, y añadió un caso borde propio significativo. |

### C2 — Seguridad de la implementación · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Compara la firma con `==`; o decide el algoritmo leyendo el `alg` del token sin restringirlo. |
| **en-progreso** | Usa `==` pero al menos restringe el algoritmo; o usa `compare_digest` pero lee `exp` antes de validar la firma. |
| **competente** | `hmac.compare_digest` para la firma + algoritmo fijado a `HS256` + firma verificada antes de `exp`. |
| **excelente** | Lo anterior + lo explica en la bitácora con el porqué (timing attack, `alg:none`, no confiar en claims no firmados). |

### C3 — Comprensión demostrada (bitácora calza con el código) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `bitacora.md`, o no responde las tres preguntas. |
| **en-progreso** | Responde superficial ("porque es más seguro") sin nombrar el mecanismo. |
| **competente** | Explica con precisión por qué firma-antes-de-exp, por qué fijar el alg, y por qué `compare_digest`. |
| **excelente** | Conecta con la lección: la firma no cifra (payload legible) → no meter datos sensibles; el secreto es lo más sensible del backend. |

## Errores típicos a marcar
- **Comparar la firma con `==`** en vez de `hmac.compare_digest`: filtra información por timing. Marca aunque los tests pasen.
- **Leer el `alg` del token para elegir cómo verificar**: la puerta del ataque `alg: none`. El algoritmo se fija en el código.
- **Validar `exp` antes que la firma**: confiar en un claim de un token aún no autenticado.
- **Re-decodificar el payload y firmar sobre los bytes decodificados**: el `signing_input` es el texto base64 (`h_b64.p_b64`), no el JSON decodificado. Si el alumno re-serializa el JSON, la firma no cuadrará (los separadores cambian).
- **Tratar `TokenExpirado` como `FirmaInvalida` o viceversa**: cada fallo tiene su excepción; mezclarlas oculta el diagnóstico.
- (transversal) Tests propios triviales (repetir un caso ya cubierto) en vez de un borde real (`exp` no numérico, header sin `alg`).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución impecable con `compare_digest` y orden perfecto, pero bitácora que no sabe explicar **por qué** ese orden o esa comparación.
- Uso de PyJWT o de patrones que el ejercicio prohíbe explícitamente (la consigna pide stdlib).
- Vocabulario de criptografía por encima del nivel sin poder defenderlo.
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué excepción lanza un token con `alg: none` y por qué se decide *antes* de mirar la firma. Si implementó de verdad, lo explica al tiro.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu verificador acepta un token que no debería. ¿En qué momento decides con qué algoritmo verificar? ¿Quién elige ese algoritmo, tú o el token?"
- **Pregunta socrática (nivel 2):** "Si un atacante intercepta un token válido y solo cambia un carácter del payload, ¿qué paso de tu verificación debería detectarlo, y por qué ese paso necesita el secreto que el atacante no tiene?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Reordena: valida la **firma** antes de mirar `exp` (no confíes en un claim de un token aún no autenticado), y compara la firma con `hmac.compare_digest`, no con `==`. Luego justifícalo en la bitácora."

## Conexión con el proyecto / capstone
- En el [capstone](/fase-3-backend/proyecto/) usarás PyJWT para validar tokens; este ejercicio es el modelo mental que te deja usarla con criterio (pasar `algorithms=["HS256"]`, no meter datos sensibles, expiración corta) en vez de copiar un snippet a ciegas.
