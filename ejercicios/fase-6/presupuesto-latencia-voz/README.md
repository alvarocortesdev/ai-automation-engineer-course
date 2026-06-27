# Ejercicio 6.12 — El cerebro de un voice agent: latencia percibida + barge-in

> **Modalidad: mixto (predicción a mano + código).** No hay audio, API ni API key: las
> latencias medidas y el estado se **inyectan** como datos para que pruebes la **lógica de
> decisión** de forma determinista. Es el razonamiento de un voice agent destilado a
> funciones puras.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.12` Voice/multimodal realtime
**Ruta:** opcional/profundización · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Implementar `latencia_percibida`: sumar **solo** las etapas que cuentan para el
  time-to-first-audio, entendiendo por qué el streaming saca de la cuenta a `llm_total` y
  `tts_total`.
- **O2** — Implementar `decidir_barge_in`: la **tabla de verdad** de los cuatro estados del
  cruce (agente hablando × voz del usuario).
- **O3** — Combinar ambas en `evaluar_turno`, reusándolas (no duplicar lógica).

## 📋 Contexto

La diferencia entre un voice agent que suena humano y uno que suena robot casi nunca es el
modelo: es la **latencia** y el **barge-in**. Aquí implementas el cálculo del presupuesto de
latencia y la decisión de interrumpir — el patrón que documentas en un ADR del capstone si le
pones voz, y la base de "validar/decidir antes de actuar" del agente de la Fase 7.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta documentación oficial.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. **Predice primero (a mano).** En `prediccion.md`, para estos 3 casos, escribe qué crees
   que devuelve cada función **antes** de ejecutar nada:
   - **Caso A (cumple):** `etapas = {"vad_endpoint": 100, "stt": 100, "red": 50}`, target
     250 ms, agente callado, usuario habla. ¿`latencia_ms`? ¿`cumple`? ¿`accion`?
   - **Caso B (no cumple):** `etapas = {"vad_endpoint": 120, "stt": 80, "llm_ttft": 180,
     "tts_primer_audio": 90, "red": 40, "llm_total": 900, "tts_total": 1500}`, target 250 ms,
     agente habla, usuario habla encima. ¿`latencia_ms` (ojo con qué sumas)? ¿`cumple`?
     ¿`accion`?
   - **Caso C (barge-in puro):** sin importar la latencia, ¿qué devuelve
     `decidir_barge_in(agente_hablando=True, voz_usuario_detectada=False)`?
2. **Implementa.** Abre `voz.py` y completa `latencia_percibida`, `decidir_barge_in` y
   `evaluar_turno` (no cambies las firmas). `evaluar_turno` **reusa** las otras dos.
3. **Corre los tests** hasta verde:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. Añade **un caso de prueba tuyo** en `test_voz.py` (idea: un stack S2S de una sola etapa
   que sí cumple el sub-250).
5. **Reflexiona.** En `verificacion.md` (3-4 frases): por qué `latencia_percibida` ignora
   `llm_total`/`tts_total` (el rol del streaming), y por qué cancelar el trabajo en vuelo en
   un barge-in importa para el **costo** (USD/min), no solo para la experiencia.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe **antes** de ejecutar, con las 3 predicciones + su razón.
- [ ] Todos los tests pasan (`pytest`).
- [ ] `latencia_percibida` suma **solo** las etapas del primer audio e **ignora**
      `llm_total`, `tts_total` y claves desconocidas; una etapa ausente cuenta como 0.
- [ ] `decidir_barge_in` cubre los **cuatro** casos del cruce con respuestas distintas.
- [ ] `evaluar_turno` **reusa** `latencia_percibida` y `decidir_barge_in` (no duplica lógica).
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` conecta el streaming con la latencia percibida y el barge-in con el costo.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`latencia_percibida` no debe sumar todo el dict: recorre `ETAPAS_PERCIBIDAS` y suma
`etapas.get(clave, 0)` para cada una — así ignoras `llm_total`, `tts_total` y lo desconocido,
y una clave ausente vale 0 sin reventar. `decidir_barge_in` es un cruce de dos booleanos:
cuatro combinaciones, cuatro respuestas; "interrumpir" es solo cuando **ambos** son
verdaderos. `evaluar_turno` no recalcula nada: llama a las otras dos y arma el dict
`{"latencia_ms", "cumple", "accion"}`; `cumple` usa `<=` contra el target.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/presupuesto-latencia-voz/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/presupuesto-latencia-voz.md` —
no la mires antes de intentarlo de verdad.
