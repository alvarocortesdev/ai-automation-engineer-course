---
ejercicio_id: fase-6/decisiones-sampling-modelo
fase: fase-6
sub_unidad: "6.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**, no la única respuesta: el ejercicio es de diseño y admite caminos
> válidos distintos. Mide coherencia y justificación, no coincidencia literal.

# Solución de referencia — Decisiones de sampling, alucinación y modelo

## Respuesta canónica (una de varias defendibles)

### Escenario 1 — Generador de SQL interno
- **Sampling:** temperature **baja** (o greedy). Quieres SQL correcto y
  reproducible; nada de "creatividad" que invente columnas. *(Matiz 2026: si el
  modelo elegido no expone temperature, se steerea con un prompt estricto + few-shot.)*
- **Riesgo de alucinación:** **alto** de impacto — el SQL se ejecuta sobre datos
  reales; una tabla o columna inventada puede fallar o, peor, devolver datos
  equivocados que el analista cree correctos.
- **Mitigación 1:** **dar el esquema** (tablas/columnas) en el contexto (grounding):
  ataca la causa raíz —que el modelo adivine nombres de su memoria—.
- **Mitigación 2:** **validar antes de ejecutar** (parsear el SQL, correrlo en
  modo de solo-lectura / `EXPLAIN`, o exigir confirmación humana): no actuar sobre
  salida cruda. Encaja con HITL.
- **Modelo:** **open-weight self-hosted** (Qwen / DeepSeek / Llama). **Restricción
  dominante: privacidad** — los datos corporativos no pueden salir de la infra.
  Trade-off: cedes algo de calidad/comodidad frente a una API frontera, pero
  garantizas que nada sensible viaja afuera.

### Escenario 2 — Generador de nombres de marca
- **Sampling:** temperature **alta** (y/o top-p ~0.9). Quieres variedad y sorpresa;
  el determinismo aquí es un defecto.
- **Riesgo de alucinación:** **bajo de impacto** — un nombre "inventado" es
  justamente lo que se pide; no hay un hecho que falsear. (Cuidado solo con que un
  nombre no choque con una marca registrada, pero eso es validación posterior,
  no alucinación factual.)
- **Mitigación 1:** pedir **muchas** opciones y dejar que el humano filtre (HITL
  ligero); el riesgo real es trivial.
- **Mitigación 2:** chequear disponibilidad (dominio / marca registrada) **fuera**
  del LLM, con una API o búsqueda — no confiar en que el modelo "sepa" si está libre.
- **Modelo:** **tier rápido/barato** (Haiku / mini / Flash-Lite). **Restricción
  dominante: costo** — la tarea es fácil y esporádica; un frontera sería pagar de
  más. Trade-off: prosa un pelo menos pulida, irrelevante para lluvia de ideas.

### Escenario 3 — Bot de FAQ de cara al cliente
- **Sampling:** temperature **baja**. Es factual y público; no quieres que
  reformule políticas con variantes que cambien el sentido.
- **Riesgo de alucinación:** **alto** — una respuesta inventada (precio o política
  falsa) frente a un cliente genera un problema real, legal o de confianza.
- **Mitigación 1:** **RAG / grounding** sobre los documentos internos — la única
  forma robusta de que responda con la política real y actual, no con su memoria.
- **Mitigación 2:** instrucción explícita de **"si no está en los documentos, di
  que no sabes / deriva a un humano"** + (idealmente) citar la fuente. Evita el
  relleno cuando falta el dato.
- **Modelo:** **tier rápido** (Haiku / Flash) con calidad suficiente.
  **Restricción dominante: latencia + costo** — chat público de alto volumen y en
  vivo; la calidad la aporta el RAG, no un modelo gigante. Trade-off: empezar
  barato y subir de tier solo si los evals muestran que falla.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Sampling invertido** en SQL o FAQ (alto) o en nombres (bajo): error de
   concepto, marcarlo.
2. **Privacidad ignorada** en el caso SQL: mandar datos sensibles a una API cerrada
   es el error más grave del ejercicio.
3. **FAQ tratado como bajo riesgo**: subestimar el impacto de mentir a un cliente.
4. **Mitigaciones repetidas o que no mitigan**: dos veces "temperature baja", o
   "usar un mejor modelo" como si fuera una defensa contra alucinación.
5. **"El mejor modelo"** sin nombrar la restricción dominante.

## Rango de soluciones aceptables

- En el FAQ, elegir un **tier balanceado** en vez de rápido es defendible si el
  alumno argumenta que la calidad de respuesta pesa más que la latencia; lo que se
  evalúa es la **justificación**, no el tier exacto.
- En SQL, si el alumno argumenta que los datos **no** son realmente sensibles en su
  organización y por eso usa una API cerrada, es válido **siempre que lo justifique
  explícitamente** (cambió la restricción dominante conscientemente).
- Cualquier par de mitigaciones distintas y pertinentes cuenta; no se exige que
  sean las de arriba. Citar dónde se profundiza (RAG→6.7, validación→6.4,
  evals→6.9) es señal de `excelente`, no requisito.
- No se exige nombre comercial exacto del modelo: familia + tier + restricción
  basta.
