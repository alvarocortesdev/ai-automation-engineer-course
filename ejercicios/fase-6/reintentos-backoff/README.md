# Ejercicio 6.3 — Reintentos con backoff exponencial + jitter

> **Modalidad: mixto (a mano + código).** Primero predices la secuencia de esperas a
> mano, sin ejecutar ni usar IA. Luego implementas el corazón de la resiliencia: la
> función que reintenta una operación que falla de forma transitoria, sin tumbar al
> servidor que ya está saturado.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.3` APIs de LLM
**Ruta:** crítica · **Timebox:** 45 min

## Objetivos

- **O1** — Implementar **reintentos con backoff exponencial + jitter** que respeten el
  `Retry-After` del servidor y un **tope** de espera.
- **O2** — Distinguir errores **reintentar-ables** (que reintentas) de los que se
  **propagan de inmediato** (request inválido, key mala).
- **O3** — Predecir la **secuencia exacta de esperas** sin ejecutar.

## El problema

Bajo carga, una API te responde `429` (rate limit) o `5xx` (caída temporal). La
respuesta correcta no es reescribir el código: es **reintentar con paciencia
creciente**. El patrón estándar:

1. **Backoff exponencial:** esperas cada vez más entre intentos — `base·2⁰`, `base·2¹`,
   `base·2²`... — con un **tope** para no esperar eternamente.
2. **Jitter:** le sumas un componente **aleatorio** a la espera, para que mil clientes
   que fallaron al mismo segundo no reintenten todos exactamente al mismo segundo
   siguiente (eso es el **thundering herd**, que vuelve a tumbar al servidor).
3. **Retry-After gana:** si el servidor dijo "vuelve en N segundos", **ese** número
   manda sobre tu backoff calculado.
4. **No todo se reintenta:** un `400` (request mal armado) o un `401` (key inválida) se
   propagan de inmediato — reintentar manda el mismo error.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~12 min

En un archivo `prediccion.md`, para este caso (con **jitter = 0** para que sea exacto):

```
una operación que SIEMPRE falla con ErrorReintentable (sin retry_after)
max_intentos = 6
base = 1.0
tope = 8.0
aleatorio(base) = 0   (jitter cero)
```

Predice la **lista exacta de esperas** que se acumularían (en orden), y explica en una
línea por qué la última no es `16`. **No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~28 min

1. Abre `backoff.py` y completa `reintentar_con_backoff(...)` (no cambies su firma). El
   reloj (`dormir`) y el jitter (`aleatorio`) se **inyectan** como parámetros: así los
   tests son deterministas y **no necesitan red ni tiempo real**.

2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, explica en 2-3 frases (1) por qué reintentar un `400` (request
inválido) está mal, y (2) por qué el **jitter** importa cuando hay **muchos** clientes
fallando a la vez (qué pasaría sin él).

## Contrato de la función

```python
def reintentar_con_backoff(operacion, *, max_intentos=5, base=1.0, tope=60.0,
                           dormir, aleatorio):
    """
    operacion: callable de 0 args. Devuelve un resultado, o lanza:
        - ErrorReintentable(retry_after=None|float)  -> reintentar.
        - cualquier OTRA excepción                   -> propagar de inmediato.
    Espera del intento i (que falla y no es el último): min(tope, base * 2**i) + jitter.
        Salvo que el error traiga retry_after, que GANA (sin jitter ni tope).
    dormir:    callable[[float], None]  inyectado (en tests, registra la espera).
    aleatorio: callable[[float], float] inyectado: recibe la espera base, devuelve el jitter.
    Devuelve el resultado en el primer éxito; si se agotan los intentos, RE-LANZA la última.
    """
```

`ErrorReintentable` ya está definida en `backoff.py` (no la cambies).

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — la lista de esperas + por qué la última no es 16, **antes** de ejecutar.
- `backoff.py` — con la función completada (los tests pasan).
- `verificacion.md` — la reflexión (reintentar-able vs no, y el porqué del jitter a escala).

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con la lista de esperas + razonamiento, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] La función reintenta **solo** el error reintentable, respeta `retry_after` cuando
      viene, aplica el `tope` al backoff, y **re-lanza** la última excepción al agotarse.
- [ ] Un error **no** reintentable se propaga de inmediato (sin dormir, sin reintentar).
- [ ] `verificacion.md` distingue reintentar-able de no, y justifica el jitter a escala.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/reintentos-backoff/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste las esperas antes de medir?) y tu
**comprensión** (¿por qué el `Retry-After` gana? ¿por qué el jitter?), no solo si los
tests pasan.
