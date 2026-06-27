# Ejercicio 6.8 — Diseño: sistema agéntico con patrón, framework y HITL

> **Modalidad: razonamiento/diseño (sin código que ejecutar, sin IA para resolver).**
> Diseñar un sistema agéntico es decidir bajo restricciones, no juntar herramientas. Aquí
> eliges patrón, framework y guardrails **por la restricción dominante** y justificas cada
> decisión. La salida es un `diseno.md` que un equipo podría leer y discutir.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.8` AI Agents desde cero
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Diseñar un agente de soporte y **defender** sus decisiones de arquitectura: patrón
multi-agente (o single-agent), framework, ubicación de los human-in-the-loop, techo de
costo, memoria, y los riesgos de seguridad OWASP que aplican. Cada decisión, atada a una
**restricción dominante**, no a una preferencia.

## 📋 Contexto

El capstone estrella del portafolio (Fase 7) es un agente que **actúa**. Antes de
construirlo, un semi-senior debe poder **defender el diseño en una entrevista**: por qué
ese patrón y no otro, qué pierde con el framework elegido, dónde va el HITL y por qué. Este
ejercicio entrena exactamente ese músculo. No hay código que ejecutar — hay decisiones que
justificar.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Escribe tus decisiones aunque dudes.
2. Solo entonces, consulta documentación oficial (Building effective agents de Anthropic,
   OWASP LLM Top 10).
3. **Solo al final**, usa IA para *revisar y cuestionar* tus decisiones — no para *generarlas*.
4. Mañana, **reescribe el diseño de memoria**. Si no puedes defenderlo, no lo entendiste.

## 🛠️ El escenario

Una tienda recibe **tickets de soporte** de clientes. Un agente debe procesarlos. El agente
puede, según el ticket:

| Acción | Qué hace | Reversibilidad |
|---|---|---|
| `responder` | Contesta una duda en lenguaje natural | reversible |
| `consultar_pedido` | Lee el estado de un pedido (solo lectura) | reversible |
| `buscar_kb` | Busca en la base de conocimiento interna (RAG) | reversible |
| `emitir_reembolso` | Devuelve plata al cliente | **irreversible** |
| `escalar_a_humano` | Deriva el ticket a un agente humano externo | semi-irreversible |

Hay **volumen alto** (muchos tickets), algunos requieren buscar en la base de conocimiento,
y la base de clientes vuelve: el mismo cliente abre varios tickets a lo largo del tiempo.

## 🧩 Qué responder (en `diseno.md`)

1. **Patrón.** ¿single-agent, orchestrator-worker, supervisor o handoffs? Da la
   **restricción dominante** que decide (no "porque suena bien"). Si eliges multi-agente,
   justifica por qué un single-agent no alcanza.
2. **Framework.** Elige uno de los cinco de la lección (LangGraph, Pydantic AI, OpenAI
   Agents SDK, Claude Agent SDK, CrewAI). Di **qué restricción** te hace elegirlo y nombra
   explícitamente **qué pierdes** con esa elección.
3. **HITL.** Marca qué acción(es) exigen confirmación humana y por qué (reversibilidad /
   blast radius). Marca cuáles van automáticas. Justifica el caso del reembolso.
4. **Techo de costo.** Dónde pones el techo de pasos y por qué; qué pasa cuando se alcanza.
5. **Memoria.** Qué guardas en **corto plazo** (run del ticket actual) y qué en **largo
   plazo** (entre tickets del mismo cliente). Da un ejemplo concreto de cada uno.
6. **Seguridad.** Nombra **tres** riesgos del OWASP LLM/Agentic que aplican a este escenario
   (p. ej. Excessive Agency LLM06, Improper Output Handling LLM05, prompt injection LLM01
   vía el texto del ticket) con **una mitigación concreta por riesgo**.

## 📦 Qué entregar (deja este archivo en esta carpeta)

- `diseno.md` — las 6 decisiones de arriba, cada una con su justificación por restricción.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El patrón elegido viene con una **restricción dominante** explícita, no con un gusto.
- [ ] El framework se justifica por restricción y nombras qué **pierdes**.
- [ ] `emitir_reembolso` (irreversible) está marcado como **HITL**; al menos una acción
      reversible va automática.
- [ ] El techo de costo tiene una ubicación y un comportamiento de corte definidos.
- [ ] Distingues memoria de corto plazo de largo plazo con un ejemplo concreto de cada una.
- [ ] Tres riesgos OWASP **distintos**, cada uno con una mitigación accionable y específica
      a este escenario (no genérica).
- [ ] Puedes **defender cada decisión sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/diseno-multiagente-hitl/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Hay más de un diseño correcto: lo que se evalúa es la
**justificación**, no que coincidas con la referencia.)
