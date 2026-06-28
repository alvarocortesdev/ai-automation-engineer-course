---
ejercicio_id: fase-8/fase-8-index
fase: fase-8
sub_unidad: "8.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio no
> tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de qué
> observar. Úsalo como vara de medir honestidad/realismo/calidad-del-contrato, nunca
> como plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico de Fase 8 + contrato de método de diseño

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier conjunto de
tres archivos que sea **honesto, concreto y con un método de diseño bien
argumentado**. La calidad se mide por proceso y razonamiento, no por contenido
específico ni por qué nivel se declare.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar

**Prerrequisitos** (perfil cero real recién salido de F6/F7):

| Prerrequisito | Estado | Por qué / a qué fase vuelvo |
|---|---|---|
| Arquitectura *light* / ports & adapters (`3.9`) | a medias | Separé dominio de infra en el capstone F3, pero no tengo claro cómo crece "a escala"; releo 3.9 antes de 8.2. |
| Bases de datos a fondo (Fase 3) | listo | Cerré 3.3 con transacciones, índices y N+1. |
| Sistemas de IA: RAG, agentes, evals (Fase 6) | listo | Construí el RAG del capstone F6 con eval harness. |
| Automatización e integración (Fase 7) | a medias | Hice el agéntico de F7 pero la parte de integración distribuida (event-driven) la siento floja; refresco 7.2. |

**Las 5 sub-unidades** (cero real esperable: mayoría `nuevo`/`lo reconozco`):

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 8.1 Fundamentos de system design | nuevo | Nunca estimé capacidad ni razoné CAP fuera de la teoría. |
| 8.2 Arquitectura de apps + DDD táctico | lo reconozco | Sé qué es una entidad, pero nunca modelé un aggregate ni un ACL de verdad. |
| 8.3 Monolito vs microservicios *(opcional)* | lo reconozco | Tengo la intuición; lo difiero, es profundización. |
| 8.4 Comunicación entre servicios *(opcional)* | nuevo | Sé de colas por F7, pero Kafka (topics/offsets) es nuevo; lo difiero. |
| 8.5 Arquitectura de sistemas de IA a escala | lo reconozco | Construí un RAG pequeño; nunca pensé caching semántico ni ruteo multi-modelo. **(Prioridad — mi especialización.)** |

> Para un perfil **oxidado-con-experiencia** (años diseñando sistemas), lo esperable
> es más `lo reconozco` y quizá algún `lo sé diseñar` en 8.1/8.3 —pero solo si lo
> defiende. La trampa #1 a detectar: marcar "lo sé diseñar" por haber *dibujado*
> arquitecturas en el trabajo, sin haber **defendido un trade-off con números** ni
> escrito un ADR. La pregunta de control: "¿dirigirías una pizarra de 40 min sobre
> esto, sin notas?".

### `plan-fase-8.md` — exemplar
- **Mar/Jue 20:00–20:50** (2 bloques) + **Sáb 10:00–12:00** (sesión larga, para el
  ejercicio de cierre que pide 3 diseños completos).
- **Ritual de repaso:** cada bloque arranca con 5–10 min reescribiendo de memoria el
  diagrama o el ADR de la sesión anterior; el sábado, repaso de la semana.
- **Diferir:** 8.3 (monolito vs micro) y 8.4 (comunicación) → backlog, son
  profundización / vocabulario de entrevista. Anota que volverá a ellas si el rol
  objetivo es backend distribuido.
- **Tiempo extra explícito a 8.5** (su especialización, todo `nuevo`/`lo reconozco`)
  y al ejercicio de cierre por ser largo (3 sistemas con Mermaid + ADRs).

Señal de calidad: **día/hora concretos**, ritual de repaso explícito y decisión clara
de qué difiere — no "estudiaré ~10 h/semana".

