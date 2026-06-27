# Ejercicio 6.15 — Model card + audit log a prueba de manipulación

> **Modalidad: mixta (código + documento).** Implementas en Python puro (sin red) un **audit
> log estructurado** que redacta PII y encadena registros con un **hash chain**
> (tamper-evidence), y escribes una **model card** para el RAG del capstone. Son los dos
> artefactos de gobernanza baratos que separan un demo de juguete de un sistema defendible.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.15` AI Governance / EU AI Act / Responsible AI
**Ruta:** crítica · **Timebox:** 45 min · **Modalidad:** mixto (código + diseño)

## 🎯 Objetivo

(a) **Implementar** tres funciones puras en `audit_log.py` que construyan un registro de
auditoría de decisiones de IA: redactar PII, encadenar con hash chain y verificar la
integridad de la cadena. (b) **Escribir** una model card (`MODEL-CARD.md`) para el asistente
RAG del capstone, con uso previsto, out-of-scope, datos, evaluación, limitaciones y tier de
gobernanza.

## 📋 Contexto

Para alto riesgo el EU AI Act **exige** logging automático (Art. 12); para todo lo demás, el
audit log es la base de la accountability. Y una model card documenta los **límites** de tu
sistema (lo que NO hace), que es justo lo que te protege. Ambos artefactos son entregables de
primera clase del capstone: el `request_id` del audit log enlaza con la traza de
observabilidad, y la model card conecta con los números de tu eval harness.

## 📏 Primero-Sin-IA

1. **Predice antes de codear.** En un papel, dibuja tres registros encadenados (cada uno
   guarda el hash del anterior). Ahora **edita un campo del registro del medio**: ¿qué hashes
   dejan de cuadrar? Escribe tu predicción en `prediccion.md`.
2. Implementa las tres funciones a mano, apoyándote solo en la lección y en la doc oficial de
   `hashlib`/`json`. Corre `pytest` hasta verde.
3. Escribe **tú** los out-of-scope y las limitaciones de la model card (es donde se demuestra
   criterio). No le pidas a una IA que la genere.
4. Solo al final, usa IA para *revisar* tu código y tu model card, no para generarlos.
5. Mañana, **reescribe de memoria** por qué un hash chain detecta manipulación.

## 🛠️ Instrucciones

### Parte A — Código (`audit_log.py`)

Implementa las tres funciones (no cambies sus firmas). Corre los tests:

```bash
uv run pytest        # o simplemente:  pytest
```

Contrato (lo fijan los tests de `test_audit_log.py`):

- `redactar(texto: str) -> str` — reemplaza **emails** y **secuencias largas de dígitos**
  (RUT, teléfonos, tarjetas: 7 o más dígitos, con o sin puntos/guiones) por `<REDACTADO>`.
  Los números cortos (un año como 2026) **no** se redactan.
- `registrar(evento: dict, prev_hash: str) -> dict` —
  - Lanza `ValueError` si falta algún campo de `CAMPOS_REQUERIDOS`.
  - Copia los campos requeridos.
  - Si el evento trae `input_text`, guarda su versión **redactada** en `input_redacted` y
    **NO** guarda el texto crudo en el registro.
  - Copia `confidence` y `human_in_the_loop` si vienen.
  - Añade `prev_hash` y calcula `record_hash` = hash del registro **excluyendo** `record_hash`.
- `verificar_cadena(registros: list[dict]) -> bool` — `True` si: el primer `prev_hash` es
  `GENESIS`, cada `record_hash` **recomputado** coincide con el guardado (esto detecta que
  alguien editó un campo), y cada `prev_hash` apunta al `record_hash` anterior.

Añade al menos **un test propio** en `test_audit_log.py` (mira los TODO al final del archivo).

### Parte B — Model card (`MODEL-CARD.md`)

Completa la plantilla de `MODEL-CARD.md` para el asistente RAG del capstone. **En inglés**
(convención de las model cards). Lo importante no es llenar campos: es que los **out-of-scope**
y las **limitaciones** sean honestos y específicos.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests de `test_audit_log.py` pasan en verde.
- [ ] El registro **nunca** guarda PII en claro (`input_text` crudo no aparece; queda
      `input_redacted`).
- [ ] `verificar_cadena` detecta tanto un **campo manipulado** como un **reordenamiento**.
- [ ] Existe tu `prediccion.md` (qué hashes se rompen al editar el registro del medio).
- [ ] La `MODEL-CARD.md` declara **uso previsto, out-of-scope, datos, evaluación, limitaciones
      y tier de gobernanza** (riesgo limitado → Art. 50, típicamente).
- [ ] Añadiste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué un hash chain vuelve el log a prueba de manipulación.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `redactar`, dos expresiones regulares: una para emails (`algo@dominio.tld`) y otra para
secuencias de 7+ dígitos (admitiendo `.` y `-` en medio). Para el hash determinista, serializa
el registro con `json.dumps(..., sort_keys=True)` y pásalo por `hashlib.sha256(...).hexdigest()`
— pero **excluye** `record_hash` del contenido que hasheas (si te incluyes a ti mismo, nunca
podrás recomputarlo). El truco del hash chain: `record_hash` incluye `prev_hash`, así que
editar un registro viejo cambia su hash y rompe el enlace de todos los siguientes. Revisa la
sección "audit logging" de la lección antes de mirar la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/model-card-y-audit-log/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
