---
ejercicio_id: fase-4/fase-4-index
fase: fase-4
sub_unidad: "4.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio
> no tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de
> qué observar. Úsalo como vara de medir honestidad/realismo/alineación, nunca
> como plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico, plan y mapa al capstone de Fase 4

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier
conjunto de tres archivos que sea **honesto, concreto y alineado con el
capstone**. La calidad se mide por el proceso (autoevaluación, planificación,
mapeo), no por contenido específico.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar (alumno cero real)
Tabla con las **11** sub-unidades. En un cero real (que ya pasó F0–F3), lo
esperable es mayoría de `nuevo` con algún `lo reconozco` en lo más cercano a lo
ya visto (p. ej. HTML/CSS si tocó algo de web). La señal de calidad es la
**razón por fila** y aplicar la prueba "¿podría hacerlo sin notas ahora?".

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 4.1 HTML + CSS | lo reconozco | Vi etiquetas y algo de CSS, pero nunca maqueté un layout con grid. |
| 4.2 Tailwind | nuevo | Nunca usé utility-first. |
| 4.3 Diseño visual | nuevo | No tengo criterio de jerarquía/espaciado; mis pantallas se ven amateur. |
| 4.4 Accesibilidad WCAG 2.2 | nuevo | No sé navegar con teclado ni qué es el contraste mínimo. |
| 4.5 React + TS | nuevo | Nunca escribí un componente ni un hook. |
| 4.6 Next.js | nuevo | No sé qué es App Router ni Server vs Client Components. |
| 4.7 Estado y datos | nuevo | No conozco TanStack Query ni RHF + zod. |
| 4.8 Estado global | nuevo | No sé cuándo necesito estado global. |
| 4.9 Design systems (opcional) | nuevo | — |
| 4.10 Usabilidad y estados | nuevo | No pienso en empty/loading/error; solo el camino feliz. |
| 4.11 UI para apps de IA | nuevo | Nunca rendericé un stream de tokens. |

> Para un perfil **oxidado-con-experiencia** (p. ej. tocó React o desplegó en
> Vercel), lo esperable es más `lo reconozco` y algún `lo sé hacer sin notas`
> —pero solo si lo puede defender. La trampa a detectar es marcar "lo sé hacer"
> sin evidencia (sobreconfianza), sobre todo en 4.4 (accesibilidad real con
> teclado/foco), 4.7 (diferencia estado servidor vs cliente) y 4.6 (Server vs
> Client Components), que casi nadie domina aunque "haya hecho React".

### `plan-fase-4.md` — exemplar
Un plan creíble, p. ej.:
- **Lun/Mié 20:00–21:00** (2 bloques × 60 min) + **Sáb 10:00–12:00** (sesión larga).
- **Ritual de repaso:** cada sesión arranca con 5–10 min reescribiendo de memoria
  lo del bloque anterior; los sábados, repaso de la semana.
- Más tiempo asignado a lo marcado `nuevo` (casi todo, en un cero real), con foco
  especial en React/Next.js (4.5–4.6), que es donde se concentra la carga.
- **Decisión sobre la opcional 4.9**, con razón. Ejemplos defendibles:
  - **Saltar** → "Con Tailwind (4.2) y estados sólidos (4.10) me alcanza para el
    capstone; design tokens los retomo si un rol pide UI a escala."
  - **Hacer** → "Apunto a roles de producto con design system; shadcn/Radix me
    acelera el capstone y los siguientes."

La señal de calidad: **día/hora concretos**, **ritual de repaso explícito** y una
**decisión razonada sobre 4.9** (no "quizás", no ignorarla). Tanto hacerla como
saltarla son válidas y `excelente` si la razón es coherente con el rol.

### `mapa-capstone.md` — exemplar
Tabla que conecta los 7 puntos del DoD con las sub-unidades. Mapeo de referencia:

| # DoD | Punto | Sub-unidad(es) que lo enseñan |
|---|---|---|
| 1 | Spec + ADRs (pantallas, estado, streaming) | Hábito de F0/F2 reaplicado; las decisiones de 4.6 (Server/Client), 4.7/4.8 (estado) y 4.11 (streaming) son el material de los ADRs. |
| 2 | Tests verdes + lint en CI (aserciones reales) | Hábito de F2 reaplicado; aserciones de comportamiento sobre componentes (Testing Library) que se montan en 4.5–4.6. |
| 3 | Seguridad web (XSS, salida del LLM) | **4.11** (no renderizar HTML no confiable del modelo) + base OWASP de F3 (3.13). |
| 4 | Observabilidad mínima (error tracking + correlation ID) | Se apoya en **4.6** (Next.js) + el contrato con la API de **F3**; puente a F5. |
| 5 | a11y WCAG 2.2 + estados completos (GATE) | **4.4** (teclado/foco/contraste/ARIA) + **4.10** (empty/loading/error/success); refuerzo en 4.11 (estados del LLM). |
| 6 | Demo que corre + README inglés + write-up | Integra todo; UI visible (4.1–4.3), app (4.5–4.6), estados (4.10–4.11). |
| 7 | Conventional Commits | Hábito desde F0; se mantiene. |

Señal de calidad: los 7 puntos conectados, con los "difíciles" bien ubicados
(a11y+estados→4.4/4.10, **no** a Next.js genérico; seguridad de salida del
LLM→4.11; observabilidad→4.6 + contrato con F3). `Excelente` si además nota qué
partes del DoD la fase **no** cubre del todo (trazas OTel completas, eval harness
de IA), que llegan en F5/F6.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Sobreconfianza en el diagnóstico.** "Lo sé hacer" sin evidencia, en especial
   en 4.4 (accesibilidad con teclado), 4.6 (Server vs Client Components) y 4.7
   (estado servidor vs cliente). Verificación: que justifique una fila en voz alta.
2. **Opcional sin decidir.** Dejar 4.9 en "quizás" o ignorarla incumple O2; o
   tratarla como obligatoria (confundir camino crítico con profundización).
3. **Mapa forzado o que omite el gate.** Mapear todo a 4.6 "porque es Next.js", o
   no ubicar el punto 5 (a11y + estados) en 4.4/4.10. Es el punto estrella de la
   fase: si no aparece bien, el alumno no entendió la vara.
4. **Plan que no responde al diagnóstico.** Marca varias `nuevo` pero reparte el
   tiempo por igual: la autoevaluación no está sirviendo.
5. **Delegar a la IA.** Plan genérico y pulido sin contexto real del alumno.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables
  están y son honestos/concretos/alineados.
- Saltar o hacer 4.9 son ambas válidas: lo que se evalúa es la **razón** ligada al
  rol objetivo, no la elección.
- Un plan **modesto pero sostenible** es preferible a uno ambicioso e irreal.
- En el mapa, varias asociaciones son defendibles (p. ej. el punto 1 puede ligar
  a 4.6, 4.7/4.8 o 4.11, o a varios); no penalizar un camino válido distinto al de
  arriba mientras esté justificado. La excepción dura: el punto 5 (a11y+estados)
  debe aterrizar en 4.4 y/o 4.10, no en "Next.js".
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se mide la
  **calidad del proceso**, no el nivel de partida.
</content>
