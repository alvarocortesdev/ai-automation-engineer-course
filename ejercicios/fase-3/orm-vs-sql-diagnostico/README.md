# Ejercicio 3.5 — Diagnostica el N+1 y decide ORM vs SQL crudo

> **Modalidad: a mano (razonamiento, sin IA, sin código que correr).** Entrena las dos decisiones de criterio que separan a un semi-senior: leer un log de SQL y cazar el N+1, y saber cuándo el ORM estorba y debes bajar a SQL crudo.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.5` ORMs y el problema N+1
**Ruta:** crítica · **Timebox:** 30 min

## 🎯 Objetivo

Demostrar, por escrito, que sabes (1) diagnosticar un N+1 leyendo queries reales y proponer la cura correcta, y (2) decidir entre ORM y SQL crudo con un trade-off defendible. Sin esto, "sé usar un ORM" es una ilusión: el N+1 te pillará en producción y pelearás con el ORM donde SQL sería más claro.

## 📋 Contexto

En el capstone tendrás endpoints lentos. La herramienta de diagnóstico no es el cronómetro (engaña con datos de prueba), es **contar las queries**. Y no toda query merece ir por el ORM: este ejercicio te obliga a defender cada decisión.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Razona antes de escribir.
2. Solo entonces, consulta la **documentación oficial** (SQLAlchemy 2.0 — Relationship Loading Techniques) para validar tu cura.
3. **Solo al final**, usa IA para *revisar* tu razonamiento — no para generarlo.
4. Mañana, explica el diagnóstico de memoria a otra persona (o en voz alta).

## El material a analizar

### Parte A — Un log de SQL de un endpoint lento

Este es el log (`echo=True`) de un endpoint `GET /pedidos` que lista pedidos y, por cada uno, muestra el nombre de su cliente. Hay **4 pedidos** en la base de prueba. Relaciones: `pedido.cliente` es **to-one** (cada pedido tiene un cliente); un `Cliente` tiene muchos `Pedido`.

```text
SELECT pedidos.id, pedidos.total, pedidos.cliente_id FROM pedidos
SELECT clientes.id, clientes.nombre FROM clientes WHERE clientes.id = 1
SELECT clientes.id, clientes.nombre FROM clientes WHERE clientes.id = 2
SELECT clientes.id, clientes.nombre FROM clientes WHERE clientes.id = 1
SELECT clientes.id, clientes.nombre FROM clientes WHERE clientes.id = 3
```

### Parte B — Tres escenarios de diseño

1. **CRUD de productos**: crear, leer, actualizar y borrar productos de un catálogo. Operaciones simples sobre una tabla, una fila a la vez.
2. **Reporte mensual de ventas**: total facturado por mes y por categoría, con el ranking de los 3 mejores productos de cada categoría (necesita `GROUP BY`, agregaciones y una window function tipo `RANK() OVER (PARTITION BY ...)`).
3. **Carga inicial de catálogo**: importar **2 millones** de productos desde un archivo a la base, una sola vez, lo más rápido posible.

## 🛠️ Qué entregar (deja estos archivos en esta carpeta)

### `diagnostico.md` (Parte A)

- ¿Cuántas queries ejecuta el endpoint? ¿Sigue el patrón N+1? Nómbralo y di cuánto vale N aquí.
- ¿Qué acceso a relación, dentro de qué bucle, dispara las queries extra?
- Un detalle fino: el cliente `id = 1` aparece **dos veces** en el log. ¿Por qué el ORM no reusó la primera carga? (pista: piensa en qué hace lazy loading en cada acceso).
- ¿Cuál es la cura: `joinedload` o `selectinload`? Justifica con el **tipo de relación** (`pedido.cliente` es to-one). ¿Cuántas queries quedarían tras la cura?

### `decisiones.md` (Parte B)

Para **cada** escenario, una línea con tu decisión (**ORM** o **SQL crudo**) y 2–3 líneas de justificación. Al menos una vez, menciona que el SQL crudo debe ir **parametrizado** (nunca concatenar strings) y por qué (seguridad / SQL injection).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Cuentas correctamente las queries del log (son 5 = 1 + 4) y nombras el N+1 (N = 4).
- [ ] Explicas que el lazy loading recarga en **cada** acceso (por eso el `id = 1` aparece dos veces) y propones la cura coherente con to-one (`joinedload`), dejando el endpoint en 1 query.
- [ ] Cada uno de los 3 escenarios tiene una decisión con justificación defendible (CRUD → ORM; reporte con window functions → SQL crudo; carga masiva → SQL/bulk, no ORM objeto por objeto).
- [ ] Mencionas el SQL parametrizado como requisito de seguridad.
- [ ] Puedes defender **sin notas** por qué contar queries es mejor diagnóstico que el cronómetro.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Parte A: cuenta líneas `SELECT`. La primera trae todos los pedidos; las siguientes traen un cliente cada una → patrón "1 + N". El `id = 1` repetido revela que el lazy loading no cachea entre objetos distintos: cada `pedido.cliente` se evalúa por separado. Como `cliente` es **un** objeto por pedido (to-one), `joinedload` lo trae en el mismo `SELECT` con un `JOIN`, sin `.unique()`.

Parte B: pregúntate por cada caso "¿el ORM expresa esto con claridad y sin pelear?". CRUD simple: sí. Window functions y rankings: el SQL es más directo y legible. Insertar millones de filas: el ORM crea un objeto por fila (lento); un bulk/`COPY`/`INSERT ... SELECT` vuela. Revisa la sección 4.9 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `diagnostico.md` + `decisiones.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/orm-vs-sql-diagnostico.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/orm-vs-sql-diagnostico.md` — no la mires antes de intentarlo.
