# Ejercicio 0.7 — Resumen de gastos por categoría

> **Modalidad: código (Primero-Sin-IA).** Re-haces a mano las piezas de la sub-unidad
> 0.7: control de flujo, estructuras (`list`/`dict`), funciones y manejo de errores.
> Sin IA hasta cerrar tu intento.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.7` Fundamentos de programación sin IA
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Implementar `total_por_categoria(gastos)`: recorre una lista de gastos, **agrupa y suma**
los montos por categoría en un `dict`, **valida** la entrada y maneja la lista vacía.

## 📋 Contexto

Es exactamente el tipo de función que vivirá dentro de tu **Capstone F0 — CLI sin IA**:
recibir datos, recorrerlos, agruparlos y rechazar lo inválido. Si la puedes escribir a
mano, tienes los cuatro ladrillos centrales de la fase firmes.

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el **contrato** en 3 líneas (esto es spec-first, ver `0.8`):
   ¿qué entra?, ¿qué sale?, ¿qué casos borde hay?
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
3. Solo entonces consulta la **documentación oficial** de Python (estructuras de datos, errores).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `gastos.py` y completa `total_por_categoria` (no cambies su firma).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **los 6 tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_gastos.py` (¿qué pasa con una categoría
   con tilde?, ¿con un `0` de monto?, ¿con muchas categorías?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Agrupa y suma correctamente (los 6 tests pasan).
- [ ] La **lista vacía** devuelve `{}` sin reventar.
- [ ] Un **monto negativo** o una **categoría vacía/ausente** lanzan `ValueError` con mensaje claro.
- [ ] Agregaste al menos **un test propio**.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Necesitas un `dict` acumulador **inicializado antes** del bucle. Para sumar "creando la
clave si aún no existe", `dict.get(clave, 0)` devuelve `0` cuando la categoría es nueva,
así evitas un `if` extra para el primer gasto de cada categoría. **Valida antes de
acumular**, no después: si un gasto es inválido, lánzalo apenas lo detectes. Revisa la
sección 4.5 y 4.7 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/fundamentos-programacion-inventario/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-0/` — no la mires antes de
intentarlo de verdad.
