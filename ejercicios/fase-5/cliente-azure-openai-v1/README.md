# cliente-azure-openai-v1 — Escribe el cliente v1 de Azure OpenAI

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.6` Azure profundización
**Ruta:** opcional / profundización · **Timebox:** 25–35 min · **Modalidad:** código

## 🎯 Objetivo

Implementar, a mano y sin IA, el cliente **vigente en 2026** para llamar a un modelo en
**Azure OpenAI Service** con la **API v1 GA**: cliente `OpenAI()` (no `AzureOpenAI()`),
`base_url` con `/openai/v1/`, config desde el entorno, y `model=` apuntando al **deployment**.

## 📋 Contexto

Casi todos los tutoriales de Azure OpenAI que encontrarás están escritos para la API vieja
(`AzureOpenAI()` + `api_version`). Este ejercicio te fija la forma correcta de 2026, que es la que
usarás cuando despliegues el RAG del capstone sobre Azure. Practicas además dos hábitos que ya son
columna del curso: **config en el entorno** (12-factor, [5.2](/fase-5-devops/5-2-12-factor/)) y
**cero secretos hardcodeados** ([5.4](/fase-5-devops/5-4-seguridad-supply-chain-ci/)).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta la **documentación oficial** (la API v1: ver Recursos de la lección).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa `build_client()` y `responder(...)` (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # o:  pytest
   ```

3. Itera hasta el **verde**. Los tests no llaman a la red: verifican la **forma** del cliente
   (API v1, sin `api_version`, sin secretos hardcodeados) y que `responder` use `model=deployment`.
4. Añade **un test propio** (idea en el `TODO` del final de `test_solucion.py`).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] Usas `OpenAI()` (no `AzureOpenAI`), `base_url` con `/openai/v1/`, y **sin** `api_version`.
- [ ] Endpoint y clave salen de `AZURE_OPENAI_ENDPOINT` / `AZURE_OPENAI_API_KEY` (nada hardcodeado).
- [ ] `responder` usa `model=deployment` y devuelve `choices[0].message.content`.
- [ ] Agregaste un test propio.
- [ ] Puedes **explicar sin notas**: ¿por qué `model=` es el deployment y no el modelo base? ¿Qué
      cambió respecto al viejo `AzureOpenAI()`?

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`base_url` = endpoint **+** `/openai/v1/`. Cuida la barra: si el endpoint ya termina en `/`,
un `.rstrip("/")` antes de concatenar evita la `//` duplicada. El endpoint y la clave salen de
`os.environ[...]`. En `responder`, la firma ya te da `deployment`: pásalo tal cual a `model=`.
Mira la sección 4.3 de la lección antes de la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/cliente-azure-openai-v1.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/cliente-azure-openai-v1.md` — no la
mires antes de intentarlo de verdad.
