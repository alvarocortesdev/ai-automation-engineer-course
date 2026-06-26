# Ejercicio 3.3 — Resolver la carrera del stock: pesimista vs optimista

> **Modalidad: código (Python + SQL, sin IA).** El bug de concurrencia más clásico del backend —vender el último ticket dos veces— resuelto con las dos estrategias que todo semi-senior debe saber implementar y contrastar.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.3` PostgreSQL a fondo
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar la compra de stock bajo concurrencia con **dos** estrategias —locking **pesimista** (`SELECT ... FOR UPDATE`) y **optimista** (columna `version` + reintento)— de modo que **nunca** se venda más de lo que hay ni el stock quede negativo, aunque 100 hilos compren a la vez. Y justificar cuál conviene según la contención.

## 📋 Contexto

Todo endpoint del capstone que decremente un recurso compartido (stock, saldo, cupos) necesita ser correcto bajo carga. Estas dos estrategias son la respuesta estándar; saber implementarlas **y elegir entre ellas** es exactamente lo que se pregunta en entrevistas de backend.

## ⚙️ Requisitos

Necesitas un **Postgres corriendo** (el que instalaste en `3.1`) y las dependencias:

```bash
uv add "psycopg[binary]" psycopg-pool pytest      # o: pip install "psycopg[binary]" psycopg-pool pytest
createdb explain_lab                               # una base cualquiera para el test
export DATABASE_URL="postgresql://localhost/explain_lab"
```

Si `DATABASE_URL` no está o no hay base, el test se **salta** con un mensaje claro — pero entonces no lo terminaste de verdad: levanta un Postgres.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Razona el entrelazado en el tiempo antes de teclear.
2. Solo entonces, consulta la **documentación oficial** (psycopg 3 transactions, Explicit Locking de Postgres).
3. **Solo al final**, usa IA para *revisar* — no para generar las funciones.
4. Mañana, reescribe ambas de memoria.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa **sin cambiar las firmas**:
   - `comprar_pesimista(pool, evento_id) -> bool`
   - `comprar_optimista(pool, evento_id) -> bool`
2. `schema.sql` documenta la tabla `eventos(id, stock, version)` (el test la crea solo).
3. Corre el test:

   ```bash
   uv run pytest        # o: pytest
   ```

   Crea un evento con `stock = 50`, lanza **100 compras concurrentes** con threads, y verifica —para **ambas** estrategias— que se vendieron exactamente 50 y el stock quedó en 0.
4. Escribe `bitacora.md`: en qué escenario de contención preferirías cada estrategia y por qué.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde** para ambas estrategias (`pesimista` y `optimista`): exactamente 50 ventas, stock final 0, nunca negativo.
- [ ] La pesimista bloquea con `FOR UPDATE` y libera al confirmar; la optimista reintenta ante `rowcount == 0` con un **tope** (sin loop infinito).
- [ ] `bitacora.md` argumenta cuándo elegir cada una (baja vs alta contención).
- [ ] Puedes explicar **sin notas** por qué un `SELECT` + `UPDATE` "normales" (sin `FOR UPDATE`, sin `version`, sin aritmética atómica) fallarían este test.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

**Pesimista:** dentro de `with pool.connection() as conn:`, `SELECT stock FROM eventos WHERE id = %s FOR UPDATE`, revisa en Python si `stock > 0`, y si sí `UPDATE eventos SET stock = stock - 1 WHERE id = %s`. El lock se mantiene hasta el commit (al salir del `with`), así que el siguiente hilo espera y lee el valor ya decrementado.

**Optimista:** `SELECT stock, version ...` (sin `FOR UPDATE`); luego `UPDATE eventos SET stock = stock - 1, version = version + 1 WHERE id = %s AND version = %s` con la `version` que leíste. Si `cur.rowcount == 0`, otro confirmó entre tu lectura y tu escritura: vuelve a leer y reintenta (hasta un tope). Revisa la sección 4.7 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `solucion.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/carrera-stock-locking.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/carrera-stock-locking.md` — no la mires antes de intentarlo.
