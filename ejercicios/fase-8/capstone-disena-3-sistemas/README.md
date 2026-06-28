# Capstone Fase 8 — Diseña 3 sistemas en papel

> **Modalidad: a mano (diseño + razonamiento, sin código).** Este capstone es el ensayo directo de la
> ronda de **system design** de entrevistas. No construyes nada: produces tres documentos de diseño que
> podrías defender frente a un entrevistador senior en 40 minutos cada uno. La vara no es "¿mi diagrama
> es el correcto?" (hay varios defendibles), sino "¿cada decisión tiene un número o un trade-off detrás,
> y aguanta una repregunta?".

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.P` Ejercicio Fase 8 — Diseña 3 sistemas en papel
**Ruta:** crítica · **Timebox:** ~45 min de diseño Primero-Sin-IA por sistema (135 min en total) + pulido

## 🎯 Objetivo

- **O1** — Diseñar **en papel** tres sistemas de IA/datos a escala, cada uno con requisitos, un diagrama
  Mermaid que renderiza, y las decisiones de arquitectura que el sistema exige.
- **O2** — Defender cada decisión clave con un **número** (costo/hora, aprobaciones HITL/día, ventana de
  frescura) o un **trade-off explícito** que nombre qué sacrificas y la alternativa descartada.
- **O3** — Registrar las decisiones más jugosas como **ADRs** (Contexto / Decisión / Consecuencias) y
  comunicar los tres diseños de forma defendible en voz alta, sin notas.

## 📋 Contexto

Esta es la pieza que entrena la ronda que separa semi-senior de senior (y la banda salarial remota-USD).
Los tres sistemas son **tu nicho exacto**: RAG multi-tenant, automatización agéntica y pipeline de datos
para IA. El sistema 1 ya lo diseñaste en el ejercicio de
[8.5](/fase-8-system-design/8-5-arquitectura-ia-escala/) (aquí lo pules); el 2 lo viste como método en
[7.7](/fase-7-automatizacion/7-7-agentes-automatizacion-ia/); el 3 es el más nuevo. Lee el método de los
**6 pasos** en la [lección del capstone](/fase-8-system-design/proyecto/) antes de empezar.

## 📏 Primero-Sin-IA (innegociable)

1. Diseña cada sistema **solo, a mano, dentro del timebox de 45 min**. Está bien que el primer diagrama
   sea feo y que tachones números.
2. Solo entonces consulta las lecciones (8.1, 8.2, 8.5, 7.7, 7.5x, 6.x).
3. **Solo al final**, usa una IA para *revisar y repreguntar* tu razonamiento —nunca para *generarlo*.
   Pídele que te ataque como un entrevistador hostil, no que te dé el diseño.
4. Mañana, reescribe de memoria los **6 pasos del método** y el **cuello de botella propio** de cada
   sistema. Si no te salen, no los aprendiste todavía.

## 🛠️ Instrucciones

Lee las tres especificaciones de esta carpeta:

- `sistema-1-rag-multitenant.md`
- `sistema-2-tickets-ia.md`
- `sistema-3-pipeline-datos.md`

Por **cada** sistema, produce un documento `diseno-1.md`, `diseno-2.md`, `diseno-3.md` con estas
**6 secciones**:

1. **Requisitos y restricciones.** Funcionales y no funcionales. Incluye al menos **un "esto no puede
   pasar nunca"** (la restricción dura que ordena el diseño).
2. **Números de servilleta.** El número que guía el diseño, con la **aritmética mostrada** (no solo el
   resultado). RAG → costo/hora a QPS de pico. Tickets → acciones sensibles/día y aprobaciones HITL/día.
   Pipeline → throughput de ingesta y **ventana de frescura**.
3. **Diagrama Mermaid.** El sistema completo, que **renderiza** (pruébalo en un editor Mermaid).
4. **El cuello de botella propio.** Cuál es (es distinto en cada sistema) y **cómo lo contienes**.
5. **Trade-offs defendidos con número.** Mínimo **2 por sistema**, cada uno nombrando qué sacrificas, su
   impacto numérico, y la **alternativa descartada**.
6. **Un ADR.** Por la decisión más jugosa de ese sistema: **Contexto / Decisión / Consecuencias**, con la
   alternativa descartada y el costo negativo que aceptas.

Deja, opcionalmente, un `supuestos.md` con cualquier supuesto que declares (números que la spec no fija).

## ✅ Criterios de "hecho" (Definition of Done del capstone)

- [ ] Los **tres** documentos de diseño existen, cada uno con las **6 secciones**.
- [ ] Cada diseño muestra **aritmética de servilleta coherente** (mostrada, no solo el resultado).
- [ ] Cada diagrama Mermaid **renderiza** y refleja el flujo real.
- [ ] **S1:** el aislamiento de tenants se trata como **seguridad** (filtro obligatorio, fail-closed), no
      como relevancia.
- [ ] **S2:** el reparto "el LLM propone, el código dispone" está; las acciones **irreversibles** pasan
      por **HITL** sin importar la confianza; hay un **eval gate** (qué mide, de dónde sale el golden set).
- [ ] **S3:** la **frescura** está definida (ventana) y el diseño nombra qué pasa cuando (a) un documento
      fuente cambia y (b) cambias el modelo de embeddings.
- [ ] **≥ 2 trade-offs por sistema**, cada uno con su número y su alternativa descartada.
- [ ] **Un ADR por sistema**, con las tres partes + alternativa descartada + costo aceptado.
- [ ] Puedes **defender los tres diseños en voz alta, sin notas**, contra una repregunta (check de
      dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/capstone-disena-3-sistemas/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`. Evalúa mi razonamiento (números, trade-offs, aislamiento, HITL,
> frescura, ADRs), no si mis diagramas coinciden con una solución única. Después, atácame con
> repreguntas como un entrevistador hostil."

La **solución de referencia** vive en `.ai/soluciones/fase-8/capstone-disena-3-sistemas.md` — no la mires
antes de cerrar tu intento de verdad.
