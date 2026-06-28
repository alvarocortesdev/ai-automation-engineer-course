---
ejercicio_id: fase-8/cache-semantico-router-fallback
fase: fase-8
sub_unidad: "8.5"
version: 1
---

# Rúbrica — Caché semántico + router con fallback

> Rúbrica **analítica** para un ejercicio de **código**. Hay tests, pero pasar los tests no es todo: se
> evalúa que el aislamiento por tenant sea una barrera **fail-closed** (seguridad), que el fallback
> distinga reintentable de no-reintentable, y que el alumno pueda **defender** por qué cada decisión es
> así. Un alumno puede hacer pasar los tests con un caché que filtra mal el tenant si los tests no lo
> cubren —por eso el corrector revisa el código, no solo el verde.

## Objetivos evaluados
- **O1** — Caché semántico con hit por similitud ≥ umbral y **aislamiento por tenant**.
- **O2** — Router multi-modelo (fácil → barato, difícil → caro).
- **O3** — Fallback que degrada solo ante 429/5xx y propaga el 400.

## Criterios y niveles

### C1 — Corrección (¿pasan los tests y hacen lo pedido?) · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; `get` compara por igualdad exacta en vez de similitud, o el router/fallback no implementados. |
| **en-progreso** | Algunos tests pasan; p. ej. el caché hace hit por similitud pero **no aísla por tenant**, o el fallback captura también el RequestInvalido. |
| **competente** | Todos los tests en verde: hit por similitud, miss bajo umbral, aislamiento por tenant, ruteo correcto, fallback que degrada en 429/5xx y propaga el 400. |
| **excelente** | Además, código limpio (filtra por tenant **antes** de buscar el vecino; usa `coseno` y el umbral inyectado; dedup de la cadena) y un test propio que cubre un borde real (tenants distintos no comparten, umbral más alto, dedup). |

### C2 — Seguridad: aislamiento por tenant fail-closed · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El `get` no filtra por tenant; un tenant puede recibir el hit de otro. |
| **en-progreso** | Filtra por tenant, pero el filtro es frágil (p. ej. compara similitud sobre todas las entradas y luego "espera" que el tenant coincida). |
| **competente** | El filtro por tenant ocurre **antes** de cualquier match; sin entradas del tenant → miss limpio. |
| **excelente** | Reconoce (en comentario o write-up) que esto es seguridad/OWASP LLM, no relevancia, y que un hit cruzado sería una fuga de datos entre clientes. |

### C3 — Manejo de errores: reintentable vs no-reintentable · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `except Exception` genérico que se traga el RequestInvalido (enmascara el bug del request). |
| **en-progreso** | Distingue los dos, pero con lógica enredada (p. ej. re-lanza el 400 manualmente tras capturarlo). |
| **competente** | Captura **solo** `ModeloSaturado` para degradar; `RequestInvalido` se propaga naturalmente; agota la cadena → `RuntimeError`. |
| **excelente** | Comenta por qué no se reintenta un 400 (es un bug del request, reintentar en otro modelo lo esconde) y por qué la cadena degrada hacia abajo en costo. |

## Errores típicos a marcar
- **Igualdad exacta en vez de similitud:** el caché solo acierta si la pregunta es idéntica → no es
  semántico. Debe usar `coseno` contra el umbral.
- **No filtrar por tenant (o filtrar después):** fuga cruzada. La barrera de tenant va **antes** del match.
- **`except Exception` que traga el 400:** enmascara un bug del request; el RequestInvalido debe propagar.
- **Fallback que degrada hacia arriba** (de Haiku a Opus) o que reintenta el mismo modelo en bucle.
- **Umbral hardcodeado** ignorando `self.umbral` inyectado (rompe el test del umbral estricto).
- **Llamar a un LLM/red de verdad** o usar `time.sleep` → tests no deterministas.
- (transversal) **Perseguir el verde sin aserciones propias** que cubran el aislamiento de tenant.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código que pasa los tests pero usa construcciones que el alumno no puede explicar (p. ej. una
  comprehension densa para el vecino más cercano) cuando se le pide razonarla.
- Comentarios sofisticados sobre OWASP/embedding weaknesses que no calzan con un `get` que en realidad
  no filtra por tenant correctamente.
- **Verificación sugerida:** pídele que explique, sin ejecutar, qué devuelve `get` si el tenant no tiene
  ninguna entrada, y por qué el filtro de tenant va antes del cálculo de similitud. Si razonó, lo
  explica; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu `get`, ¿compara la pregunta nueva con TODAS las entradas o solo con las del
  mismo tenant? Ese filtro no es un detalle de relevancia: es la barrera que impide que un cliente vea
  los datos de otro."
- **Pregunta socrática (nivel 2):** "Si el proveedor te devuelve un 400 (request mal armado),
  ¿reintentar en otro modelo lo arregla? ¿O solo esconde el bug? ¿Qué error deberías dejar propagar y
  cuál degradar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Filtra primero por `tenant_id`, luego
  busca el de mayor `coseno` entre esas entradas y compáralo con `self.umbral`. Y en el fallback,
  captura **solo** `ModeloSaturado`; deja que `RequestInvalido` salga solo."

## Conexión con el proyecto / capstone
- Estas dos piezas son cajas concretas del diagrama del [capstone F8](/fase-8-system-design/proyecto/):
  el caché semántico y el router multi-modelo aparecen en el RAG multi-tenant y en el sistema de
  tickets. Aquí las implementas a escala de juguete para entender qué van a hacer en el diseño en papel.
