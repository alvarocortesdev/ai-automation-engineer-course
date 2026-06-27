# Ejercicio 6.1 — Decisiones de sampling, alucinación y modelo

> **Modalidad: a mano (diseño/razonamiento, sin código).** No hay tests que pasen:
> lo que se evalúa es tu **criterio de ingeniería**. Igual que en una entrevista de
> system design, no hay una única respuesta "correcta" — hay decisiones bien o mal
> **justificadas**.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.1` Fundamentos de LLMs
**Ruta:** crítica · **Timebox:** 35 min

## Objetivos

- **O1** — Elegir y justificar un setting de sampling (temperature / top-p, o su
  ausencia) apropiado a cada tarea.
- **O2** — Evaluar el riesgo de alucinación de un caso y diseñar **dos**
  mitigaciones concretas.
- **O3** — Elegir una familia/tier de modelo del panorama 2026 nombrando la
  **restricción dominante** (costo / latencia / privacidad / calidad).

## Los tres escenarios

1. **Generador de SQL interno.** Una herramienta interna donde analistas escriben
   una pregunta en lenguaje natural y el LLM genera la consulta SQL que se ejecuta
   sobre la base de datos de la empresa. Volumen bajo, usuarios técnicos, datos
   corporativos sensibles que no pueden salir de la infraestructura.

2. **Generador de nombres de marca.** Un asistente de marketing que propone 15–20
   nombres creativos para un producto nuevo, con eslóganes. Uso esporádico, no hay
   datos sensibles, se valora la **variedad** y la sorpresa.

3. **Bot de FAQ de cara al cliente.** Un chat público en el sitio web que responde
   preguntas sobre políticas de devolución, horarios y precios, **a partir de los
   documentos internos** de la empresa. Alto volumen, latencia visible al usuario,
   y una respuesta inventada (un precio o una política falsa) genera un problema
   real con clientes.

## Tu tarea (Primero-Sin-IA, sin consultar a la IA)

Crea un archivo `decisiones.md`. Para **cada uno** de los tres escenarios, completa
esta plantilla:

```markdown
## Escenario N — <nombre>

- **Sampling:** <temperature baja / alta / no aplica> — <una línea de por qué,
  ligada a la tarea>
- **Riesgo de alucinación:** <bajo / medio / alto> — <por qué en este caso>
- **Mitigación 1:** <qué harías y qué ataca>
- **Mitigación 2:** <distinta de la anterior, qué ataca>
- **Modelo (familia/tier):** <frontera / balanceado / rápido, y familia> —
  **restricción dominante:** <costo / latencia / privacidad / calidad> + 1 línea
  de trade-off (qué ganas y qué cedes)
```

Reglas:
- Las **dos mitigaciones** de cada escenario deben ser **distintas** (no repitas
  "temperature baja" como mitigación si ya la pusiste en sampling).
- En "modelo", nombra la restricción que **manda** en ese caso, no solo "el mejor".
- No tienes que acertar nombres comerciales exactos; basta con familia + tier +
  razonamiento (p. ej. "open-weight self-hosted" o "tier rápido tipo Haiku/Flash").

## Qué entregar

- `decisiones.md` — los tres escenarios con la plantilla completa.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios resueltos con la plantilla.
- [ ] Cada decisión de sampling está **justificada por la tarea** (no "porque sí").
- [ ] Cada escenario tiene **dos** mitigaciones distintas y apropiadas.
- [ ] Cada elección de modelo nombra la **restricción dominante**, no solo
      "el mejor".
- [ ] Puedes **defender en voz alta** cualquiera de tus nueve decisiones sin notas.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/decisiones-sampling-modelo/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará la **coherencia** de tus decisiones con la tarea, no si
coinciden con una respuesta única.
