# spec-first-divisor-cuenta — Spec-first: divisor de cuenta

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.8` Spec-first y lectura de stack traces
**Ruta:** crítica · **Modalidad:** mixto (spec + código) · **Timebox:** 35–45 min

## 🎯 Objetivo

Escribir **primero la mini-spec y solo después el código** de `dividir_cuenta(total, personas)`, que
reparte una cuenta en partes iguales y devuelve cuánto paga cada persona. La spec es tu lista de tests
escrita en español: cada caso borde que anotes se convierte en un test o en una rama de validación.

## 📋 Contexto

Pensar el contrato **antes** de programar (qué entra, qué sale, qué casos raros) es la semilla del
*spec-driven development*, un hilo que recorre todo el curso (en la Fase 2 lo formalizarás con Spec Kit
y ADRs). Cuesta dos minutos y caza bugs cuando todavía son baratos: en tu cabeza, no en producción. El
Capstone F0 arranca exactamente así.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, sin IA (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta **documentación oficial** de Python si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, escribe la mini-spec **de memoria**. Si no puedes nombrar los bordes, ahí está tu punto débil.

## 🛠️ Instrucciones

El orden es **innegociable**:

1. **Primero la spec.** Crea `spec.md` (tú lo escribes) con una tabla de tres partes —**entradas /
   salida / casos borde**— para `dividir_cuenta`. Mínimo estos bordes: total negativo, total cero, cero
   personas, personas negativas, y división no exacta. Anota también tu **decisión de diseño** sobre el
   redondeo (¿devuelves el `float` completo o redondeas a peso?).
2. **Después el código.** Abre `dividir_cuenta.py` y completa la función `dividir_cuenta` (no cambies su
   firma) para cumplir **tu** spec. Recuerda: **valida antes de dividir**.
3. **Verifica.** Corre los tests hasta que pasen todos en verde:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. **Cierra el loop.** Agrega en `test_dividir_cuenta.py` **un test tuyo** para un caso borde de tu spec
   que los tests de base no cubran.

> El contrato que fijan los tests: `dividir_cuenta` devuelve `total / personas` como `float` **sin
> redondear**; `total < 0` y `personas <= 0` lanzan `ValueError`; `total == 0` es válido. Tu `spec.md`
> debe llegar a este mismo contrato razonándolo, no copiándolo.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `spec.md` existe, fue escrito **antes** del código, y lista entradas, salida y **al menos 4 casos
      borde**.
- [ ] Cada caso borde de la spec aparece como un **test** o como una **rama de validación** del código.
- [ ] Los tests pasan; cuentas inválidas (total negativo, cero/menos personas) lanzan `ValueError`
      (no `ZeroDivisionError`).
- [ ] La validación ocurre **antes** de la división.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar **sin notas** por qué validar antes de dividir y por qué la spec primero caza más bugs.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Tu spec es tu lista de tests: si escribiste "cero personas → ValueError" como caso borde, eso es un test
y una rama `if`. El **orden dentro de la función** importa: valida `personas <= 0` y `total < 0`
**antes** de dividir, porque `total / 0` revienta con `ZeroDivisionError` antes de que puedas lanzar tu
`ValueError` con un mensaje claro. Y la decisión de diseño del redondeo: el contrato pide el `float`
completo; si tú habrías redondeado, anótalo en la spec como una alternativa que descartaste a propósito.
Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `spec.md`, `dividir_cuenta.py`, `test_dividir_cuenta.py`),
- la **rúbrica**: `.ai/rubricas/fase-0/spec-first-divisor-cuenta.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-0/spec-first-divisor-cuenta.md` — no la mires
antes de intentarlo de verdad.
