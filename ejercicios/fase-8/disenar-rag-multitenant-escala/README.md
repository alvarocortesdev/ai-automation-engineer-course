# Ejercicio 8.5a — Diseña un RAG multi-tenant para escala y costo

> **Modalidad: a mano (diseño + razonamiento, sin IA).** Este ejercicio entrena la pregunta de system
> design que distingue a un AI engineer: no "diseña Twitter", sino "diseña un asistente RAG
> multi-tenant" en 45 minutos. No hay código de producción; hay decisiones defendidas con números.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.5` Arquitectura de sistemas de IA a escala
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Diseñar la arquitectura de un asistente RAG **multi-tenant** para **escala y costo**:
  aislamiento de tenants, caché semántico, ruteo multi-modelo, cola de inferencia y fallback.
- **O2** — Estimar el **costo por hora** de generación con un cálculo de servilleta y usarlo para
  **priorizar** las intervenciones de ahorro.
- **O3** — Defender una decisión del **triángulo latencia/costo/calidad** con un trade-off explícito,
  registrada en un **ADR**.

## 📋 Contexto

Esta es la columna vertebral del [capstone de la fase](/fase-8-system-design/proyecto/): dos de los
tres sistemas en papel son de IA. Aquí practicas el más arquetípico (el RAG multi-tenant) end-to-end:
desde el número de costo hasta el ADR. Si dominas este, el de tickets con IA es una variante.

## 📏 Primero-Sin-IA

1. Diseña el sistema **solo**, a mano, dentro del timebox. Está bien que el primer diagrama sea feo.
2. Solo entonces consulta la lección (el ejemplo resuelto y la tabla del triángulo).
3. **Solo al final**, usa IA para *revisar y corregir* tu razonamiento — no para *generarlo*.
4. Mañana, reescribe de memoria el **orden de las 6 decisiones** y ve si te sale.

## 🛠️ Instrucciones

Lee la especificación en `sistema.md` (DocsAI, 40 tenants, 50 QPS de pico). Produce un documento de
diseño en `diseno.md` con **estas 6 secciones**:

1. **Números primero.** De QPS de pico a **costo por hora** de generación si todo va al modelo caro y
   nada se cachea. Muestra la aritmética: tokens de entrada × tarifa + tokens de salida × tarifa, por
   pregunta, × QPS × 3600.
2. **Aislamiento de tenants.** Decide entre índice-por-tenant e índice-compartido-con-filtro
   `tenant_id`. Nombra el **trade-off** (aislamiento vs costo operacional) y **cómo blindas el filtro**
   para que una fuga cruzada sea imposible, no solo improbable.
3. **Plan de costo ordenado por impacto.** Al menos **2 intervenciones** (caché semántico, ruteo
   multi-modelo). Para cada una: el **ahorro estimado** (usa el 45% de repetidas y las dos tarifas) y
   su **trade-off** (incluida la obsolescencia/invalidación de la caché).
4. **Resiliencia bajo pico.** Decide dónde va una **cola de inferencia** y dónde va **fallback** rápido.
   Justifica con la distinción **interactivo (chat) vs batch (resúmenes nocturnos)**.
5. **Una decisión del triángulo.** Señala **un** punto donde sacrificas conscientemente **calidad por
   costo** (o **latencia por estabilidad**) y di **por qué** es correcto para este negocio.
6. **Diagrama Mermaid + ADR.** Un diagrama del sistema resultante (debe renderizar) y **un ADR**
   (Contexto / Decisión / Consecuencias) para la decisión de aislamiento de tenants.

Deja también, opcionalmente, un `notas.md` con cualquier supuesto que declares.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las **6 secciones** están presentes.
- [ ] La **aritmética de costo** es coherente y está **mostrada** (no solo el resultado final).
- [ ] La decisión de **aislamiento** nombra su trade-off **y** describe el blindaje del filtro (por qué
      una query sin `tenant_id` debe ser imposible, no solo desaconsejada).
- [ ] **≥2 intervenciones** de costo, cada una con **ahorro estimado** y **trade-off** nombrado.
- [ ] La **cola** y el **fallback** están ubicados con justificación **interactivo/batch**.
- [ ] Hay **una decisión del triángulo** defendida como decisión de negocio (no "porque es mejor").
- [ ] El **diagrama Mermaid renderiza** y el **ADR** tiene sus tres partes.
- [ ] Puedes **defender el diseño completo sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/disenar-rag-multitenant-escala/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará tu **razonamiento** (los números, el trade-off de aislamiento, la decisión del
triángulo), no si tu diagrama es idéntico a una solución única — hay varias arquitecturas defendibles.
