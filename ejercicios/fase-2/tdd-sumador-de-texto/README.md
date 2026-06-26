# 2.7 — Sumador de texto (kata de TDD desde cero)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.7` TDD obligatorio
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Construir una función `sumar(numeros: str) -> int` **test-driven**: tú escribes los
tests, uno por comportamiento, viendo el **rojo antes que el verde** en cada ciclo.
El entregable no es solo la función: es la **evidencia** de que diseñaste con tests
(la bitácora de ciclos) y no que escribiste el código y luego unos tests que ya pasaban.

## 📋 Contexto

`sumar` recibe una cadena con números y devuelve su suma. Es el kata clásico de TDD
(el "String Calculator" de Roy Osherove), elegido porque cada nuevo comportamiento
fuerza un pequeño cambio de diseño: el ritmo perfecto para practicar
**fake it → triangulación → refactor**. Lo que entrenas aquí es exactamente el hábito
que usarás en el **Capstone F2** sobre tu propia API.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Un comportamiento a la vez.
2. Solo entonces, consulta la [documentación oficial de pytest](https://docs.pytest.org/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* los tests ni el código.
4. Mañana, **reescríbelo de memoria**, ciclo por ciclo. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Trabaja los comportamientos **en este orden**. Para **cada uno**, completa un ciclo
red-green-refactor y anótalo en `bitacora.md`:

1. `sumar("")` devuelve `0`.
2. `sumar("1")` devuelve `1`.
3. `sumar("1,2")` devuelve `3`.
4. `sumar("1,2,3,4")` devuelve `10` (cualquier cantidad de números).
5. `sumar("1\n2,3")` devuelve `6` (el salto de línea `\n` también separa, igual que la coma).
6. `sumar(" 1 , 2 ")` devuelve `3` (ignora espacios alrededor de cada número).
7. `sumar("1,-2,3")` lanza `ValueError` y el mensaje **incluye** el número negativo.

El ciclo, sin saltarte pasos:

```bash
# 1. escribe el test del comportamiento en test_solucion.py
uv run pytest        # 2. CONFIRMA el ROJO (debe fallar por falta de código)
# 3. escribe el código MÍNIMO en solucion.py
uv run pytest        # 4. VERDE
# 5. refactor si hace falta -> uv run pytest entre cada cambio (siempre verde)
```

> ⚠️ **No escribas una línea de implementación sin un test rojo que la exija.**
> El starter de `test_solucion.py` ya trae **el primer test** escrito (comportamiento 1)
> y el de `solucion.py` lanza `NotImplementedError` para que arranque en rojo. Sigue tú.

### Auto-verificación (solo al final)

Cuando cierres tus 7 ciclos, corre la suite de aceptación que te damos:

```bash
uv run pytest acceptance_test.py
```

Comprueba que no se te escapó ningún comportamiento. **No la abras antes de terminar**:
te quita el trabajo de traducir la spec a tests, que es justo lo que se entrena.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Hay **un test por comportamiento** (1–7), escrito por ti en `test_solucion.py`.
- [ ] `bitacora.md` muestra el `🔴` (rojo) **antes** del `🟢` (verde) en cada ciclo.
- [ ] `uv run pytest` (tus tests) y `uv run pytest acceptance_test.py` están ambos en **verde**.
- [ ] El comportamiento 7 lanza `ValueError` con el número negativo en el mensaje, testeado con `pytest.raises`.
- [ ] No hay código en `solucion.py` que ningún test exija (nada "por si acaso").
- [ ] Puedes explicar **sin notas** qué es "fake it", qué es "triangulación", y dónde aparecieron.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.py` — tu implementación, crecida test a test.
- `test_solucion.py` — tus tests, uno por comportamiento.
- `bitacora.md` — el log de ciclos: por cada comportamiento, una línea
  `🔴 <qué probé> → 🟢 <qué código mínimo> → 🔵 <refactor o "nada">`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El comportamiento 1 sale con `if numeros == "": return 0`. Para el 2 y 3, "fake it"
pierde fuerza rápido: en cuanto tengas `"1,2"`, separa por coma, convierte a `int` y
suma. El 4 funciona **gratis** si usaste `split(",")` + `sum(...)` — esa es la gracia
de la triangulación. El 5 es el refactor clave: antes de separar, reemplaza `\n` por
`,` (`numeros.replace("\n", ",")`) y reusas tu split de una sola separación. El 6:
`.strip()` a cada parte antes de `int(...)`. El 7: junta los negativos en una lista y,
si no está vacía, `raise ValueError(f"...{negativos}")`. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `bitacora.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/tdd-sumador-de-texto.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/tdd-sumador-de-texto.md`
— no la mires antes de intentarlo de verdad.
