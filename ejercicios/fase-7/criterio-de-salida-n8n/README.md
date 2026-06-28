# criterio-de-salida-n8n — ¿n8n, código o Temporal?

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.1` n8n: de tool a arquitectura
**Ruta:** crítica · **Timebox:** 35–40 min · **Modalidad:** razonamiento / diseño (a mano)

## 🎯 Objetivo

Aplicar un **criterio de salida** defendible: ante cuatro casos concretos, decidir
si la automatización **se queda en n8n** o se **gradúa** a código o a durable
execution (Temporal), justificando con la **restricción dominante** y no con gusto
personal. Documentar la decisión de graduar en un **ADR**.

## 📋 Contexto

La señal de seniority no es "todo lo resuelvo con mi herramienta favorita", sino
"elijo por la restricción y reconozco cuándo la herramienta actual ya no rinde".
Este ejercicio entrena ese juicio, que decide la **arquitectura del Capstone F7**:
qué partes viven en n8n (orquestación visible) y cuáles se gradúan a código o a
[Temporal (7.3)](/fase-7-automatizacion/7-3-durable-execution-temporal/).

## 📏 Primero-Sin-IA

1. Decide **solo**, a mano (timebox arriba). El objetivo es tu razonamiento, no
   "la respuesta correcta" (no hay una única).
2. Solo entonces, consulta documentación oficial si la necesitas.
3. **Solo al final**, usa IA para *cuestionar* tu razonamiento — no para que decida
   por ti.
4. Mañana, aplica el criterio a un caso **nuevo** de memoria.

## 🧩 Los cuatro escenarios

1. **Bienvenida a leads.** Cada vez que entra un lead en una planilla, mandar un
   correo de bienvenida y registrar la fila en un CRM. Pocos pasos, lineal, ~30
   eventos al día. Lo mantiene el equipo de marketing (no son developers).
2. **Motor de pricing.** Por cada orden, aplicar ~12 reglas de descuento anidadas
   que **cambian seguido**, con casos borde delicados que exigen **tests unitarios
   serios** y code review. Lo mantiene un equipo de developers; miles de órdenes
   por hora.
3. **Onboarding de proveedor.** Enviar un contrato, **esperar la firma** del
   proveedor (puede tardar 7 días), luego **esperar la aprobación** de finanzas
   (otros días), y recién entonces dar de alta y hacer un **cobro inicial**. Si el
   servidor se reinicia a mitad de proceso, debe **reanudar exactamente donde
   quedó**, y cada paso (el cobro) debe ejecutarse **exactamente una vez**.
4. **Triage de documentos con IA.** Llega un correo con un PDF; un modelo
   **extrae y clasifica** los datos; según el resultado, se dispara **uno de tres**
   flujos internos. La orquestación (recibir → decidir ruta → disparar) es simple y
   conviene que **operaciones la vea y la ajuste**; pero la extracción con IA
   necesita **evals** y lógica **testeable**.

## 🛠️ Instrucciones

Edita `decision.md` (tiene la plantilla):

1. **Tabla de decisión** con los 4 escenarios. Por fila: tu **elección**
   (`n8n` · `código` · `Temporal` · `híbrido`), la **restricción dominante** que la
   determina, y **una señal concreta** que te haría cambiar de opinión.
2. **Un ADR** para el escenario que elijas **graduar de n8n a otra cosa**: contexto,
   decisión, alternativas consideradas y el **trade-off** que aceptas (qué ganas y
   qué pierdes). Formato de ADR como en
   [`2.13`](/fase-2-ingenieria/2-13-colaboracion-spec-driven-adrs/).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las 4 filas tienen una elección **justificada por una restricción**, no por gusto.
- [ ] Al menos un escenario nombra el **límite real del low-code** que obliga a graduar.
- [ ] El escenario con **estado durable / esperas largas / reanudar exacto** se
      asigna a **Temporal**, no a n8n ni a un script suelto.
- [ ] El escenario de IA reconoce el **patrón híbrido** (n8n delgado que dispara un
      servicio en código), no "todo n8n" ni "todo código".
- [ ] El ADR nombra un trade-off **honesto**: graduar también cuesta (menos
      visibilidad para ops, más infra que operar).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La pregunta guía es "¿cuál es la **restricción dominante**?", no "¿cuál me gusta?".
Lineal + lo mantiene ops + baja frecuencia → n8n. Lógica compleja + tests + equipo
de devs + volumen → código. Esperas de días + reanudar exactamente tras un crash +
cada paso exactamente una vez → ése "reanudar exacto" es la **firma** de durable
execution (Temporal, 7.3). El escenario de IA es una **trampa**: ni todo n8n ni
todo código; piensa en n8n como orquestador delgado que llama a un servicio
testeable para la extracción. Cuidado con el sesgo "código siempre es mejor": a
veces n8n gana justamente porque un no-dev debe poder mantenerlo. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu solución (este directorio, con tu `decision.md`),
- la **rúbrica**: `.ai/rubricas/fase-7/criterio-de-salida-n8n.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/criterio-de-salida-n8n.md`
— no la mires antes de intentarlo de verdad. Se evalúa que tu razonamiento sea
**defendible**, no que "aciertes".
