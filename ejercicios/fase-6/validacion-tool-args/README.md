# Ejercicio 6.4 — Gate de validación de argumentos de una tool

> **Modalidad: código (sin IA para resolver).** Implementas el **hueco** del bucle de
> tool use: entre "el modelo pidió una herramienta" y "mi sistema la ejecuta" hay una
> decisión que es **tuya**. Aquí vive la seguridad de un agente.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.4` Structured outputs, function calling, tool use + MCP
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar `decidir(nombre, argumentos)`: dado el nombre de la tool que pidió el
modelo y el dict de argumentos (lo que ya extrajiste del bloque `tool_use`), devolver
una **decisión** —`EJECUTAR`, `RECHAZAR` o `CONFIRMAR`— aplicando, en este orden,
**permiso → forma → semántica**.

## 📋 Contexto

El modelo nunca ejecuta tu función: te **pide** una llamada con un nombre y unos
argumentos. Esos argumentos pueden tener forma perfecta (un `int` bien tipado) y aun
así ser peligrosos: una tool fuera de tu allowlist, un `pedido_id` negativo, un
reembolso de un millón. Este gate es lo que impide que un predictor de tokens, o una
inyección de prompt, le dé una orden directa a tu sistema. Es el corazón de la
seguridad del capstone de la fase (validar salida antes de ejecutar + least privilege
+ HITL).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** de pydantic.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ El dominio (tu gate decide sobre esto)

Dos tools permitidas (allowlist):

| Tool | Argumentos | Reversibilidad |
|---|---|---|
| `buscar_pedido` | `pedido_id` (entero positivo) | solo lectura (reversible) |
| `reembolsar` | `pedido_id` (entero positivo), `monto_clp` (entero positivo) | **irreversible** (mueve plata) |

Reglas del gate, **en este orden**:

1. **Permiso:** si `nombre` no está en la allowlist → `RECHAZAR` (sin mirar los
   argumentos).
2. **Forma:** valida los argumentos con un modelo **pydantic** por tool (tipos +
   requeridos + positivos). Si no validan → `RECHAZAR`.
3. **Semántica / negocio:** un `reembolsar` con `monto_clp` **sobre el techo**
   (`TECHO_REEMBOLSO_CLP = 200_000`) → `CONFIRMAR` (requiere humano). Dentro del techo
   → `EJECUTAR`. Un `buscar_pedido` válido → `EJECUTAR`.

## 🧩 Instrucciones

1. Abre `gate.py`. Tienes el dataclass `Decision`, los constantes y la firma de
   `decidir`. Escribe los **modelos pydantic** y la lógica de las tres capas.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_gate.py` (un caso borde que se te
   ocurra: ¿qué pasa con un argumento extra que no pediste?).

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — para los 3 casos de abajo, qué decisión predices y por qué.
  **Escríbelo ANTES de ejecutar.**
- `gate.py` — tu implementación (todos los tests en verde).
- `verificacion.md` — 2-3 frases: por qué la **forma válida** de los argumentos no
  basta para ejecutar, conectándolo con **Excessive Agency (OWASP LLM06)** y
  **least privilege**.

Los 3 casos a predecir en `prediccion.md`:
- `decidir("buscar_pedido", {"pedido_id": 8842})`
- `decidir("borrar_todo", {})`
- `decidir("reembolsar", {"pedido_id": 1, "monto_clp": 950000})`

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe **antes** de ejecutar, con las 3 predicciones + razón.
- [ ] Todos los tests pasan (`pytest`).
- [ ] Una tool fuera de la allowlist se **rechaza** sin validar sus argumentos.
- [ ] Un reembolso **sobre el techo** devuelve `CONFIRMAR` (HITL), no `EJECUTAR`.
- [ ] `verificacion.md` conecta la decisión con LLM06 / least privilege.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/validacion-tool-args/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
