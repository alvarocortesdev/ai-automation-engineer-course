---
ejercicio_id: fase-8/modelar-aggregate-y-value-object
fase: fase-8
sub_unidad: "8.2"
version: 1
---

# Rúbrica — Refactor de modelo anémico a aggregate + value object

> Rúbrica **analítica** atada a los `objetivos`. Lo que se evalúa no es "que pase tests" (el
> anémico ya pasaba el caso feliz), sino si el alumno **volvió imposible el estado inválido**:
> dinero negativo, saldo negativo, saldo desincronizado. Un modelo que pasa `acceptance_test.py`
> pero deja una fuga (p. ej. expone la lista interna) **no** es `competente` en C1.

## Objetivos evaluados
- **O1** — Value object `Dinero` que carga su invariante: inmutable, igualdad por valor, no negativo, no opera entre monedas distintas.
- **O2** — Aggregate root `Billetera` que protege invariantes desde afuera: saldo nunca negativo y saldo **calculado** de los movimientos (no un campo).
- **O3** — Domain event `PagoRealizado` emitido **solo** cuando la operación ocurre con éxito; orden validar → mutar → emitir.

## Criterios y niveles

### C1 — Corrección: las invariantes son imposibles de violar · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sigue siendo anémico: `saldo` es un campo mutable, o se puede dejar negativo, o `Dinero` admite negativos. No pasa `acceptance_test.py`. |
| **en-progreso** | Pasa algunos casos pero queda una fuga: expone la lista interna por referencia (se salta el límite), o `saldo` es campo que "se actualiza" en vez de calcularse, o valida con `assert` (se va con `-O`). |
| **competente** | `Dinero` inmutable/no-negativo/no-cross-currency; `Billetera` rechaza pagar de más sin dejar saldo negativo; `saldo()` es función de los movimientos; no se filtra lo interno. Pasa `acceptance_test.py`. |
| **excelente** | Además: excepciones de dominio con nombre (`SaldoInsuficiente`), `Dinero` cubre un caso extra pensado (p. ej. `__eq__` correcto entre monedas), y el alumno nombra **qué clase de bug eliminó por construcción** (no por test). |

### C2 — Calidad de ingeniería: TDD real, value object idiomático · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `bitacora.md`, o tests escritos después "para que pase"; o un solo test del caso feliz. |
| **en-progreso** | Hay tests pero no prueban las invariantes con `pytest.raises` (no testea que `Dinero(-1)` o pagar de más fallen); `bitacora` sin el 🔴 antes del 🟢. |
| **competente** | Un test por invariante, incluidos los caminos de error con `pytest.raises`; `bitacora.md` muestra red→green→refactor; usa `@dataclass(frozen=True)` (no `__setattr__` manual). |
| **excelente** | Hay un test de **propiedad/invariante** (p. ej. tras cualquier secuencia de cargas/pagos válidos, `saldo() == suma(cargas) - suma(pagos)` y nunca negativo), no solo casos puntuales. |

### C3 — Comprensión demostrada · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue value object de entity ni explica por qué calcular el saldo importa. |
| **en-progreso** | Explica el qué pero no el porqué ("uso frozen porque sí"). |
| **competente** | Articula que **calcular** el saldo elimina el bug de desincronización *por construcción*, y por qué la encapsulación (atributos privados) es lo que protege la invariante. |
| **excelente** | Conecta con el dominio real (Copec Pay/pagos): por qué el dinero va en centavos enteros y no `float`, y por qué el domain event desacopla efectos secundarios (email/observabilidad). |

## Errores típicos a marcar
- **Saldo como campo que se "mantiene"** (`self._saldo += ...`) en vez de calcularse: vuelve a meter el bug de desincronización que el ejercicio pedía eliminar.
- **Exponer la colección interna por referencia** (`return self._movimientos`): permite saltarse las reglas mutándola desde fuera (el "spot the leak" de 6.2).
- **Validar con `assert`** en vez de `raise ValueError`/excepción de dominio: los `assert` se eliminan con `python -O`.
- **Emitir el evento antes de validar**: registrar `PagoRealizado` y *después* chequear saldo → anuncia un hecho que puede no ocurrir.
- **`Dinero` como `float` o sin `frozen`**: bugs de redondeo y/o objeto mutable que deja de ser value object.
- **No proteger cross-currency**: `Dinero(1000,"CLP") + Dinero(1000,"USD")` debe fallar, no sumar 2000.
- (transversal testing) tests solo del caso feliz, sin `pytest.raises` para los caminos de error.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Modelo impecable pero `bitacora.md` ausente o con todos los 🟢 sin 🔴 previo: el TDD no ocurrió, el código llegó entero (pídele que explique qué test forzó la excepción de dominio).
- Usa patrones sofisticados (event sourcing completo, `__slots__`, metaclasses) impropios del alcance, sin poder justificar por qué aquí: probable copy-paste.
- Explica `frozen`/value object con la definición de libro pero no puede señalar en *su* `Billetera` dónde está protegida la invariante "no negativo".

## Feedback sugerido (graduado)
- **Pista (nivel 1):** "¿Existe algún camino —aunque sea raro— para dejar tu `Billetera` con saldo negativo o desincronizado? Recórrela como si quisieras romperla."
- **Pregunta socrática (nivel 2):** "Si `saldo` fuera una función de los movimientos en vez de un campo, ¿qué bug se vuelve imposible de escribir? ¿Por qué?"
- **Dirección concreta (nivel 3, sólo tras intento real):** apunta a la fuga concreta (campo mutable / colección expuesta / orden emit-antes-de-validar) y nombra la invariante desprotegida, sin escribir el código corregido.

## Conexión con el proyecto / capstone
- Es el músculo de modelado que el capstone F8 (diseña 3 sistemas) y cualquier sistema de pagos/pedidos exigen: objetos que protegen sus invariantes en vez de validaciones dispersas.
