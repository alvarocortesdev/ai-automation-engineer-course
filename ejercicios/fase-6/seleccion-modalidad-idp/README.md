# Ejercicio 6.11 — Elegir la modalidad y diseñar el pipeline de IDP

> **Modalidad: a mano (diseño / razonamiento).** No hay código que ejecutar ni tests. El
> entregable es un documento de diseño donde **eliges** la herramienta multimodal correcta
> para cada caso y **justificas** por la restricción dominante. Es el tipo de decisión que
> defiendes en una entrevista de system design.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.11` Multimodal: STT/TTS/vision/OCR-IDP
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O1** — Elegir el adaptador multimodal correcto (STT / TTS / vision / OCR-IDP) y el
  modo (API vs local) para un escenario, justificando por la **restricción dominante**.
- **O2** — Defender la elección de **IDP especializado vs LLM de vision** nombrando qué se
  **pierde** con la elección.
- **O3** — Diseñar un pipeline de IDP con **gate de confianza + HITL + validación cruzada**,
  más sus controles de seguridad/privacidad y observabilidad.

## Tu tarea (Primero-Sin-IA)

Resuélvelo **a mano**, razonando tú primero. Solo después consulta documentación oficial;
y solo al final usa IA para *revisar*, no para *generar*. Escribe todo en `diseno.md`.

### Parte A — Elegir la modalidad (4 escenarios)

Para cada escenario, indica: **(1)** qué adaptador usas (STT / TTS / vision / OCR-IDP),
**(2)** API o local, y **(3)** cuál es la **restricción dominante** que decide (la cosa
que, si la haces mal, hunde el caso). Una o dos líneas por escenario.

1. **Subtítulos en vivo** para un webinar en español, con baja latencia.
2. **8.000 facturas/mes** de proveedores conocidos; un total mal leído **paga de más**.
3. Una app que **describe en voz alta lo que muestra la cámara**, para una persona con
   baja visión.
4. **Transcribir entrevistas médicas** grabadas, con datos de pacientes que **no pueden
   salir de la empresa**.

### Parte B — Diseñar el pipeline de IDP del escenario 2

Diseña el flujo end-to-end (puedes usar un diagrama Mermaid). Cubre:

- **Servicio:** ¿IDP especializado (Document Intelligence) o LLM de vision? Justifica por
  la restricción dominante y nombra **qué pierdes** con tu elección.
- **Gate de confianza + HITL:** dónde pones el umbral, qué pasa con los campos arriba y
  abajo, y por qué el monto es el campo más delicado.
- **Validación cruzada:** qué **regla de negocio** chequeas más allá del confidence (p. ej.
  la suma de las líneas vs el total) y qué error atrapa que el gate deja pasar.
- **Seguridad y privacidad:** nombra **dos** riesgos distintos (p. ej. indirect prompt
  injection desde el texto del documento — LLM01; PII en las facturas —
  privacidad/governance, 6.15) con **una mitigación concreta cada uno**.
- **Observabilidad:** **dos** métricas que registrarías para saber si el pipeline está
  sano (p. ej. tasa de revisión humana, distribución de confidence, tasa de fallo de la
  validación cruzada).

## Qué entregar

- `diseno.md` — Partes A y B completas, con justificaciones por restricción dominante.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 4 escenarios traen una **restricción dominante** explícita, no un "me gusta más".
- [ ] El escenario 4 va **local** por privacidad (no API de terceros) y lo justificas.
- [ ] El escenario 2 elige IDP vs vision nombrando qué **pierdes**.
- [ ] El gate de confianza distingue auto-aceptar de HITL con un **umbral concreto**.
- [ ] La validación cruzada es una **regla de negocio real**, no "revisar más confidence".
- [ ] **Dos** riesgos de seguridad/privacidad distintos, cada uno con mitigación accionable.
- [ ] **Dos** métricas de observabilidad accionables.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/seleccion-modalidad-idp/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará la **calidad de tus justificaciones** (¿hay una restricción
dominante real?, ¿nombras lo que pierdes?), no que coincidas con una respuesta única —
varios diseños son válidos si están bien defendidos.
