# 2.3 — Refactoriza una función con smells (red ya puesta)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.3` Code smells y refactoring
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Tomar una función que **funciona pero huele mal** y dejarla limpia aplicando
refactorings **con nombre del catálogo de Fowler**, en pasos pequeños, **sin que
ningún test se ponga rojo**. El entregable no es solo el código limpio: es la
evidencia de que sabes nombrar el smell y el refactoring que lo cura.

## 📋 Contexto

`calc(items, c, p)` calcula el total de una orden (subtotal + descuento por tipo
de cliente − envío + IVA). Está bien calculada y trae una suite en **verde** que
pinta su comportamiento. Es el caso ideal del refactoring: la red ya existe, así
que puedes mover código con confianza. Esto es exactamente lo que harás en el
**Capstone F2** sobre tu propia API, a mayor escala.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Refactoriza un paso a la vez.
2. Solo entonces, consulta el [catálogo oficial de Fowler](https://refactoring.com/catalog/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Corre la suite y confirma el **VERDE de partida**. Si no está verde, no refactorices:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

2. Aplica refactorings **con nombre**, **uno a la vez**. Después de **cada** paso,
   corre `pytest`. Si se pone rojo, **revierte ese paso** (no acumules cambios).
3. Caza, como mínimo, estos smells y aplica su refactoring:

   | Smell | Refactoring de Fowler |
   |---|---|
   | Mysterious Name (`calc`, `c`, `p`, `t`) | Rename Variable / Rename Function |
   | Magic Numbers (`0.20`, `50000`, `0.19`…) | Replace Magic Literal with Symbolic Constant |
   | Duplicated Code (descuento vip ≈ frecuente) | Extract Function |
   | Long Function (hace 4 cosas) | Extract Function (subtotal, descuento, envío, IVA) |
   | Nested Conditional | Decompose Conditional / guardas con `return` |
   | Comments (desodorante) | bórralos: el código se explica solo |

4. Documenta tu trabajo en `smells.md` (ver entregable).

> ⚠️ **No cambies el comportamiento.** Mismas entradas → mismos números. No
> modifiques las **aserciones** de los tests. Si renombras `calc`, ajusta SOLO la
> línea `from solucion import calc` del test (eso es parte del Rename).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` sigue **verde** sobre la suite provista (no la modificaste para que pase).
- [ ] Cada refactoring aplicado tiene un **nombre del catálogo** en `smells.md`.
- [ ] Eliminaste la **duplicación** del descuento (vip/frecuente) sin cambiar los montos.
- [ ] No quedan **números mágicos** ni **comentarios-desodorante**.
- [ ] Los condicionales anidados quedaron **aplanados** (guardas / `if/elif`).
- [ ] Puedes explicar **sin notas** por qué corres los tests después de *cada* paso.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.py` — tu versión refactorizada, con la suite en verde.
- `smells.md` — tabla con **smell → refactoring de Fowler aplicado → por qué**
  (mínimo **seis** filas).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza barato y reversible: **Rename** primero (`calc`→`total_orden`, `c`→
`tipo_cliente`, `p`→`codigo_cupon`, `t`→`subtotal`). Luego saca los números a
constantes (`DESCUENTO_VIP_ALTO = 0.20`, `UMBRAL_ENVIO_GRATIS = 50000`,
`TASA_IVA = 0.19`…). El corazón es la **duplicación**: el bloque vip y el frecuente
comparten la forma "si supera el umbral, descuento alto; si no, bajo" — extráela a
`descuento_por_cliente(tipo, subtotal)`. Extrae también `subtotal(items)`,
`costo_envio(...)` e `iva(...)` con **Extract Function** y compón el total al final.
Aplana cada condicional a guardas. Corre `pytest` entre cada paso. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `smells.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/refactor-precio-con-smells.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/refactor-precio-con-smells.md`
— no la mires antes de intentarlo de verdad.
