# Ejercicio 7.7 — El plano de control de un agente que actúa

> **Modalidad: código (Primero-Sin-IA, timebox 45 min).** Construyes la capa
> determinista que vuelve seguro a un agente que ejecuta acciones reales. El
> "cerebro" (LLM) ya propuso; tú escribes el código que **dispone**. Sin red, sin
> llamadas a ningún proveedor: la propuesta del cerebro llega como un dict que tú
> controlas (igual que mockear respuestas de LLM, ver 2.11).

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.7` Agentes de automatización con IA
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar el **plano de control** de un agente: dada la propuesta del LLM (categoría, validez, confianza), la acción propuesta y el estado del run (costo acumulado, inputs ya procesados), decidir la **ruta** —`AUTO`, `HITL`, `RECHAZO` o `DUPLICADO`— aplicando, **en orden**, idempotencia, guardrail de I/O (OWASP LLM05), techo de costo, HITL obligatorio para acciones sensibles (OWASP LLM06) y umbral de confianza.

## 📋 Contexto

Es el punto 6 del Definition of Done del [capstone de la fase](/fase-7-automatizacion/proyecto/) hecho código: validación de salida + least-privilege + HITL para acciones sensibles + techo de costo. El **orden** de los chequeos es el diseño de seguridad: la primera barrera que aplica decide la ruta.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la documentación oficial (OWASP LLM Top 10).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe de memoria** los cinco chequeos en orden. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `plano_control.py` e implementa `decidir(...)` (no cambies su firma). El contrato y el orden exacto de los chequeos están en el docstring.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**. Presta atención a los tests de **orden**: verifican que la primera barrera gana (un duplicado con schema inválido es `DUPLICADO`, no `RECHAZO`).
4. Añade al menos **un test propio** en `test_plano_control.py` (sugerencia en el `TODO` al final del archivo).
5. Escribe `write-up.md` respondiendo:
   - (a) ¿Por qué una acción sensible va a HITL **aunque** el modelo reporte confianza 0.99? Nombra el riesgo OWASP y por qué la confianza auto-reportada no basta.
   - (b) ¿Por qué la idempotencia va **primero**, antes que el guardrail de schema?
   - (c) ¿Qué garantiza validar la salida contra el schema y qué **no** garantiza? Da un ejemplo de salida válida vs schema pero incorrecta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest` pasa en verde, incluidas las pruebas de orden.
- [ ] Una acción sensible con confianza 0.99 devuelve `HITL`, no `AUTO`.
- [ ] El techo de costo se aplica de verdad (no es un parámetro muerto).
- [ ] Un duplicado con schema inválido devuelve `DUPLICADO` (idempotencia primero).
- [ ] Agregaste al menos un test propio.
- [ ] El `write-up.md` distingue **validar el schema** de **confiar en el contenido** y nombra LLM05/LLM06.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Es una cadena de `if` con `return` temprano, en el orden exacto del contrato:
idempotencia → schema → costo → sensible → confianza. Cada `return` corta el
flujo, así que la primera barrera que aplica decide. No combines condiciones en
un solo `if` con `and`: separa cada barrera para que el `motivo` que devuelves
identifique exactamente qué la frenó. Cuidado con la frontera de la confianza:
`confianza < umbral` es HITL; `confianza == umbral` es AUTO. Revisa la sección 4.4
de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, con `write-up.md`),
- la **rúbrica**: `.ai/rubricas/fase-7/plano-control-agente.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/plano-control-agente.md` — no la mires antes de intentarlo de verdad. El corrector revisará tu **razonamiento** (el orden de los chequeos y el write-up), no solo el verde de los tests.
