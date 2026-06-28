---
ejercicio_id: fase-7/fase-7-index
fase: fase-7
sub_unidad: "7.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio
> no tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de
> qué observar. Úsalo como vara de medir honestidad/realismo/trade-off, nunca
> como plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico de Fase 7 + decisión de capstone estrella

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier conjunto
de tres archivos que sea **honesto, concreto y con un trade-off defendible**. La
calidad se mide por proceso y por razonamiento, no por contenido específico ni
por qué capstone se elija.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar

**Prerrequisitos** (perfil cero real recién salido de F3 y F6):

| Prerrequisito | Estado | Por qué / a qué fase vuelvo |
|---|---|---|
| Idempotencia y resiliencia (`3.14`) | a medias | Entiendo backoff/timeouts, pero nunca implementé una idempotency key real; releo 3.14. |
| APIs + OAuth2 (Fase 3) | listo | Cerré el capstone F3 con auth y endpoints. |
| Agentes + evals + seguridad LLM (Fase 6) | a medias | Hice el loop ReAct y un eval de RAG, pero nunca evalué un *agente* (trayectorias); vuelvo a 6.9. |

**Las 10 sub-unidades** (cero real esperable: mayoría `nuevo`, algún `lo reconozco`):

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 7.1 n8n como arquitectura | lo reconozco | Armo flujos, pero nunca configuré error workflow ni versioné en Git. |
| 7.2 Integración + confiabilidad | nuevo | No sé qué es una DLQ ni el patrón outbox. |
| 7.3 Durable execution / Temporal | nuevo | Nunca usé Temporal ni pensé "replay determinista". |
| 7.4 De RPA a código *(opcional)* | nuevo | Profundización; lo difiero. |
| 7.5a ELT + modelado | nuevo | No sé diferenciar ELT de ETL ni modelar un star schema. |
| 7.5b dbt de verdad | nuevo | Nunca escribí un modelo ni un test de dbt. **(Prioridad.)** |
| 7.5c Un orquestador | nuevo | No conozco Dagster/Airflow. |
| 7.5d Data contracts + quality | nuevo | No sé qué frena un data contract vs un test. |
| 7.6 CDC + streaming *(opcional)* | nuevo | Profundización; lo difiero. |
| 7.7 Agentes de automatización con IA | lo reconozco | Usé un LLM para clasificar; nunca con eval gate, HITL ni techo de costo. |

> Para un perfil **oxidado-con-experiencia** (años de n8n, algún pipeline), lo
> esperable es más `lo reconozco` y quizá algún `lo sé hacer` en 7.1 —pero solo si
> lo defiende. La trampa #1 a detectar: marcar 7.1/7.2 como "lo sé hacer" cuando en
> realidad *arrastra nodos del happy path* pero nunca diseñó idempotencia, DLQ ni
> un criterio de salida; o marcar 7.7 como "lo sé hacer" por haber *usado* un LLM,
> sin haberlo *evaluado* ni *acotado* con guardrails.

### `plan-fase-7.md` — exemplar
- **Mar/Jue 20:00–20:50** (2 bloques) + **Sáb 09:30–11:30** (sesión larga, para el
  bloque de Data Engineering que necesita práctica con dbt corriendo).
- **Ritual de repaso:** cada bloque arranca con 5–10 min reescribiendo de memoria
  lo anterior; el sábado, repaso de la semana.
- **Diferir:** 7.4 (RPA) y 7.6 (CDC) → backlog, son profundización.
- **Tiempo extra explícito a 7.5a–d** (Data Engineering) por ser todo `nuevo` y el
  gap más grande, y a 7.7 (eval de agente + guardrails) por ser el corazón del
  capstone estrella.

Señal de calidad: **día/hora concretos**, ritual de repaso explícito, y una
decisión clara de qué difiere — no "estudiaré ~12 h/semana".

### `decision-capstone.md` — exemplar (cualquiera de las dos opciones es válida)
**Ejemplo A (estrella = agéntico F7, recomendación del curso bien adoptada):** "Mi
estrella será el sistema agéntico de F7. Trade-off: el RAG-sobre-docs es el 80% de
los portafolios (saturado); el agéntico end-to-end con manejo de fallas es mi
nicho menos copiado y conecta con mi experiencia de automatización. Cuesta más,
pero diferencia más, y no estoy eligiéndolo solo porque el curso lo diga: mi rol
objetivo es Automation Engineer. Igual dejo el RAG de F6 sólido como base. Los tres
gates del DoD que más me costarán: (1) eval harness de **agente** con gate de
regresión (7.7/6.9), porque nunca evalué trayectorias ni tool-call accuracy;
(2) HITL + techo de costo para acciones sensibles (7.7); (3) idempotencia + DLQ/replay
durable del lado de integración (7.2/7.3)."

**Ejemplo B (estrella = RAG F6):** igual de válido si argumenta el trade-off
honestamente (p. ej. "priorizo profundidad en recuperación/evals porque el rol que
busco es más AI Engineer puro; asumo que el RAG es más común y lo compenso con un
eval harness y un write-up de fallas serios, y dejo el agéntico de F7 como segundo
proyecto"). Lo que se evalúa es el **razonamiento**, no la opción —ni siquiera si
contradice la recomendación del curso, mientras lo defienda.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Usar vs diseñar.** El error #1 en esta fase: marcar n8n/automatización como
   "lo sé hacer" por *arrastrar nodos*. Verificación: que justifique cómo haría el
   flujo *idempotente*, qué pone en la *DLQ* y cuándo se *gradúa a Temporal*, no
   cómo conecta dos nodos.
2. **Plan irreal o sin repaso.** Bloques que no caben en su vida, o sin *spacing*.
   La fase es densa (tres mundos); un plan sin repaso no la sostiene.
3. **No diferir nada.** Tratar 7.4/7.6 como crítico infla el plan; el diseño
   correcto las marca como profundización diferible.
4. **Decisión de capstone sin trade-off.** Elegir por moda o por obediencia. La
   señal `excelente` es nombrar qué se pierde al no elegir la otra opción —incluso
   si adopta la recomendación del curso, debe defenderla con *su* caso.
5. **Subestimar el Data Engineering.** Si marcó 7.5a–d como `nuevo` pero no le da
   tiempo, contradice el peso real de la fase (es el gap más grande del roadmap).
6. **Delegar a la IA.** El ejercicio pierde sentido si un chat dictó nivel, plan o
   capstone.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables
  están y son honestos/concretos/argumentados. No exigir las tablas exactas de arriba.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se evalúa la
  calidad del proceso de autoevaluación, planificación y decisión, no el nivel de
  partida ni qué capstone se elija.
- Un plan **modesto pero sostenible** y una decisión **bien argumentada** ganan a
  uno ambicioso/irreal y a una decisión "de moda" sin trade-off. Premiar realismo
  y razonamiento.
- Adoptar la recomendación del curso (agéntico) **o** apartarse de ella (RAG) son
  ambas `excelente` si el trade-off está nombrado y aterrizado en su situación. El
  corrector no penaliza la opción; penaliza la falta de razonamiento.
- Un alumno oxidado puede marcar correctamente que ya domina 7.1: válido y
  `excelente` **si** dice cómo lo va a *validar* (resolver un ejercicio sin IA),
  no si lo salta a ciegas.
