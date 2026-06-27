---
ejercicio_id: fase-4/estados-ui-chat-ia
fase: fase-4
sub_unidad: "4.11"
version: 1
---

# Rúbrica — Diseña los estados y la seguridad de una UI de chat de IA

> Rúbrica analítica atada a los `objetivos` del contrato. Es un ejercicio de **razonamiento/diseño**:
> la entrega es `diseno-chat.md`, no hay suite. El corrector evalúa la **calidad del razonamiento**
> (inventario de estados, diagnóstico del buggy, seguridad, a11y, trade-off), no una nota numérica.

## Objetivos evaluados
- **O1** — Inventariar y diseñar los seis estados de primera clase y sus transiciones.
- **O2** — Diagnosticar los riesgos de seguridad (XSS) y accesibilidad de renderizar salida de un LLM.
- **O3** — Justificar optimistic UI y el trade-off de latencia/UX del streaming.

## Criterios y niveles

### C1 — Inventario de estados (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan estados (solo "cargando/listo"), o no distingue `streaming` de `enviando`. |
| **en-progreso** | Nombra la mayoría de los seis pero confunde dos, o no asocia la transición que activa cada uno. |
| **competente** | Los seis estados (vacío/enviando/streaming/completado/error/cancelado), cada uno con qué ve el usuario y qué transición lo activa. |
| **excelente** | Distingue con nitidez `enviando` (mandé, nada llegó: "pensando") de `streaming` (llegan chunks: "escribiendo"), y trata `cancelado` y `error` como estados de pleno derecho con su affordance. |

### C2 — Diagnóstico del componente buggy (comprensión) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Detecta uno o ningún defecto; no propone arreglo. |
| **en-progreso** | Detecta varios pero se le pasa el XSS o el "sin optimistic UI"; arreglos vagos. |
| **competente** | Nombra los cuatro defectos principales (sin streaming, sin optimistic UI, sin estados, XSS) y, para cada uno, el patrón de la lección que lo arregla. |
| **excelente** | Añade el déficit de a11y (sin `aria-live`) y/o de error mudo, y conecta cada arreglo con la sección concreta de la lección. |

### C3 — Seguridad (OWASP web) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica el XSS, o cree que "como viene de mi backend es seguro". |
| **en-progreso** | Identifica el riesgo pero la regla correcta es difusa ("usar una librería" sin decir cuál ni por qué). |
| **competente** | Explica que la salida del LLM es no confiable (inducible vía prompt injection), que `dangerouslySetInnerHTML` = XSS, y la regla: renderizar como texto (React escapa en `{}`) o markdown sanitizado sin HTML. Conecta con OWASP de la Fase 3. |
| **excelente** | Menciona defensa en profundidad (también sanitizar/validar en el backend) y que el riesgo aplica aunque "sea tu propio endpoint" porque solo reenvía lo del modelo. |

### C4 — Accesibilidad + trade-off (comprensión) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra medidas de a11y; el trade-off es "streaming es mejor" sin matiz. |
| **en-progreso** | Una medida de a11y; el trade-off menciona beneficio pero no costo. |
| **competente** | Dos medidas concretas (p. ej. `aria-live="polite"`, foco/teclado, "Detener" alcanzable) y un trade-off honesto: streaming + optimistic = mejor latencia percibida, a costa de más complejidad de estado. |
| **excelente** | Articula que el streaming NO acelera la generación (latencia percibida, no real) y por qué eso igual justifica la complejidad extra; conecta a11y con [4.4 WCAG](/fase-4-frontend/4-4-accesibilidad-wcag/). |

## Errores típicos a marcar
- Colapsar `enviando` y `streaming` en un solo "cargando" → pierde el estado más característico de la UI de IA.
- "Como el texto viene de mi backend, puedo renderizarlo como HTML" → no entiende que el backend solo reenvía la salida del modelo (C3).
- Proponer borrar el parcial ante error → mala UX (contradice 4.6).
- Trade-off como "streaming siempre mejor" sin nombrar el costo (más estado que manejar) ni el matiz de latencia percibida.
- (transversal) inventa estados que no existen o se olvida de `cancelado`/`vacío`.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Documento exhaustivo y bien formateado pero que, al preguntar, no puede explicar por qué `streaming` ≠ `enviando`, o por qué el XSS aplica "aun siendo mi backend".
- Cita patrones avanzados (suspense, error boundaries, SSE a mano) sin poder defender cuándo usarlos.
- **Verificación sugerida:** pídele que, en una frase, diga qué ve el usuario en `enviando` vs `streaming`; o que defienda por qué validar/escapar en el cliente no exime de hacerlo en el servidor. Respuesta fluida = entendió; titubeo = copió.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia.
- **Pista (nivel 1):** "Cuenta los estados: ¿qué ve el usuario justo después de enviar y antes de que llegue el primer token? ¿Es lo mismo que mientras el texto crece?"
- **Pregunta socrática (nivel 2):** "Si un atacante logra que el modelo devuelva `<script>…`, ¿qué pasa en tu UI según cómo renderizas el texto? ¿Qué línea exacta abre o cierra esa puerta?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu inventario debe tener seis estados, no cuatro: separa enviando de streaming y trata cancelado/vacío como estados reales. Para seguridad, la regla es renderizar como texto o markdown sanitizado; nombra por qué `dangerouslySetInnerHTML` es el riesgo. No te doy el documento."

## Conexión con el proyecto / capstone
- Este inventario es el plano de la UI del [Capstone F4](/fase-4-frontend/proyecto/): cada estado que nombres aquí es un estado que tendrás que dibujar allá, y la regla de seguridad (no renderizar HTML del LLM) es un gate del Definition of Done.
