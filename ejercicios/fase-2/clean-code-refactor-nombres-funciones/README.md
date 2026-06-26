# Ejercicio 2.2 — Refactor: nombres con intención + funciones pequeñas

> **Modalidad: código (Primero-Sin-IA).** Practicas los objetivos O1 y O2 de la sub-unidad
> [2.2 Clean code](../../../src/content/docs/fase-2-ingenieria/2-2-clean-code.mdx): **nombres
> que revelan intención** y **funciones pequeñas con una sola responsabilidad**. La función ya
> funciona y los tests ya están en verde: tu trabajo es dejarla **legible sin romper nada**.
> Sin IA hasta cerrar tu intento.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.2` Clean code
**Ruta:** crítica · **Timebox:** 30–40 min

## 🎯 Objetivo

Refactorizar `total_pedido(lineas)` para que **revele intención** (sin nombres crípticos, sin
índices mágicos, sin números mágicos) y quede **descompuesta en funciones de una sola
responsabilidad**, **sin cambiar su comportamiento ni su firma pública**.

## 📋 Contexto

Refactorizar bajo una red de tests es el músculo central del capstone de la fase
(*Refactor + suite de tests*). Aquí lo entrenas en pequeño: cambias la forma del código pero
no lo que hace, y los tests verdes te lo confirman después de **cada** paso. Si en algún paso
se ponen rojos, ese paso cambió comportamiento — deshazlo.

## 📏 Primero-Sin-IA

1. **Antes de tocar nada**, lee la función original y di en voz alta qué hace. Si te cuesta,
   ese costo de lectura es exactamente lo que vas a eliminar.
2. Refactoriza **a mano**, en pasos pequeños, corriendo los tests entre cada paso (timebox arriba).
3. Solo entonces consulta la **documentación oficial** (PEP 8, catálogo de refactorings de Fowler).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `total_pedido.py`. **No cambies** la firma pública `total_pedido(lineas)`.
2. Confirma que partes de verde:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Refactoriza en pasos pequeños (sugerencia: nombres → desempaquetar tupla → constantes →
   extraer funciones), corriendo `pytest` después de **cada** cambio. El objetivo es estar
   **siempre en verde**.
4. Añade al menos **un test borde tuyo** en `test_total_pedido.py` (¿precio 0?, ¿cantidad 0?,
   ¿una línea activa y muchas inactivas?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] No quedan nombres sin intención (`d`, `r`, `i`, `x`, `tmp`) ni índices mágicos (`linea[1]`).
- [ ] Los números mágicos (`100000`, `0.1`) están en **constantes con nombre**.
- [ ] La función está **descompuesta** en piezas con una sola responsabilidad (al menos: sumar
      líneas activas / aplicar descuento por volumen), cada una nombrada por lo que hace.
- [ ] **Todos los tests siguen en verde** y la firma pública `total_pedido(lineas)` no cambió.
- [ ] Agregaste un test borde tuyo.
- [ ] Puedes **explicar sin notas** por qué tu versión se lee mejor que la original.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Pasos pequeños, tests entre cada uno: (1) renombra `d/r/i` a nombres del dominio
(`lineas/total/linea`); (2) `producto, precio, cantidad, activo = linea` para matar los índices
mágicos y reemplaza `== True` por el booleano directo; (3) sube `100000` y `0.1` a constantes
`UMBRAL_DESCUENTO_VOLUMEN` y `TASA_DESCUENTO_VOLUMEN`; (4) extrae `subtotal_de_lineas_activas` y
`con_descuento_por_volumen`, y deja `total_pedido` orquestando ambas. Revisa las secciones 4.1–4.4
de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-2/clean-code-refactor-nombres-funciones/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-2/` — no la mires antes de intentarlo
de verdad. Recuerda: los tests garantizan que **no rompiste** nada, pero la calidad de tus
**nombres** y tu **descomposición** la juzga la rúbrica, no el color verde.
