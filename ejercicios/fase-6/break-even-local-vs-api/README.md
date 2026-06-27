# Ejercicio 6.10 — Calculadora del punto de equilibrio local vs API

> **Modalidad: mixto (a mano + código).** Primero calculas a mano, sin ejecutar ni usar
> IA. Luego implementas tres funciones puras que deciden **cuándo conviene servir local**
> por costo — la cuenta que un AI Engineer hace antes de proponer "corramos esto on-prem".

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.10` Open-source, local y serving
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Calcular el **costo por request** y el **costo mensual** de una API a partir de
  los tokens de entrada/salida y el pricing **por millón** de tokens.
- **O2** — Calcular el **punto de equilibrio** en requests donde servir local (costo
  **fijo** de GPU) iguala a la API (costo **variable** por request).
- **O3** — Explicar por qué a **volumen bajo o variable** la API casi siempre gana por
  costo.

## El problema

El costo de una **API** es **variable**: sube linealmente con cada request. El costo de
**servir local** es **fijo**: pagas la GPU por hora, esté ociosa o llena. Por eso la
pregunta "¿local o API?" tiene una respuesta de costo que se **calcula**, no se opina:

```
costo_api_mensual   = requests_mes × costo_por_request          (lineal)
costo_local_mensual = horas_del_mes × costo_por_hora_de_GPU      (fijo)

requests_equilibrio = costo_local_mensual / costo_por_request
```

Por **debajo** del equilibrio gana la API; por **encima** (volumen alto y sostenido) gana
local. Saber dónde cae ese número es lo que separa una migración a local justificada de
una hecha "porque suena pro".

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, con estos datos:

```
API:   1000 tokens de entrada + 1000 de salida por request
       precios: in = 0.20 , out = 0.80   (USD por millón de tokens)
Local: GPU rentada a 1.00 USD/hora, corriendo 730 horas al mes
```

Calcula **a mano** (sin ejecutar): (a) el costo por request, (b) el costo local mensual,
(c) el **punto de equilibrio** en requests/mes, y (d) si una empresa hace **20.000
requests/mes**, ¿cuánto le cuesta cada opción y cuál gana? Escribe una línea de
razonamiento por paso. **No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~25 min

1. Abre `costo_serving.py` y completa las tres funciones (no cambies sus firmas).
   `punto_equilibrio_requests` debe **reusar** `costo_api_por_request`, no reimplementar la
   fórmula.
2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.
4. Añade **al menos un test propio**: un caso borde que se te ocurra (por ejemplo, qué pasa
   con un costo local de 0, o con un request de solo salida).

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, responde en 2-3 frases: ¿por qué local **no** es "siempre más
barato"? ¿Qué otra razón —fuera del costo— podría justificar servir local **aunque** estés
por debajo del punto de equilibrio?

## Contrato de las funciones

```python
def costo_api_por_request(tokens_in, tokens_out, precio_in, precio_out) -> float: ...
def costo_api_mensual(requests_mes, tokens_in, tokens_out, precio_in, precio_out) -> float: ...
def punto_equilibrio_requests(costo_local_mensual, tokens_in, tokens_out, precio_in, precio_out) -> float:
    """Lanza ValueError si el costo por request es 0 (una API gratis no tiene equilibrio)."""
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — los cálculos a mano + quién gana a 20.000 requests, **antes** de ejecutar.
- `costo_serving.py` — con las tres funciones completadas (los tests pasan).
- `verificacion.md` — la reflexión sobre por qué local no es "siempre más barato".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con los cálculos y el ganador a 20.000 requests, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] `punto_equilibrio_requests` **reusa** `costo_api_por_request` y **falla** (ValueError)
      cuando el costo por request es 0.
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` explica que local es costo fijo y nombra una razón no-costo (privacidad/latencia).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El `1e6` aparece porque el pricing viene **por millón** de tokens. El punto de equilibrio
es una simple división: cuánto cuesta la GPU fija, dividido por lo que cuesta **un**
request en la API. Si el costo por request fuera 0, esa división no tiene sentido (no hay
número de requests gratis que iguale un costo positivo): ahí va el `ValueError`. Revisa la
sección "punto de equilibrio" de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/break-even-local-vs-api/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir?) y tu **comprensión**
(¿la reflexión explica que local es costo fijo?), no solo si los tests pasan. La **solución
de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de intentarlo de verdad.
