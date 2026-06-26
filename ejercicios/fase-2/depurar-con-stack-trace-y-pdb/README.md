# 2.12 — Caza el bug con método: stack trace → pdb → test de regresión

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.12` Debugging y código legado
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** código

## 🎯 Objetivo

Depurar un bug de **código legado** (que no escribiste) con **método científico**, no
con `print` al azar ni "que la IA lo reescriba": reproducir, leer el stack trace,
formar una hipótesis, confirmarla con `pdb`, capturar el bug con un **test de
regresión que falle primero**, y arreglar **solo la causa raíz**.

## 📋 Contexto

`resumen_cuenta(movimientos)` ya estaba en producción y tiene el bug del ticket
**#412**: "revienta para cuentas que solo tienen abonos". Es el caso realista del
trabajo: casi todo el código que tocas llega así, sin tests y reportado por alguien
más. Quien entra, entiende el fallo y lo arregla **sin romper nada** es quien vale la
banda semi-senior. Alimenta directo el **Capstone F2** (entrar a tu propio código
viejo y dejarlo mejor).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Depura tú: trace, hipótesis, pdb.
2. Solo entonces, consulta la [doc oficial de `pdb`](https://docs.python.org/3/library/pdb.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *encontrar el bug por ti*.
4. Mañana, **reescríbelo de memoria**. Si no puedes depurarlo sin ayuda, no lo aprendiste.

## 🛠️ Instrucciones (orden ESTRICTO)

1. **Reproduce.** Corre los tests y mira el rojo:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

   `test_regresion_412_solo_abonos` falla con un `ValueError`. Copia el **stack
   trace** completo en `traza.md` y léelo de **abajo hacia arriba**: anota el tipo
   de excepción, el mensaje, y el **frame exacto de `solucion.py`** donde nace.

2. **Hipótesis + confirmación con el debugger.** Escribe tu hipótesis en una frase.
   Confírmala con `pdb` (no con `print`). Dos formas válidas:

   ```bash
   python -m pdb -c continue solucion.py    # post-mortem al reventar
   ```

   o pon un `breakpoint()` en `resumen_cuenta` y corre el caso. Una vez detenido,
   inspecciona el estado (`p cargos`, `p abonos`, `w`) y **pega en `traza.md`** los
   comandos que usaste y lo que viste.

3. **Test de regresión rojo.** Completa el `TODO` de `test_regresion_412_solo_abonos`
   (afirma cuánto vale `mayor_cargo` cuando no hay cargos). Míralo **fallar** antes de
   tocar `solucion.py`.

4. **Arregla la causa raíz.** Cambio **mínimo** en `solucion.py`. Declara en `traza.md`
   tu decisión de diseño: ¿`mayor_cargo` es `0` o `None` sin cargos? ¿por qué? Corre
   `pytest`: todo verde (el de regresión pasa, el normal sigue pasando).

5. **Dos sombreros (deuda separada).** El módulo además **ignora en silencio** un
   movimiento con `tipo` desconocido (ni `"abono"` ni `"cargo"`). Eso NO es el ticket
   #412: **no lo arregles aquí**. Ya hay un test `xfail` que lo registra como deuda;
   anótalo también en `traza.md` como un bug futuro con su propio ticket.

> ⚠️ **Arregla la causa, no el síntoma.** Envolver `max(cargos)` en un `try/except`
> que devuelva `0` "apaga" el error pero se tragaría cualquier otro `ValueError`
> real. La causa raíz es que `max([])` no tiene valor: usa el mecanismo que Python
> da para "máximo o un default".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `traza.md` demuestra que **leíste el trace** (tipo, mensaje, frame exacto).
- [ ] `traza.md` muestra una **sesión real de pdb** (comandos + el valor de `cargos` observado).
- [ ] El test de regresión **falló primero** y ahora pasa; `test_caso_normal_funciona` sigue verde.
- [ ] El fix ataca la **causa raíz** (no un `try/except` que traga el error) y no cambia comportamiento ajeno.
- [ ] La rareza del `tipo` desconocido queda **anotada como deuda**, no "arreglada de paso".
- [ ] Puedes explicar **sin notas** por qué el test de regresión va **antes** que el fix.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.py` — el módulo con la causa raíz arreglada (cambio mínimo).
- `test_solucion.py` — con el `TODO` del test de regresión completado.
- `traza.md` — stack trace leído + hipótesis + sesión de pdb + decisión de diseño + deuda anotada.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El mensaje `max() ... is empty` lo dice todo: alguien llamó `max()` con una secuencia
vacía. ¿Cuál, y por qué está vacía cuando solo hay abonos? Confírmalo: `p cargos` en el
frame del crash → `[]`. El fix idiomático para "el máximo, o un valor por defecto si
está vacío" es el parámetro `default=` de `max()` (`max(cargos, default=0)`). Para los
dos sombreros: el `tipo` desconocido cae fuera de los dos `_solo(...)`, así que no se
suma a ningún lado — eso ya lo pinta el test `xfail`; no lo "corrijas" en este ticket.
Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `traza.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/depurar-con-stack-trace-y-pdb.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/depurar-con-stack-trace-y-pdb.md`
— no la mires antes de intentarlo de verdad.
