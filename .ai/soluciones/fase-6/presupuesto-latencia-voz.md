---
ejercicio_id: fase-6/presupuesto-latencia-voz
fase: fase-6
sub_unidad: "6.12"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de medir**:
> el alumno debe corregir su trabajo, no recibir este código. Úsala para detectar el error y
> graduar las pistas.

# Solución de referencia — El cerebro de un voice agent: latencia percibida + barge-in

## Respuesta canónica (implementación)

```python
from __future__ import annotations

ETAPAS_PERCIBIDAS = ("vad_endpoint", "stt", "llm_ttft", "tts_primer_audio", "red")


def latencia_percibida(etapas):
    return sum(etapas.get(clave, 0) for clave in ETAPAS_PERCIBIDAS)


def decidir_barge_in(agente_hablando, voz_usuario_detectada):
    if agente_hablando and voz_usuario_detectada:
        return "interrumpir"
    if agente_hablando and not voz_usuario_detectada:
        return "seguir_hablando"
    if not agente_hablando and voz_usuario_detectada:
        return "escuchar"
    return "esperar"


def evaluar_turno(etapas, agente_hablando, voz_usuario_detectada, target_ms=250.0):
    latencia = latencia_percibida(etapas)
    return {
        "latencia_ms": latencia,
        "cumple": latencia <= target_ms,
        "accion": decidir_barge_in(agente_hablando, voz_usuario_detectada),
    }
```

## Razonamiento paso a paso

1. **`latencia_percibida` recorre un conjunto fijo, no el dict completo.** Iterando sobre
   `ETAPAS_PERCIBIDAS` y usando `etapas.get(clave, 0)` se logran tres cosas a la vez: se
   **ignoran** `llm_total`, `tts_total` y cualquier clave desconocida (no están en el
   conjunto), una etapa **ausente** vale 0 (no hay `KeyError`), y el dict vacío da 0. El
   insight de fondo: el total de generación ocurre **mientras el agente ya habla** (gracias
   al streaming), así que no cuenta para el time-to-first-audio.
2. **`decidir_barge_in` es una tabla de verdad de dos booleanos → cuatro estados.** El error
   es colapsar casos. "interrumpir" es **solo** cuando ambos son verdaderos (el usuario habla
   encima del agente). "escuchar" (usuario habla, agente callado) es un turno normal, **no**
   un barge-in — confundirlos es el fallo típico.
3. **`evaluar_turno` compone, no recalcula.** Llama a `latencia_percibida` para el número y a
   `decidir_barge_in` para la acción; el `cumple` usa `<=` (la regla documentada es "cumple si
   latencia <= target"). El `target_ms` por defecto es 250 (la vara del S2S), pero es
   parametrizable para evaluar un target turn-based realista (p. ej. 800).

### Traza de los 3 casos del README
- **Caso A:** `100 + 100 + 50 = 250` (solo vad_endpoint, stt, red presentes), target 250 →
  `cumple=True` (250 <= 250); agente callado + usuario habla → `accion="escuchar"`.
- **Caso B:** suma de las 5 percibidas `120+80+180+90+40 = 510` (ignora `llm_total=900` y
  `tts_total=1500`), target 250 → `cumple=False`; ambos hablan → `accion="interrumpir"`.
  **Este es el caso clave:** quien suma todo obtiene 2430 y concluye mal.
- **Caso C:** `decidir_barge_in(True, False)` → `"seguir_hablando"` (el agente habla y el
  usuario no; no hay nada que interrumpir).

## Puntos resbalosos (donde el corrector debe mirar)

1. **Sumar `llm_total`/`tts_total`:** el error conceptual #1. Lo atrapa
   `test_latencia_suma_solo_las_etapas_percibidas` (espera 510, no 2430).
2. **`KeyError` con etapa ausente:** usar `etapas["clave"]` en vez de `.get(clave, 0)`. Lo
   atrapa `test_latencia_etapa_ausente_cuenta_como_cero`.
3. **No ignorar claves desconocidas:** sumar sobre `etapas.values()` mete `ruido_misterioso`.
   Lo atrapa `test_latencia_ignora_claves_desconocidas`.
4. **`decidir_barge_in` con menos de 4 salidas:** colapsar "escuchar"/"esperar", o devolver
   solo un booleano. Lo atrapan los cuatro tests de barge-in.
5. **`cumple` con `<`:** el caso exactamente en el target cae mal. Lo atrapa
   `test_evaluar_en_el_target_cumple`.
6. **`evaluar_turno` que reimplementa** la suma o la tabla: duplicación; marca aunque los
   tests pasen (criterio C3).

## Rango de soluciones aceptables

- En `latencia_percibida`, un bucle `for` explícito con acumulador es igual de válido que la
  comprensión con `sum(...)`, siempre que ignore lo no-percibido y maneje ausentes.
- En `decidir_barge_in`, un `match`/`case` sobre la tupla `(agente_hablando,
  voz_usuario_detectada)` o un diccionario de mapeo son alternativas válidas y limpias.
- Los **nombres de los cuatro estados** deben coincidir con los del contrato
  (`"interrumpir"`, `"seguir_hablando"`, `"escuchar"`, `"esperar"`) porque los tests los
  comparan por igualdad exacta.
- **Profundización opcional (excelente, no requerida):** umbrales/target por escenario,
  devolver también qué etapa domina la latencia (para guiar el recorte), o calcular el
  ahorro de cancelar el trabajo en vuelo. No penalizar a quien hace solo lo pedido.
