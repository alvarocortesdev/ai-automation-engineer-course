---
ejercicio_id: fase-3/carrera-stock-locking
fase: fase-3
sub_unidad: "3.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Resolver la carrera del stock: pesimista vs optimista

## Implementación canónica (`solucion.py`)

```python
from psycopg_pool import ConnectionPool


def comprar_pesimista(pool: ConnectionPool, evento_id: int) -> bool:
    with pool.connection() as conn:                      # tx; commit al salir del with
        cur = conn.execute(
            "SELECT stock FROM eventos WHERE id = %s FOR UPDATE",  # bloquea la fila
            (evento_id,),
        )
        (stock,) = cur.fetchone()
        if stock <= 0:
            return False
        conn.execute(
            "UPDATE eventos SET stock = stock - 1 WHERE id = %s",
            (evento_id,),
        )
        return True
    # al salir del with: COMMIT -> se libera el lock de fila


def comprar_optimista(
    pool: ConnectionPool, evento_id: int, max_intentos: int = 1000
) -> bool:
    for _ in range(max_intentos):
        with pool.connection() as conn:
            cur = conn.execute(
                "SELECT stock, version FROM eventos WHERE id = %s",  # sin FOR UPDATE
                (evento_id,),
            )
            stock, version = cur.fetchone()
            if stock <= 0:
                return False
            cur = conn.execute(
                "UPDATE eventos SET stock = stock - 1, version = version + 1 "
                "WHERE id = %s AND version = %s",
                (evento_id, version),
            )
            if cur.rowcount == 1:
                return True
            # rowcount == 0: otro confirmó entre nuestra lectura y escritura -> reintentar
    raise RuntimeError("se agotaron los reintentos optimistas")
```

Verificado contra `test_acceptance.py` (Postgres local): ambas estrategias venden exactamente 50 con `stock` inicial 50 y 100 hilos; stock final 0; nunca negativo.

## Por qué cada una funciona

- **Pesimista:** `FOR UPDATE` toma un lock de fila al leer. El segundo hilo que llega se **bloquea** en su `SELECT ... FOR UPDATE` hasta que el primero haga `COMMIT` (al salir del `with pool.connection()`); recién entonces lee el `stock` ya decrementado. Cero ventana para el lost update: el acceso a la fila queda **serializado**.
- **Optimista:** no toma locks. La guarda `WHERE version = %s` hace que el `UPDATE` afecte 0 filas si alguien cambió la fila (subió `version`) entre la lectura y la escritura. Detectamos `rowcount == 0` y reintentamos con una **lectura fresca**. Detalle fino de Postgres: bajo `READ COMMITTED`, si dos `UPDATE` apuntan a la misma fila, el segundo espera a que el primero confirme y luego **re-evalúa** su `WHERE` contra la fila actualizada; como `version` ya subió, no calza y `rowcount` queda en 0. Por eso converge sin perder ventas.

## Por qué la versión "ingenua" falla
Un `SELECT stock` + (cálculo en Python) + `UPDATE SET stock = <valor calculado>` sin `FOR UPDATE`, sin `version` y sin aritmética en SQL: dos hilos leen `stock = 50`, ambos calculan `49`, ambos escriben `49`. Se "vendieron" 2 pero el stock bajó 1. Repetido bajo 100 hilos, se venden muchas más de 50 unidades. Ese es el lost update que el test caza.

## El recorrido de razonamiento esperado (bitácora)
1. Reconocer que el riesgo está en la **ventana** entre leer y escribir.
2. Pesimista cierra la ventana con un lock; optimista la tolera y detecta el choque al escribir.
3. Elección por contención: **baja** → optimista (sin locks, mejor throughput, reintentos raros); **alta** → pesimista (serializa, predecible, evita la tormenta de reintentos). En este test, con 100 hilos sobre 1 fila, la contención es **alta**: el pesimista es más eficiente; el optimista funciona pero hace muchos reintentos.

## Puntos resbalosos (donde el corrector debe mirar)
1. **El lock se libera en el commit, no antes.** Si el alumno hace `conn.commit()` o sale del `with` antes del `UPDATE`, pierde la exclusión. Con `pool.connection()`, el commit ocurre al salir del bloque; el `return True` dentro del `with` está bien (el `__exit__` confirma después de evaluar el return).
2. **Re-leer dentro del loop optimista.** La lectura de `(stock, version)` debe estar **dentro** del `for`. Si está fuera, reintenta siempre con la `version` vieja → loop hasta agotar el tope.
3. **Tope de reintentos.** Sin tope (`while True`) puede colgar el test bajo alta contención. Con tope razonable (cientos) y `stock = 50`, siempre termina: un hilo pierde a lo sumo ~50 veces (los 50 commits exitosos) antes de ver `stock = 0` y devolver `False`.
4. **`stock <= 0` antes de escribir.** Debe devolver `False`, no decrementar bajo cero ni lanzar.
5. **Cálculo en SQL vs Python.** `SET stock = stock - 1` es lo idiomático. Dentro del `FOR UPDATE`, calcular en Python también es seguro (la fila está bloqueada); en la optimista, el decremento debe ir en el `UPDATE` (la guarda `version` protege).

## Rango de soluciones aceptables
- **Pesimista con aritmética atómica + guarda:** `UPDATE eventos SET stock = stock - 1 WHERE id = %s AND stock > 0` tras el `FOR UPDATE`, usando `rowcount` para el retorno — válido y robusto.
- **Pesimista usando `conn.transaction()` explícito** en vez de confiar en el commit del pool — equivalente.
- **Optimista con backoff** entre reintentos — aceptable, no exigido.
- **Optimista que usa `REPEATABLE READ` + captura de `SerializationFailure`** en vez de la columna `version` — es una variante legítima del "optimismo gestionado por el motor"; aceptable si pasa el test, aunque el enunciado pedía la columna `version` explícita (márcalo como cumplido si demuestra el concepto).
- ❌ **No aceptable como competente:** "pesimista" sin `FOR UPDATE`; optimista sin la guarda `WHERE version`; recalcular stock en Python y escribir el valor absoluto sin protección; `while True` sin tope.
