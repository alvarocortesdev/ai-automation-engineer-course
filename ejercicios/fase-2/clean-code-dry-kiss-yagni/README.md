# Ejercicio 2.2 — DRY/KISS/YAGNI con criterio

> **Modalidad: mixto (código + write-up), Primero-Sin-IA.** Practicas el objetivo O3 de la
> sub-unidad [2.2 Clean code](../../../src/content/docs/fase-2-ingenieria/2-2-clean-code.mdx):
> aplicar **DRY/KISS/YAGNI con criterio**, distinguiendo duplicación real de incidental. El
> código ya funciona y los tests ya están en verde; tu trabajo es decidir **qué tocar y qué
> no**, y **justificarlo**. Sin IA hasta cerrar tu intento.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.2` Clean code
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Refactorizar `facturacion.py` aplicando **el principio correcto a cada uno de tres casos** —y
**resistiendo** aplicarlo donde no corresponde— sin cambiar el comportamiento, y **justificar
las tres decisiones** (incluida la de NO unir dos funciones parecidas) en `decisiones.md`.

## 📋 Contexto

El error más caro de clean code no es repetir código: es **abstraer lo que no debía**.
Unir dos trozos que solo se parecen los acopla y, cuando uno cambia, el otro se rompe en
silencio. Este ejercicio entrena el juicio que separa al que aplica reglas del que aplica
criterio — exactamente el razonamiento que irá en los ADRs del capstone de la fase.

## 📏 Primero-Sin-IA

1. **Antes de tocar nada**, por cada par de trozos parecidos pregúntate: *"si esta regla
   cambiara mañana, ¿la otra debería cambiar con ella?"*. Esa pregunta decide DRY vs. dejar.
2. Refactoriza **a mano**, corriendo los tests entre cambios (timebox arriba).
3. Solo entonces consulta la **documentación oficial** (PEP 20, *The Wrong Abstraction*).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar* ni para decidir
   por ti.
5. Mañana, **reescribe de memoria** tu `decisiones.md`. Si no puedes defender las tres, no
   internalizaste el criterio.

## 🛠️ Instrucciones

1. Confirma que partes de verde:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

2. En `facturacion.py`:
   - **(a)** Extrae la fórmula del IVA a un solo lugar (DRY) y haz que ambas funciones la reusen.
   - **(b)** **Deja separados** `es_rut_valido` y `es_sku_valido` (resiste la falsa DRY).
   - **(c)** Simplifica `formatear_precio` a lo que de verdad se usa (KISS/YAGNI).
3. Corre `pytest` después de cada cambio: deben quedar **todos en verde**.
4. Completa `decisiones.md` con las **tres decisiones**, cada una con su porqué.
5. Añade al menos **un test borde tuyo** en `test_facturacion.py`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La fórmula del IVA vive en **un** solo lugar (la constante `IVA` ya no está sin usar) y
      `precio_con_iva` / `precio_con_iva_descuento` la reusan.
- [ ] Los dos validadores **siguen separados**, y `decisiones.md` explica por qué unirlos sería
      un error.
- [ ] `formatear_precio` quedó **simplificada** a su uso real, sin perder comportamiento.
- [ ] **Todos los tests siguen en verde** y agregaste un test propio.
- [ ] `decisiones.md` tiene las tres decisiones, cada una con su porqué en lenguaje claro.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

DRY real: la fórmula `x + int(x * 0.19)` representa **el mismo conocimiento** (la tasa de IVA);
si el IVA sube, ambas funciones cambian por la misma razón → extrae `con_iva(neto)` que use la
constante `IVA`. Falsa DRY: el RUT y el SKU validan largo por razones **sin relación**; un
genérico `es_texto_valido` los acoplaría → déjalos separados aunque se vean idénticos hoy.
YAGNI/KISS: mira cómo se llama `formatear_precio` en los tests (siempre con un solo argumento);
los otros parámetros son futuro imaginado → bórralos y deja la firma `formatear_precio(monto)`.
Revisa la sección 4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-2/clean-code-dry-kiss-yagni/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-2/` — no la mires antes de intentarlo
de verdad. El corrector pondrá especial atención en tu `decisiones.md`: el color verde de los
tests no demuestra criterio; tu justificación, sí.
