# Ejercicio 7.5a — Construir la capa gold sin doble conteo

> **Modalidad: código (Python puro, sin pandas, sin IA).** Este ejercicio te hace tropezar a propósito
> con el bug #1 del modelado analítico: el **fan-out / doble conteo** que aparece cuando combinas datos
> a distintos *grains*. Lo entiendes de verdad cuando un test te lo caza.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.5a` ELT moderno + modelado analítico
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Implementar dos transformaciones de la **capa gold** sobre un star schema en silver, y construir el
`valor_total_por_cliente` **sin inflar el costo de envío** —que vive a grain de orden, no de línea.

## 📋 Contexto

En la lección modelaste un star schema. Aquí lo "materializas" en miniatura, en Python, para sentir en
los dedos por qué declarar el **grain** importa: una agregación a grain de línea (`ingresos_por_categoria`)
es trivial; combinar dos grains (`valor_total_por_cliente`: líneas + envío de orden) es donde casi todo
el mundo se equivoca. Es exactamente la lógica que tu capstone necesita para darle al agente cifras
correctas.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces consulta **documentación oficial** si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar*.
4. Mañana, **reescribe `valor_total_por_cliente` de memoria**. Si no puedes explicar por qué el envío
   se cuenta una vez por orden, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `transformaciones.py` y lee el contrato completo en el docstring (los shapes de `lineas`,
   `productos`, `ordenes`).
2. Implementa `ingresos_por_categoria` y `valor_total_por_cliente` (no cambies las firmas).
3. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. Itera hasta que **todos pasen en verde**, incluido `test_envio_no_se_duplica_con_varias_lineas`.
5. Añade al menos **un test propio** en `test_transformaciones.py` (ve el `TODO` al final).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan en verde.
- [ ] `valor_total_por_cliente` cuenta el envío **una vez por orden** (no por línea): el test del
      fan-out pasa.
- [ ] Una categoría que está en la dimensión pero sin ventas **no aparece** en el resultado.
- [ ] Las listas vacías devuelven `{}`.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar, sin notas, por qué aplanar líneas con órdenes infla el envío** (check de
      dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`ingresos_por_categoria`: construye primero un mapa `producto_id -> categoria` desde `productos`, luego
recorre `lineas` sumando `monto` en un dict por categoría. Una sola pasada.

`valor_total_por_cliente`: **no juntes todo en una sola tabla**. Calcula dos agregaciones separadas y
súmalas al final:
1. `monto` por cliente — recorre `lineas`, pero necesitas el `cliente_id`, que está en `ordenes`: arma
   un mapa `orden_id -> cliente_id` primero.
2. `envio` por cliente — recorre `ordenes` (¡cada orden aparece una sola vez ahí!), suma `envio`.

Si te ves multiplicando el envío por el número de líneas, ese es justo el bug que el ejercicio quiere
que sientas. Revisa la sección de doble conteo de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-7/capa-gold-sin-doble-conteo.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/` — no la mires antes de intentarlo de
verdad.
