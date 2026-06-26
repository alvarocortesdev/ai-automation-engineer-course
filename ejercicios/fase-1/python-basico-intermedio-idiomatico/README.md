# Ejercicio 1.1 — Inventario idiomático, empaquetado

> **Modalidad: código (Primero-Sin-IA).** No es solo "hacer que pase": el objetivo es que pase
> con código **idiomático** (la forma Pythonic) y sin romper la estructura de **paquete**. Un
> revisor lee ese estilo en segundos.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.1` Python de básico a intermedio
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Implementar dos funciones idiomáticas dentro de un paquete Python (`despensa/`) y dejar la suite de
tests en verde, **incluida la prueba que importa desde el nivel del paquete** (`from despensa import
...`), que te obliga a tocar `__init__.py`.

## 📋 Contexto

Este `despensa/` es el esqueleto del lado Python del **Capstone F1 — La misma app, dos lenguajes**.
La lógica de inventario que escribes aquí la cubrirás con más tests en `1.6` y la tiparás con
pydantic en `1.4`. No es práctica desechable.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, sin IA (timebox arriba). Piensa el **contrato** antes de codear: qué entra,
   qué sale, qué casos borde (esto es spec-first).
2. Solo entonces, consulta **documentación oficial** (Python tutorial: comprehensions, módulos).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria** en un paquete nuevo. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Implementa `resumen_inventario` y `formatear_lineas` en `despensa/inventario.py` (no cambies sus
   firmas).
2. Edita `despensa/__init__.py` para **re-exportar** ambas funciones, de modo que
   `from despensa import resumen_inventario` funcione.
3. Corre los tests desde esta carpeta:

   ```bash
   uv run pytest        # recomendado
   pytest               # si ya tienes pytest en el entorno
   ```

4. Itera hasta que **todos los tests pasen en verde**.
5. Añade al menos **un caso de prueba tuyo** en `test_inventario.py` (un caso borde que se te ocurra).

### Contrato de las funciones

- `resumen_inventario(productos)` — `productos` es una lista de `dict` con `"nombre"` (str no vacío),
  `"precio"` (número ≥ 0) y `"stock"` (entero ≥ 0). Devuelve un `dict`:
  - `"unidades"`: suma de los `stock`.
  - `"valor"`: suma de `precio * stock` de cada producto.
  - `"agotados"`: lista de los `nombre` cuyo `stock` es 0.
  - Lista vacía → `{"unidades": 0, "valor": 0, "agotados": []}`.
  - `precio` o `stock` negativos → `ValueError`.
- `formatear_lineas(productos)` — devuelve una lista de strings numerada desde 1, formato exacto
  `"1. café — $2500 (x3)"` (usa f-string y `enumerate`). Lista vacía → `[]`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan, incluido `test_import_desde_paquete`.
- [ ] El código es **idiomático**: sin `range(len(...))`, con f-strings, comprehensions y truthiness.
- [ ] Lista vacía no revienta; entradas inválidas lanzan `ValueError`.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué tocaste `__init__.py`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `resumen_inventario`, valida en un solo recorrido **antes** de acumular; `sum(p["stock"] for p
in productos)` con un generator evita listas intermedias, y `[p["nombre"] for p in productos if
p["stock"] == 0]` te da los agotados. Para `formatear_lineas`, `enumerate(productos, start=1)` da el
número y el producto a la vez. Si `from despensa import resumen_inventario` falla con `ImportError`,
es porque `__init__.py` no re-exporta ese nombre: añade ahí `from despensa.inventario import ...`.
Revisa la sección 4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/python-basico-intermedio-idiomatico.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/python-basico-intermedio-idiomatico.md`
— no la mires antes de intentarlo de verdad.
