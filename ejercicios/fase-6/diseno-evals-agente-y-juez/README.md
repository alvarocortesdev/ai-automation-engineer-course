# Ejercicio 6.9 — Diseño: plan de evals para un agente + un juez calibrado

> **Modalidad: diseño/razonamiento (sin código que ejecutar).** Diseñas el plan de
> evaluación de un agente que **actúa**, eliges qué medir de forma determinista y qué con un
> LLM-as-judge, y construyes un juez que no te mienta. El entregable es `diseno.md`. No hay
> tests automáticos: tu IA corrige el **razonamiento** contra la rúbrica.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.9` Eval-driven development
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Producir un plan de evals defendible para un **agente de soporte** (el de la lección 6.8):
elegir y justificar las métricas de agente, construir el golden set desde trazas de prod,
diseñar un LLM-as-judge con su rúbrica y mitigación de sesgos, y definir el gate + la
trazabilidad que lo hacen un ship-gate real.

## 📋 Contexto

El agente recibe tickets y puede: **responder dudas**, **consultar el estado de un pedido**,
**emitir un reembolso** (irreversible) y **escalar a un humano**. Hay alto volumen y tienes
**trazas de producción** disponibles (cada interacción quedó registrada con su entrada, la
trayectoria de tools y la respuesta final). Un agente que actúa sin eval gate es un incidente
con factura: este diseño es lo que lo vuelve embarcable y defendible en una entrevista.

## 📏 Primero-Sin-IA

1. Diséñalo **solo**, a mano (timebox arriba). Escribe tus decisiones y **por qué**.
2. Solo entonces, consulta documentación oficial (DeepEval métricas de agente, Langfuse
   datasets/scores, el survey de LLM-as-a-judge).
3. **Solo al final**, usa IA para *revisar y cuestionar* tu diseño — no para generarlo.
4. Mañana, **reescribe de memoria** las 4 métricas de agente y los 3 sesgos del juez.

## 🧩 Tu tarea (en `diseno.md`)

Decide y **justifica cada punto** (no "porque suena bien" — la razón concreta):

1. **Métricas del agente.** Elige y define las que vas a medir entre: **tool-call accuracy**,
   **trajectory**, **task completion**, **costo/pasos**. Para **cada una**, indica si es
   **determinista** o necesita un **LLM-as-judge**, y por qué. (Pista: la mayoría es
   determinista; reserva el juez para lo genuinamente subjetivo.)
2. **Dataset desde trazas de prod.** Explica cómo construyes el golden set a partir de las
   trazas: qué casos **promueves** al dataset y por qué los **fallidos/raros** valen más que
   los felices. Da 2 ejemplos concretos de casos que promoverías.
3. **LLM-as-judge.** Para la métrica que sí lo necesita, escribe la **rúbrica**: criterio +
   escala (p. ej. 0–1 o pass/fail) + formato de salida esperado del juez. Luego:
   - nombra **dos** sesgos del juez que aplican aquí (entre position, verbosity,
     self-enhancement) y da **una mitigación concreta** por sesgo;
   - explica cómo **validas que el juez está calibrado** (contra qué lo comparas).
4. **Gate en CI + budget.** Define el **gate de regresión** (umbral absoluto + baseline +
   tolerancia) y el **budget de costo/pasos** que bloquearían un merge. Di en qué punto del
   pipeline corre (¿en cada PR? ¿solo en los que tocan el agente?).
5. **Trazabilidad.** Explica cómo atas cada score a **prompt + modelo + versión de dataset**
   (Langfuse como single source of truth) y por qué un número sin esa cadena **no es
   comparable ni defendible**.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Cada métrica de agente viene etiquetada **determinista** o **con-juez**, con su razón.
- [ ] El golden set se construye **desde trazas de prod** (no inventado); justificas qué
      promueves con 2 ejemplos.
- [ ] La rúbrica del juez tiene **criterio + escala + formato**.
- [ ] Nombras **2 sesgos** del juez con **1 mitigación concreta** cada uno.
- [ ] Dices cómo **validas el juez** (contra labels humanos en una muestra).
- [ ] El gate distingue **umbral absoluto** de **regresión**, y hay un **budget de costo/pasos**.
- [ ] Explicas la **trazabilidad** score ↔ prompt + modelo + dataset.
- [ ] Puedes **defender cada decisión sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Tool-call accuracy, trajectory y costo/pasos son **deterministas**: comparas contra un golden
(tool + args, secuencia de pasos) o sumas tokens/pasos — no necesitas un juez. Task completion
abierta ("¿resolvió la duda del cliente?") es lo que típicamente pide un **LLM-as-judge**. Los
casos más valiosos del golden set son los que **fallaron** o los **raros** (un reembolso mal
emitido enseña más que diez "¿cuál es mi pedido?" exitosos). Y recuerda: el juez **también** es
un sistema a evaluar — valídalo contra una muestra etiquetada por humanos antes de confiar en su
número.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu `diseno.md`, la **rúbrica**
(`.ai/rubricas/fase-6/diseno-evals-agente-y-juez.md`) y `.ai/INSTRUCCIONES-CORRECTOR.md`:

> "Corrige `ejercicios/fase-6/diseno-evals-agente-y-juez/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
