---
ejercicio_id: fase-3/orm-vs-sql-diagnostico
fase: fase-3
sub_unidad: "3.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnostica el N+1 y decide ORM vs SQL crudo

## Parte A — `diagnostico.md`

**Conteo.** El log tiene **5 queries**: 1 `SELECT ... FROM pedidos` + 4 `SELECT ... FROM clientes WHERE id = ?` (una por cada uno de los 4 pedidos). Patrón **N+1** con **N = 4** (1 query inicial + N queries, una por resultado).

**Causa.** Al iterar los pedidos y acceder a `pedido.cliente` (relación **lazy**) dentro del bucle, cada acceso dispara su propia query. El endpoint pide los clientes "de a uno", cuando podría traerlos todos junto con los pedidos.

**El `id = 1` repetido.** El cliente `id = 1` aparece **dos veces** porque dos pedidos distintos pertenecen a él, y el **lazy loading se evalúa por cada acceso de atributo**: no hay un caché compartido que diga "ya cargué al cliente 1". Cada `pedido.cliente` es una consulta independiente. (Matiz fino que el alumno no tiene por qué saber, pero suma: dentro de **una misma** `Session`, si el objeto Cliente 1 ya estuviera en el *identity map*, una segunda carga del **mismo** atributo no re-consultaría; aquí son dos atributos `cliente` de dos pedidos distintos, ambos lazy, por eso ambos van a la base.)

**Cura.** Como `pedido.cliente` es **to-one** (cada pedido tiene **un** cliente), la cura natural es `joinedload`:

```python
select(Pedido).options(joinedload(Pedido.cliente))
```

Un `LEFT JOIN` trae el cliente en la misma query → el endpoint queda en **1 query**, sin `.unique()` (no es colección). `selectinload` también lo curaría (2 queries) pero agrega un round-trip innecesario para un to-one.

## Parte B — `decisiones.md`

| Escenario | Decisión | Justificación esperada |
|---|---|---|
| **1. CRUD de productos** | **ORM** | Operaciones simples fila a fila: el ORM elimina boilerplate, parametriza solo (seguro), y es legible. Es exactamente para lo que el ORM brilla. |
| **2. Reporte mensual con window functions** | **SQL crudo** | `GROUP BY` + agregaciones + `RANK() OVER (PARTITION BY ...)` se expresan mucho más claro y directo en SQL que peleando con la API del ORM. Va parametrizado (`text(...)` con bind params). |
| **3. Carga de 2 millones de filas** | **SQL crudo / bulk** | El ORM crea un objeto Python por fila y rastrea cada uno: lentísimo a esa escala. Un `INSERT ... SELECT`, `COPY` (Postgres) o el bulk de SQLAlchemy Core vuela. |

**Seguridad (debe aparecer al menos una vez).** El SQL crudo se escribe **parametrizado** (`text("... WHERE mes = :mes")` con `{"mes": ...}`), **nunca** concatenando strings (f-strings o `+`), porque eso abre SQL injection. El ORM ya parametriza por defecto; al bajar a SQL crudo, la responsabilidad vuelve al desarrollador.

## El recorrido de razonamiento esperado
1. Contar queries del log → reconocer 1 + N.
2. Atar las N queries al acceso lazy dentro del bucle.
3. Elegir la cura por **tipo de relación**: to-one → `joinedload`; to-many → `selectinload`.
4. Para ORM vs SQL: preguntarse "¿el ORM expresa esto con claridad y sin pelear, y a qué costo?". CRUD sí; analítica y cargas masivas, no.

## Puntos resbalosos (donde el corrector debe mirar)
1. **"Falta un índice".** Error frecuente: un índice acelera cada query pero no reduce que sean 5. La cura del N+1 es eager loading.
2. **`selectinload` para el to-one.** Funciona pero no es óptimo (2 queries vs 1). Marca que `joinedload` es lo natural aquí, y por qué.
3. **No explicar el `id = 1` repetido.** Si lo ignora, probablemente no entendió que lazy re-consulta en cada acceso.
4. **Decisiones sin defensa.** "Siempre ORM" o "siempre SQL crudo" no son aceptables; el ejercicio mide el criterio del trade-off.
5. **Olvidar la parametrización.** El requisito de seguridad es parte del DoD.

## Rango de respuestas aceptables
- Parte A: aceptar `joinedload` (óptimo) o `selectinload` (correcto, sub-óptimo) **si** justifica; exigir el conteo correcto (5 = 1+4) y el nombre del patrón.
- Parte B: el escenario 1 admite ORM; 2 y 3 admiten SQL crudo/bulk. Una defensa razonada distinta (p. ej. "uso una vista materializada para el reporte") es aceptable si el alumno la justifica con trade-offs reales.
- ❌ **No aceptable como competente:** no contar las queries, confundir el N+1 con un problema de índices, o decisiones de la Parte B sin justificación.
