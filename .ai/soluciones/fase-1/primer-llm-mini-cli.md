---
ejercicio_id: fase-1/primer-llm-mini-cli
fase: fase-1
sub_unidad: "1.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tu primer LLM en una mini-CLI

## Respuesta canónica

```python
from __future__ import annotations

import os
import sys
from typing import Callable, Mapping

MODELO = "claude-haiku-4-5"
MAX_TOKENS = 1024

Preguntar = Callable[[str], str]


class PromptVacio(ValueError): ...
class FaltaApiKey(RuntimeError): ...
class ModeloInalcanzable(RuntimeError): ...


def leer_api_key(entorno: Mapping[str, str]) -> str:
    clave = entorno.get("ANTHROPIC_API_KEY", "").strip()
    if not clave:
        raise FaltaApiKey(
            "Falta la variable de entorno ANTHROPIC_API_KEY. "
            "Expórtala antes de correr: export ANTHROPIC_API_KEY='tu-clave'"
        )
    return clave


def responder(prompt: str, preguntar_al_modelo: Preguntar) -> str:
    if not prompt or not prompt.strip():
        raise PromptVacio("el prompt no puede estar vacío")
    return preguntar_al_modelo(prompt).strip()


def preguntar_a_claude(prompt: str) -> str:
    import anthropic  # dentro: los tests corren sin el paquete

    cliente = anthropic.Anthropic()  # lee ANTHROPIC_API_KEY del entorno
    try:
        mensaje = cliente.messages.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError as e:
        raise FaltaApiKey("API key inválida o ausente") from e
    except anthropic.APIError as e:        # red, rate limit (429), 5xx...
        raise ModeloInalcanzable(str(e)) from e
    return mensaje.content[0].text


def main(argv: list[str], entorno: Mapping[str, str],
         preguntar: Preguntar = preguntar_a_claude) -> int:
    prompt = " ".join(argv).strip()
    if not prompt:
        print("uso: python solucion.py <tu pregunta>", file=sys.stderr)
        return 2
    try:
        leer_api_key(entorno)               # falla temprano y claro si no hay key
        salida = responder(prompt, preguntar)
    except FaltaApiKey as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except ModeloInalcanzable as e:
        print(f"error: el modelo no respondió ({e})", file=sys.stderr)
        return 4
    print(salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], os.environ))
```

(Las excepciones de dominio y las constantes `MODELO`/`MAX_TOKENS` vienen en el starter.)

## Razonamiento paso a paso

1. **El secreto vive en el entorno.** `leer_api_key` sólo lee `ANTHROPIC_API_KEY` y lanza `FaltaApiKey`
   si falta o está vacía. El SDK la lee por su cuenta vía `anthropic.Anthropic()`; `leer_api_key` es
   un **gate amistoso** para fallar temprano con un mensaje útil, no un segundo origen de verdad. El
   valor de la key nunca se imprime.
2. **Validar antes de gastar.** `responder` lanza `PromptVacio` **antes** de delegar: no tiene sentido
   tocar la red (ni pagar) por un prompt vacío. Esa validación va antes de `preguntar_al_modelo(...)`.
3. **El núcleo no sabe del SDK.** `responder` recibe `preguntar_al_modelo` **inyectado**: idéntico al
   seam de `fetch` de 1.5. No importa `anthropic`, no atrapa errores del SDK. Eso lo hace testeable
   sin red, sin key y sin el paquete instalado.
4. **El adaptador traduce los errores.** `preguntar_a_claude` es el único lugar que conoce el SDK:
   importa `anthropic` **dentro** (para no romper los tests offline), arma el llamado y mapea
   `AuthenticationError → FaltaApiKey` y `APIError → ModeloInalcanzable` (semilla de ports & adapters).
   Lee el texto en `content[0].text` (lista de bloques → primer bloque → `.text`).
5. **`main` ordena las guardas** en códigos de salida distintos: sin prompt → `2`; falta key → `3`;
   modelo inalcanzable → `4`; éxito → imprime y `0`. `preguntar` está inyectado (default
   `preguntar_a_claude`) para que `main` también sea testeable con un fake.

## Por qué el seam (lo que de verdad enseña el ejercicio)

`preguntar_al_modelo` está inyectado: el núcleo no sabe de dónde viene la respuesta. En los tests es
un stub que devuelve texto o lanza una excepción —**sin red, sin tokens, sin key**. Es exactamente
cómo se testea cualquier código que llama a un LLM (formal en 2.11): el LLM es una API, se mockea su
respuesta igual que se mockeó `fetch` en 1.5. El corrector debe verificar que el alumno **entiende**
esto, no sólo que los tests pasan.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`import anthropic` a nivel de módulo.** "Funciona" si el paquete está instalado, pero rompe los
   tests offline y acopla el núcleo al SDK. Debe ir dentro del adaptador.
2. **Key hardcodeada o impresa.** `Anthropic(api_key="sk-...")` o `print(clave)` = secreto filtrado.
   El valor de la key nunca debe aparecer en el código ni en la salida.
3. **`content` tratado como string.** El texto está en `content[0].text`; `content` es una lista.
4. **Validar después de llamar.** Gasta una petición en input ya inválido. El test
   `modelo_que_no_debe_correr` lo detecta con un `AssertionError`.
5. **`except Exception` genérico en `responder`.** El mapeo de errores va en el adaptador, con tipos
   del SDK (`AuthenticationError`, `APIError`); `responder` no debe envolver nada.
6. **Omitir `max_tokens`.** Es obligatorio; sin él, el SDK rechaza la llamada.

## Rango de soluciones aceptables
- **`leer_api_key` con o sin `.strip()`:** rechazar la cadena vacía es `competente`; rechazar también
  "solo espacios" (con `.strip()`) es más robusto, pero ambos cumplen si pasan los tests dados.
- **Códigos de salida exactos:** los tests fijan `0/2/3/4`. Mientras sean distintos y consistentes con
  los tests, el texto de los mensajes a `stderr` es libre.
- **`responder` con `.strip()` o sin él:** el test `test_responder_recorta_espacios` exige el `.strip()`
  sobre la salida; quitarlo lo hace fallar.
- **Mapeo de errores del adaptador:** atrapar `anthropic.APIConnectionError`/`RateLimitError` por
  separado y mapearlos también a `ModeloInalcanzable` es válido (son subclases de `APIError`); colapsar
  todo en `APIError` es `competente`, distinguirlos es `excelente`. Distinguir además 4xx vs 5xx para
  decidir reintento (de 1.5/3.14) es bonus, no exigido.
- **`main` validando la key con `leer_api_key` vs delegando en el SDK:** llamar `leer_api_key` para
  fallar temprano es lo esperado por los tests (`test_main_sin_api_key_devuelve_3` no llama al modelo).
  Una solución que sólo descubra la falta de key cuando el SDK falla **no** pasaría ese test (gastaría
  la llamada), así que el gate previo es parte del contrato aquí.