### `contrato-metodo.md` — exemplar
**Por qué ADRs + diagramas (ejemplo):** "Me comprometo a que cada decisión de
arquitectura sea un ADR (contexto → opciones → decisión → consecuencias) y cada
sistema un diagrama Mermaid. Un diagrama sin ADR es decoración porque muestra *qué*
construí pero no *por qué* —y en la entrevista lo que se evalúa es el porqué. El ADR
es lo que me deja defender la decisión seis meses después, cuando ya olvidé el
contexto."

**Los 3 sistemas, pre-clasificados (ejemplo):**

| Sistema | Dificultad anticipada | Restricción dominante |
|---|---|---|
| RAG multi-tenant | más difícil | **Aislamiento de datos entre tenants** (que el tenant A nunca recupere un chunk del tenant B): toca seguridad, particionado y filtrado por metadata a la vez. |
| Automatización de tickets con IA | media | **Latencia/costo del agente vs. acciones seguras** (eval gate + HITL + techo de costo sin que el flujo se vuelva lento o caro). |
| Pipeline de datos para IA | menos difícil | **Frescura del dato** (cada cuánto re-embeddear; throughput de ingesta) — me apoyo en lo de F7. |

> Cualquier orden de dificultad es válido si las **restricciones dominantes** son
> específicas y plausibles. Lo que se penaliza es "que escale bien" para los tres.

**Triángulo latencia/costo/calidad (ejemplo propio):** "Para el RAG multi-tenant,
elegir un modelo grande (GPT/Claude de gama alta) sube la **calidad** de las
respuestas pero también el **costo** por request y la **latencia**. Mi decisión:
ruteo multi-modelo —un modelo barato y rápido para consultas simples, escalar al caro
solo cuando el retrieval trae poca confianza— más caching semántico para no pagar dos
veces la misma pregunta. Subo calidad donde importa sin reventar el budget de latencia.
Eso es navegar el triángulo: no maximizar las tres, sino elegir cuál sacrifico y
dónde."

## Puntos resbalosos (donde el corrector debe mirar)
1. **Dibujar vs diseñar.** El error #1 de la fase: marcar system design como "lo sé
   diseñar" por haber hecho diagramas. Verificación: que pueda defender un trade-off
   con una estimación o un número, no solo describir cajas.
2. **Diseñar de más.** Si el contrato presume de microservicios/Kafka como señal de
   nivel, es la misconception que la fase ataca: la complejidad se justifica con una
   restricción real, no se exhibe.
3. **Plan irreal o sin repaso.** Bloques que no caben en su vida, o sin *spacing*. La
   fase es de razonamiento; sin repaso, los diagramas/ADRs no se sedimentan.
4. **No diferir nada.** Tratar 8.3/8.4 como crítico infla el plan; el diseño correcto
   las marca como profundización diferible.
5. **Triángulo sin ejemplo propio.** Recitar "latencia/costo/calidad" sin una decisión
   concreta donde una arista compita con otra → `en-progreso`, no `competente`.
6. **Restricciones dominantes genéricas.** "Que sea escalable" para los tres sistemas
   en vez de algo específico (aislamiento multi-tenant, latencia del agente, frescura).
7. **Delegar a la IA.** El ejercicio pierde sentido si un chat dictó nivel, plan,
   triángulo o clasificación.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables están y
  son honestos/concretos/argumentados. No exigir las tablas exactas de arriba.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se evalúa la calidad
  del proceso de autoevaluación, planificación y compromiso de método, no el nivel de
  partida.
- Un plan **modesto pero sostenible** y un contrato con **un ejemplo propio del
  triángulo** ganan a uno ambicioso/irreal y a uno que recita teoría. Premiar realismo
  y razonamiento.
- Cualquier orden de dificultad de los 3 sistemas es válido **si** las restricciones
  dominantes son específicas; el corrector no penaliza el orden, penaliza la
  vaguedad.
- Un alumno oxidado puede marcar correctamente que domina 8.1: válido y `excelente`
  **si** dice cómo lo va a *validar* (resolver el ejercicio de estimación sin IA), no
  si lo salta a ciegas.
