# Ejercicio 6.3 — Calculadora de costo y elección de modelo

> **Modalidad: mixto (a mano + código).** Primero calculas a mano, sin ejecutar ni
> usar IA. Luego implementas dos funciones puras: cuánto cuesta una llamada y cuál es
> el modelo más barato para una carga dada — la cuenta que un AI Engineer hace de
> cabeza antes de elegir un modelo.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.3` APIs de LLM
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O1** — Calcular el **costo en USD** de una llamada a partir de los tokens de
  entrada/salida y el pricing **por millón** de tokens.
- **O2** — Predecir a mano el costo en varios modelos y **cuál es el más barato**, sin
  ejecutar.
- **O3** — Explicar por qué la **salida** pesa más que la entrada en el costo total.

## El problema

El costo de una llamada a un LLM se calcula sobre **tokens**, con precios distintos para
la **entrada** (lo que mandas) y la **salida** (lo que el modelo genera), y casi siempre
la salida cuesta más. La fórmula, con el pricing dado **por millón** de tokens
(1M = 1 000 000):

```
costo_usd = (tokens_entrada / 1e6) * precio_entrada
          + (tokens_salida  / 1e6) * precio_salida
```

Elegir el modelo **más barato que hace el trabajo** (model routing) es una de las
palancas de costo más grandes en producción. Aquí construyes la base de esa decisión.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, usa esta tabla de precios (USD por millón de tokens):

```
opus    -> in: 5,  out: 25
sonnet  -> in: 3,  out: 15
haiku   -> in: 1,  out: 5
```

Para una llamada de **10 000 tokens de entrada** y **2 000 de salida**, calcula **a
mano** el costo en los **tres** modelos y di **cuál es el más barato**, con una línea de
razonamiento por modelo. **No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~25 min

1. Abre `costo.py` y completa `calcular_costo(...)` y `modelo_mas_barato(...)` (no
   cambies sus firmas). El pricing se **inyecta** como parámetro `precios`: así pruebas
   la lógica sin depender de ninguna API ni de precios reales.

2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, explica en 2-3 frases por qué la **salida** suele pesar más que la
entrada en el costo, y qué implica eso para un modelo que tiende a responder de forma
**muy verbosa** (mucho texto de salida).

## Contrato de las funciones

```python
def calcular_costo(tokens_entrada, tokens_salida, modelo, precios) -> float:
    """precios: {modelo: {"in": $/1M_entrada, "out": $/1M_salida}, ...}
    Lanza KeyError/ValueError si `modelo` no está en `precios`."""

def modelo_mas_barato(tokens_entrada, tokens_salida, precios) -> str:
    """Devuelve el NOMBRE del modelo más barato para esa carga.
    Lanza ValueError si `precios` está vacío."""
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — costo a mano en los 3 modelos + cuál es el más barato, **antes** de ejecutar.
- `costo.py` — con las dos funciones completadas (los tests pasan).
- `verificacion.md` — la reflexión sobre por qué la salida pesa más.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con los cálculos + el más barato, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] `calcular_costo` usa la fórmula por millón, maneja 0 tokens, y **falla** (excepción)
      ante un modelo que no está en la tabla.
- [ ] `verificacion.md` conecta el precio de salida con el costo de una respuesta verbosa.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/costo-llamada-llm/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir?) y tu **comprensión**
(¿la reflexión explica por qué la salida pesa más?), no solo si los tests pasan.
