# Ejercicio 4.0 — Diagnóstico, plan y mapa al capstone de Fase 4

> **Modalidad: a mano (sin IA).** Este es el ejercicio de entrada de la Fase 4.
> No mide si "sabes frontend": mide si entras con un **plan honesto** y si ves la
> fase como una **construcción hacia el capstone** (el frontend de una app de
> IA), no como 11 temas sueltos. Se corrige por honestidad y concreción, no por
> "respuesta correcta".

## Objetivos

- **O1** — Autoevaluar con honestidad tu nivel de partida en las 11 sub-unidades.
- **O2** — Diseñar un plan realista que **decida explícitamente** sobre la única
  sub-unidad opcional (4.9 design systems) según tu rol objetivo.
- **O3** — Mapear cada punto del **Definition of Done del Capstone F4** a las
  sub-unidades que lo enseñan (*constructive alignment*).

## Contexto

La Fase 4 te lleva de no haber escrito una etiqueta HTML a tener el **frontend
de una app de IA con streaming** (el capstone `4.P`), accesible y con todos sus
estados. Antes de empezar conviene saber **de dónde partes** y **hacia dónde
construyes**. Las 11 sub-unidades:

| Camino crítico | Opcional / profundización |
|---|---|
| 4.1 HTML + CSS · 4.2 Tailwind · 4.3 Diseño visual · 4.4 Accesibilidad WCAG 2.2 · 4.5 React + TS · 4.6 Next.js · 4.7 Estado y datos · 4.8 Estado global · 4.10 Usabilidad y estados · 4.11 UI para apps de IA | 4.9 Design systems |

Los 7 puntos del **Definition of Done del Capstone F4** (de la portada de la fase):

1. Spec inicial (pantallas, estados, contrato con la API) + ADRs de decisiones clave.
2. Tests verdes + lint en CI; calidad por aserciones reales (no % de cobertura).
3. Seguridad web: no renderizar como HTML la salida no confiable del LLM (XSS), manejo de errores contra la API.
4. Observabilidad mínima: error tracking en el cliente + correlation ID propagado al backend F3.
5. a11y WCAG 2.2 + estados completos (empty/loading/error/success) como **gate**.
6. Demo que CORRE + README en inglés + write-up de trade-offs.
7. Conventional Commits en todo el historial.

## Tu tarea (Primero-Sin-IA, timebox 35 min)

Crea tres archivos markdown **en esta carpeta**:

1. **`diagnostico.md`** — tabla con las 11 sub-unidades (4.1 a 4.11) y tu nivel
   **honesto** por cada una: `nuevo` · `lo reconozco` · `lo sé hacer sin notas`.
   La prueba de "lo sé hacer" es concreta: ¿podrías, **ahora, sin notas y sin
   IA**, maquetar una tarjeta responsive / explicar Server vs Client Components /
   hacer un modal accesible con teclado? Si dudas, no es "lo sé hacer".

2. **`plan-fase-4.md`** — tu plan de estudio:
   - **Bloques semanales concretos** (día + hora + duración), no buenas
     intenciones.
   - Tu **ritual de repaso** (cuándo reescribes de memoria lo del día anterior).
   - Una **decisión explícita sobre la opcional 4.9 (design systems)**: ¿la haces
     o la saltas? **Justificada por tu rol objetivo** (ej.: "salto design systems
     por ahora; con Tailwind + estados sólidos me alcanza para el capstone; la
     retomo si un rol pide componentes a escala").

3. **`mapa-capstone.md`** — tabla que conecte **cada uno de los 7 puntos del
   Definition of Done** con **qué sub-unidad(es) te lo enseñan**. Una fila por
   punto del DoD.

## Qué entregar

- `diagnostico.md`, `plan-fase-4.md`, `mapa-capstone.md` en esta carpeta.

## Hecho significa

- [ ] El diagnóstico cubre las **11** sub-unidades con un nivel **defendible**
      (no todo en "lo sé hacer": eso es sobreconfianza, no diagnóstico).
- [ ] El plan tiene **bloques reales** en tu semana y un ritual de repaso.
- [ ] El plan **decide explícitamente** sobre la opcional 4.9, **con una razón**
      ligada a tu objetivo (no "quizás", no la ignora).
- [ ] El mapa conecta los **7** puntos del DoD con **al menos una** sub-unidad
      cada uno, sin inventar conexiones forzadas.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/fase-4-index/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará la **honestidad** de tu autoevaluación, la **realidad** de
tu plan y la **coherencia** de tu mapa, no si "acertaste". No hay respuesta única.
</content>
