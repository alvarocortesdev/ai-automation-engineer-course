# Ejercicio 6.13 — ¿A qué volumen se paga el fine-tuning? (break-even por costo)

> **Modalidad: mixto (a mano + código).** Primero calculas a mano, sin ejecutar ni usar
> IA. Luego implementas tres funciones puras que deciden **cuándo el fine-tuning gana por
> costo** — la cuenta que un AI Engineer hace antes de proponer "fine-tuneemos para
> ahorrar".

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.13` Fine-tuning en sistema híbrido
**Ruta:** opcional / profundización · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Calcular el **costo por request** del baseline (prompt largo de few-shot) y del
  modelo fine-tuneado (prompt corto, precio por token a veces distinto), a partir de tokens
  y pricing **por millón**.
- **O2** — Calcular el **punto de equilibrio** en requests donde el fine-tuning (costo
  **fijo** de entrenamiento + costo por request **menor**) iguala al baseline (sin costo
  fijo, costo por request **mayor**).
- **O3** — Explicar por qué, si el modelo fine-tuneado **no** es más barato por request, el
  fine-tuning **nunca** se paga por costo, sin importar el volumen.

## El problema

El fine-tuning, cuando gana por costo, lo hace porque te deja **acortar el prompt**: el
comportamiento que antes conseguías con un few-shot enorme (caro en cada request) queda
horneado en los pesos, así que mandas un prompt corto. Pero hay dos costos que lo frenan:

1. Un **costo fijo de entrenamiento**, que pagas una sola vez.
2. A veces, los modelos fine-tuneados cuestan **más por token** que el base.

```
costo_baseline_total(n)    = n × costo_por_request_baseline              (sin costo fijo)
costo_finetuning_total(n)  = costo_entrenamiento + n × costo_por_request_ft

equilibrio = costo_entrenamiento / (costo_req_baseline − costo_req_ft)
```

Por **debajo** del equilibrio gana el baseline; por **encima** (volumen alto y sostenido)
gana el fine-tuning. Y si `costo_req_ft >= costo_req_baseline`, el ahorro por request es
cero o negativo: **no hay equilibrio** y el fine-tuning nunca se paga por costo.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, con estos datos:

```
BASELINE (prompt largo de few-shot):
  2000 tokens de entrada + 200 de salida por request
  precios: in = 0.40 , out = 1.60   (USD por millón de tokens)

FINE-TUNING (prompt corto, modelo un poco más caro por token):
  200 tokens de entrada + 200 de salida por request
  precios: in = 0.60 , out = 2.40   (USD por millón de tokens)
  costo de entrenamiento (una vez): 26 USD
```

Calcula **a mano** (sin ejecutar): (a) el costo por request del baseline, (b) el costo por
request del fine-tuneado, (c) el **ahorro por request**, (d) el **punto de equilibrio** en
requests, y (e) si una empresa hace **20.000 requests/mes**, ¿cuánto cuesta cada opción ese
mes y cuál gana? Escribe una línea de razonamiento por paso. **No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~25 min

1. Abre `costo_finetuning.py` y completa las tres funciones (no cambies sus firmas).
   `costo_total` se reusa para baseline (costo fijo 0) y para fine-tuning (costo fijo =
   entrenamiento).
2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.
4. Añade **al menos un test propio**: un caso borde que se te ocurra (por ejemplo, un costo
   de entrenamiento de 0, o un ahorro por request negativo).

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, responde en 2-3 frases: ¿por qué el fine-tuning **no** es "siempre más
barato"? ¿Qué pasa con el punto de equilibrio si el modelo fine-tuneado cuesta **más** por
token que el baseline, y por qué? Nombra además **una** razón distinta del costo por la que
igual podrías fine-tunear (pista: la lección habla de formato/estilo/consistencia).

## Contrato de las funciones

```python
def costo_por_request(prompt_tokens, output_tokens, precio_in, precio_out) -> float: ...
def costo_total(costo_fijo, costo_req, n_requests) -> float: ...
def requests_equilibrio_finetuning(costo_entrenamiento, costo_req_baseline, costo_req_ft) -> float:
    """Lanza ValueError si el ahorro por request (baseline − ft) es <= 0."""
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — los cálculos a mano + quién gana a 20.000 requests, **antes** de ejecutar.
- `costo_finetuning.py` — con las tres funciones completadas (los tests pasan).
- `verificacion.md` — la reflexión sobre por qué el fine-tuning no es "siempre más barato".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con los cálculos y el ganador a 20.000 requests, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] `requests_equilibrio_finetuning` **falla** (ValueError) cuando el ahorro por request es
      cero o negativo.
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` explica que sin ahorro por request no hay equilibrio, y nombra una
      razón no-costo (formato/estilo/consistencia) para fine-tunear.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El `1e6` aparece porque el pricing viene **por millón** de tokens. El punto de equilibrio
es una división: el costo fijo de entrenamiento dividido por **lo que ahorras en cada
request** (el costo por request del baseline menos el del fine-tuneado). Si ese ahorro es
cero o negativo —porque el modelo fine-tuneado cuesta igual o más por request— la división
no tiene sentido de negocio: no hay número de requests que recupere el costo de
entrenamiento. Ahí va el `ValueError`. Revisa la sección "Non-examples" de la lección
(el punto sobre "fine-tuning siempre sale más barato") antes de mirar la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/break-even-finetuning-vs-prompt/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir?) y tu **comprensión** (¿la
reflexión explica que sin ahorro por request no hay equilibrio?), no solo si los tests
pasan. La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
