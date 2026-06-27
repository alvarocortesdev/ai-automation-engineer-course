---
ejercicio_id: fase-6/model-card-y-audit-log
fase: fase-6
sub_unidad: "6.15"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno ni pegar el código. Es la
> **vara de medir**: úsala para detectar el error, nombrar la misconception y graduar pistas.
> Hay implementaciones válidas distintas (otra regex, otro hash); lo innegociable es el
> **comportamiento** (redactar, no guardar crudo, detectar manipulación) y un model card con
> out-of-scope honestos.

# Solución de referencia — Model card + audit log

## Parte A — `audit_log.py` (referencia, pasa los 10 tests)

```python
from __future__ import annotations

import hashlib
import json
import re

GENESIS = "0" * 64
CAMPOS_REQUERIDOS = (
    "request_id", "timestamp", "actor", "modelo", "prompt_version", "decision",
)

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_DIGITOS = re.compile(r"\d[\d.\-]{5,}\d")  # 7+ dígitos, admitiendo . y -


def redactar(texto: str) -> str:
    texto = _EMAIL.sub("<REDACTADO>", texto)
    texto = _DIGITOS.sub("<REDACTADO>", texto)
    return texto


def _hash_registro(registro: dict) -> str:
    # Excluye record_hash del contenido: si te incluyes a ti mismo no puedes recomputarlo.
    contenido = {k: v for k, v in registro.items() if k != "record_hash"}
    canonico = json.dumps(contenido, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonico.encode("utf-8")).hexdigest()


def registrar(evento: dict, prev_hash: str) -> dict:
    faltan = [c for c in CAMPOS_REQUERIDOS if c not in evento]
    if faltan:
        raise ValueError(f"Faltan campos requeridos: {faltan}")
    registro = {c: evento[c] for c in CAMPOS_REQUERIDOS}
    if "input_text" in evento:
        registro["input_redacted"] = redactar(evento["input_text"])  # NUNCA el crudo
    for c in ("confidence", "human_in_the_loop"):
        if c in evento:
            registro[c] = evento[c]
    registro["prev_hash"] = prev_hash
    registro["record_hash"] = _hash_registro(registro)
    return registro


def verificar_cadena(registros: list[dict]) -> bool:
    esperado_prev = GENESIS
    for r in registros:
        if r.get("prev_hash") != esperado_prev:
            return False
        if _hash_registro(r) != r.get("record_hash"):  # RECOMPUTA: detecta campos editados
            return False
        esperado_prev = r["record_hash"]
    return True
```

## Razonamiento paso a paso

1. **`redactar`** es la pieza de privacidad: dos regex, email y secuencia de 7+ dígitos
   (RUT/teléfono/tarjeta). Los números cortos (un año) no caen porque exigen 7+ dígitos.
2. **El hash determinista** usa `json.dumps(..., sort_keys=True)` → el mismo contenido produce
   siempre el mismo hash, sin importar el orden de inserción. Clave: **excluir `record_hash`**
   del contenido hasheado, o sería imposible recomputarlo.
3. **El hash chain:** `record_hash` incluye `prev_hash`. Por eso, editar un registro viejo
   cambia su `record_hash`, y como el siguiente guarda ese hash en su `prev_hash`, **rompe el
   enlace**. Dos defensas que `verificar_cadena` combina: recomputar el hash de cada registro
   (detecta un campo editado) y comprobar que cada `prev_hash` apunta al anterior (detecta
   reordenamiento o un eslabón faltante).
4. **`registrar`** valida primero (falla rápido con `ValueError`), redacta la entrada en
   `input_redacted` y **descarta el crudo**: el registro no debe contener PII en claro.

## Parte B — Model card (ejemplo de referencia, en inglés)

```markdown
# Model Card — Internal Docs RAG Assistant

## Intended use
Answer employee questions about internal product documentation, always citing the source
document. Read-only: it informs, it does not act.

## Out-of-scope uses
- Not for legal, medical or financial advice.
- Does not make decisions about people (hiring, credit, performance). It informs only.
- Not a source of truth without a citation: if it can't find the source, it must say "I don't know".

## Data
- Corpus: 1,200 internal KB documents, version 2026-06. Languages: ES/EN.
- Embeddings: text-embedding-3-large. No customer PII (verified during ingest).

## Evaluation
- Recall@5 = 0.86 on 120 golden questions (see eval harness, 6.9).
- Faithfulness (LLM-as-judge) = 0.91. Reported per language (ES 0.93 / EN 0.89).

## Limitations and risks
- May hallucinate if retrieval returns irrelevant chunks.
- Knowledge cutoff = corpus date; stale after new product releases until re-ingest.
- Inherits any bias present in the KB. Untested outside the product domain.

## Governance
- EU AI Act tier: limited risk (chatbot) -> Article 50 transparency applies.
- Extraterritorial scope: yes — EU employees receive the output.
- Transparency: UI shows "You are talking to an AI assistant".
- Accountable owner: Platform team.
- Audit logging: yes — structured, PII-redacted, hash-chained (see audit_log.py).
```

## Puntos resbalosos (donde el corrector debe mirar)

1. **`verificar_cadena` que solo compara `prev_hash`** sin recomputar el `record_hash`: pasa
   `test_cadena_integra` y `test_cadena_detecta_reordenamiento` pero **falla**
   `test_cadena_detecta_tamper_de_campo`. Es el error conceptual central: sin recomputar, no
   detectas la edición de un campo.
2. **Incluir `record_hash` en el contenido hasheado** → no se puede recomputar; o hace que
   nunca verifique.
3. **Guardar `input_text` crudo** en el registro (pasivo de privacidad).
4. **Hash no determinista** (dict sin `sort_keys`): la cadena "se rompe sola" al re-serializar.
5. **Model card con out-of-scope vacío** o "sin limitaciones": justo lo que protege, ausente.

## Rango de soluciones aceptables

- Otra regex de redacción es válida si redacta emails y dígitos largos sin tragarse números
  cortos. Aceptar también redactar tarjetas/IBAN si el alumno los añade.
- Otro algoritmo de hash (sha512, blake2) es válido mientras sea determinista y
  registrar/verificar coincidan.
- Es válido que `verificar_cadena([])` devuelva `True` o `False`, siempre que el alumno lo
  decida explícitamente y lo testee (es su caso borde propio).
- La model card puede describir otro sistema RAG (no el del ejemplo) mientras los out-of-scope
  y limitaciones sean **específicos y honestos**, no plantilla.
- Conectar el `request_id` con la traza de observabilidad y la evaluación con el eval harness
  es señal de `excelente`, no requisito mínimo.
