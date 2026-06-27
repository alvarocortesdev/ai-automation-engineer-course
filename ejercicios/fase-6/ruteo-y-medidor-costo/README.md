# Ejercicio 6.16 — Medidor de costo en vivo + router de modelos

> **Modalidad: mixto (a mano + código).** Primero calculas a mano, sin ejecutar ni usar IA.
> Luego implementas tres funciones puras: cuánto cuesta una llamada (contando el cache), a qué
> modelo rutear cada request, y cuánto sale el mes completo. Es la cuenta que un AI Engineer
> lleva a la reunión con el cliente.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.16` Costo/latencia + LLMOps
**Ruta:** crítica · **Timebox:** 45 min

## Objetivos

- **O1** — Calcular el **USD por request** desde `usage`, contando las **tres tarifas de input**
  por separado: fresco (1.0×), cache read (0.1×) y cache write (1.25×), más el output.
- **O2** — **Rutear** cada request al **modelo más barato** que cubre su dificultad (barato→caro).
- **O3** — Agregar el **costo mensual** sobre una mezcla de tráfico, con desglose por modelo.

## El problema

Apenas activas prompt caching, la respuesta de un LLM trae **tres** categorías de tokens de
entrada, cada una con su precio. Tratarlas todas igual hace que tu número de costo **mienta**.

| Campo de `usage` | Multiplicador sobre el precio de input |
|---|---|
| `input_tokens` (fresco) | **1.0×** |
| `cache_read_input_tokens` (servido del cache) | **0.1×** |
| `cache_creation_input_tokens` (escrito al cache) | **1.25×** |
| `output_tokens` | precio de **output** |

La fórmula del costo de una llamada (pricing **por millón** de tokens, 1M = 1.000.000):

```
costo = (input_tokens      / 1e6) * precio_in  * 1.00
      + (cache_read         / 1e6) * precio_in  * 0.10
      + (cache_write        / 1e6) * precio_in  * 1.25
      + (output_tokens      / 1e6) * precio_out * 1.00
```

El ruteo barato→caro manda cada request al modelo más barato que la resuelve, según su dificultad.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, usa esta tabla de precios (USD por millón, in / out):

```
haiku  -> in: 1,  out: 5
sonnet -> in: 3,  out: 15
opus   -> in: 5,  out: 25
```

1. Una request a **opus** con `usage`: input 2.000, cache_read 10.000, cache_write 0, output 500.
   Calcula su costo **a mano**, contando el cache_read a 0.1×. Luego di cuánto habría costado si
   esos 10.000 fueran input fresco.
2. Con `escalones = [(0.3, "haiku"), (0.7, "sonnet"), (1.0, "opus")]`, di qué modelo rutea cada
   dificultad: `0.3`, `0.71`, `1.4`.

**No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~25 min

1. Abre `medidor.py` y completa `costo_usd(...)`, `rutear_modelo(...)` y `costo_mensual(...)` (no
   cambies sus firmas). Los precios se **inyectan** como parámetro: tu lógica no depende de precios
   reales que cambian cada par de meses.
2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.
4. Añade al menos **un caso propio** en `test_medidor.py` (un borde que se te ocurra, p. ej. una
   request con `cache_write` mayor que 0).

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, explica en 2-3 frases: (a) por qué cachear un prefijo de **un solo uso**
pierde plata (pista: el multiplicador del cache write), y (b) cuándo rutear a un modelo barato
puede salir caro (calidad).

## Contrato de las funciones

```python
def costo_usd(usage, precio_in: float, precio_out: float) -> float:
    """USD de UNA llamada. `usage` tiene .input_tokens, .cache_read_input_tokens,
    .cache_creation_input_tokens, .output_tokens. Precios por millón de tokens."""

def rutear_modelo(dificultad: float, escalones: list[tuple[float, str]]) -> str:
    """Devuelve el modelo más barato cuyo techo >= dificultad. `escalones` va de menor a
    mayor capacidad. Si ninguno cubre, devuelve el último (más capaz).
    Lanza ValueError si `escalones` está vacío."""

def costo_mensual(trafico, escalones, precios) -> dict:
    """`trafico`: lista de requests, cada una con .dificultad y .usage.
    `precios`: {modelo: {"in": $/1M, "out": $/1M}, ...}.
    Rutea cada request, calcula su costo, y devuelve
    {"total": float, "por_modelo": {modelo: float, ...}}."""
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — las cuentas a mano, **antes** de ejecutar.
- `medidor.py` — con las tres funciones completadas (los tests pasan).
- `verificacion.md` — la reflexión sobre cache de un solo uso y ruteo barato.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con las cuentas + el ruteo, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] `costo_usd` cuenta cache_read a 0.1× y cache_write a 1.25× (no como input fresco).
- [ ] `rutear_modelo` maneja el borde exacto (`dificultad == techo`) y el fuera de rango.
- [ ] `costo_mensual` **reusa** `costo_usd` y `rutear_modelo` (no duplica lógica) y devuelve el
      desglose por modelo, no solo el total.
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` conecta el premium de cache write con "cachear de un solo uso pierde plata".

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/ruteo-y-medidor-costo/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir?) y tu **comprensión** (¿la
reflexión explica el premium del cache write?), no solo si los tests pasan. La **solución de
referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de intentarlo de verdad.
