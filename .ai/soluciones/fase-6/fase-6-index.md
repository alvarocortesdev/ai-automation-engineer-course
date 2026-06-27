---
ejercicio_id: fase-6/fase-6-index
fase: fase-6
sub_unidad: "6.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio
> no tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de
> qué observar. Úsalo como vara de medir honestidad/realismo/trade-off, nunca
> como plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico de Fase 6 + decisión de capstone

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier conjunto
de tres archivos que sea **honesto, concreto y con un trade-off defendible**. La
calidad se mide por proceso y por razonamiento, no por contenido específico ni
por qué capstone se elija.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar

**Prerrequisitos** (perfil cero real recién salido de F1–F5):

| Prerrequisito | Estado | Por qué / a qué fase vuelvo |
|---|---|---|
| Python + pydantic | listo | Cerré F1 con pydantic y type hints. |
| Backend FastAPI | a medias | Hice el capstone F3 pero no recuerdo dependencias/async; releo 3.8. |
| UI con streaming | a medias | Vi streaming en F4 pero no lo monté solo; valido con un ejercicio. |
| Deploy + observabilidad | me falta | No instrumenté trazas; vuelvo a 5.10 antes del capstone. |

**Las 18 sub-unidades** (cero real esperable: mayoría `nuevo`, algún `lo reconozco`):

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 6.0 Matemática mínima | lo reconozco | Sé qué es un vector, no calculo coseno a mano. |
| 6.0b Puente ML/DL | nuevo | No sé explicar attention. |
| 6.1 Fundamentos LLMs | lo reconozco | Uso LLMs, no domino sampling. |
| 6.2 Prompt & Context | lo reconozco | Escribo prompts; nunca gestioné token budget. |
| 6.3 APIs de LLM | lo reconozco | Llamé APIs; no manejé rate limits/reintentos. |
| 6.4 Structured + tools + MCP | nuevo | Nunca validé salidas ni levanté un MCP. |
| 6.5 Embeddings | nuevo | No diseñé chunking. |
| 6.6 Vector DBs | nuevo | No elegí una vector DB con criterio. |
| 6.7 RAG a fondo | lo reconozco | Usé RAG; no sé diagnosticar recall bajo. |
| 6.8 AI Agents | nuevo | Nunca escribí el loop ReAct a mano. |
| 6.9 Eval-driven | nuevo | Nunca monté un eval harness. **(Prioridad.)** |
| 6.10 Open-source/serving | nuevo | No conozco vLLM/batching. |
| 6.11 Multimodal | nuevo | Solo texto hasta ahora. |
| 6.12 Voice realtime | nuevo | Profundización; lo difiero. |
| 6.13 Fine-tuning | nuevo | Profundización; lo difiero. |
| 6.14 Seguridad LLM | nuevo | No conozco OWASP LLM. |
| 6.15 AI Governance | nuevo | No conozco EU AI Act. |
| 6.16 Costo/latencia LLMOps | nuevo | Nunca medí USD/request. |

> Para un perfil **oxidado-con-experiencia** (hizo RAG en Azure, agentes en n8n),
> lo esperable es más `lo reconozco` y quizá algún `lo sé hacer` — pero solo si lo
> defiende. La trampa #1 a detectar: marcar 6.7/6.9 como "lo sé hacer" cuando en
> realidad *usó* RAG pero no sabe *diagnosticarlo* ni *evaluarlo* con un harness.

### `plan-fase-6.md` — exemplar
- **Mar/Jue 20:00–20:50** (2 bloques) + **Sáb 09:30–11:30** (sesión larga).
- **Ritual de repaso:** cada bloque arranca con 5–10 min reescribiendo de memoria
  lo anterior; el sábado, repaso de la semana.
- **Diferir:** 6.12 (voz) y 6.13 (fine-tuning) → backlog, son profundización.
- **Tiempo extra explícito a 6.9** (eval-driven) por ser `nuevo` y el de mayor
  retorno de la fase; segundo foco a 6.7 (RAG) y 6.14 (seguridad).

Señal de calidad: **día/hora concretos**, ritual de repaso explícito, y una
decisión clara de qué difiere — no "estudiaré ~12 h/semana".

### `decision-capstone.md` — exemplar (cualquiera de las dos opciones es válida)
**Ejemplo A (estrella = agéntico F7):** "Mi estrella será el sistema agéntico de
F7. Trade-off: el RAG-sobre-docs es el 80% de los portafolios (saturado); el
agéntico end-to-end con manejo de fallas es mi nicho menos copiado y conecta con
mi experiencia de automatización. Cuesta más, pero diferencia más. Igual hago el
RAG de F6 sólido como base. Los tres gates del DoD que más me costarán: (1) eval
harness de **agente** con gate de regresión (6.9), porque nunca evalué
trayectorias; (2) techo de costo + HITL para acciones sensibles (6.16/6.14);
(3) idempotencia/DLQ del lado de automatización (F7)."

**Ejemplo B (estrella = RAG F6):** igual de válido si argumenta el trade-off
honestamente (p. ej. "priorizo profundidad en recuperación/evals porque es el
core del rol que busco; asumo que es más común y lo compenso con un eval harness
y un write-up de fallas serios"). Lo que se evalúa es el **razonamiento**, no la
opción.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Usar vs entender.** El error #1 en esta fase: marcar RAG/agentes/evals como
   "lo sé hacer" por haberlos *usado* con IA o low-code. Verificación: que
   justifique cómo *diagnosticaría* un recall bajo o cómo *montaría* un eval
   harness, no cómo *invoca* uno.
2. **Plan irreal o sin repaso.** Bloques que no caben en su vida, o sin *spacing*.
   La fase es larga; un plan sin repaso no sostiene 18 sub-unidades.
3. **No diferir nada.** Tratar 6.12/6.13 como crítico infla el plan; el diseño
   correcto las marca como profundización diferible.
4. **Decisión de capstone sin trade-off.** Elegir por moda. La señal `excelente`
   es nombrar qué se pierde al no elegir la otra opción.
5. **Subestimar 6.9.** Si lo marcó `nuevo` pero no le da tiempo extra, contradice
   la tesis de la fase (eval-driven = diferenciador).
6. **Delegar a la IA.** El ejercicio pierde sentido si un chat dictó nivel, plan
   o capstone.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables
  están y son honestos/concretos/argumentados. No exigir las tablas exactas de arriba.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se evalúa la
  calidad del proceso de autoevaluación, planificación y decisión, no el nivel de
  partida ni qué capstone se elija.
- Un plan **modesto pero sostenible** y una decisión **bien argumentada** ganan a
  uno ambicioso/irreal y a una decisión "de moda" sin trade-off. Premiar realismo
  y razonamiento.
- Un alumno oxidado puede marcar correctamente que ya domina varias sub-unidades:
  válido y `excelente` **si** dice cómo lo va a *validar* (resolver un ejercicio
  sin IA), no si las salta a ciegas.
