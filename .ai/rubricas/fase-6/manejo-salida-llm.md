---
ejercicio_id: fase-6/manejo-salida-llm
fase: fase-6
sub_unidad: "6.14"
version: 1
---

# Rúbrica — Output handling: trata la salida del LLM como no confiable

> Rúbrica **analítica** para un ejercicio de **código**. Se evalúa la **política de
> seguridad** (orden y razón de las capas) y la comprensión de **por qué** se codifica
> en un caso y se bloquea en otro — no solo si `pytest` pasa. Un alumno puede hacer
> pasar los tests con la lógica correcta y aun así no entender LLM05; ahí miras el
> write-up.

## Objetivos evaluados
> De `objetivos` en `ejercicio.yml`.

- **O1** — Implementar el gate de tres capas (fuga → presupuesto → codificación).
- **O2** — Distinguir cuándo **codificar** para el sink de cuándo **bloquear**.
- **O3** — Mapear cada capa a su riesgo OWASP LLM (LLM05, LLM07/LLM02, LLM10).
- **O4** — Explicar por qué la salida del LLM es no confiable.

## Criterios y niveles

### C1 — Corrección del gate (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No implementa, o los tests no pasan, o invierte la decisión (bloquea el `<script>` y/o renderiza un secreto). |
| **en-progreso** | Tests pasan pero el orden de las capas está mal (p. ej. revisa longitud antes que fuga) o usa un escaper a mano frágil en vez de `html.escape`. |
| **competente** | Tres capas en orden (fuga → presupuesto → codificación), `pytest` verde, usa `html.escape`. |
| **excelente** | Además: `motivo` informativo por rama (pensando en logs/observabilidad), comparación de fuga robusta (insensible a mayúsculas como pide el contrato), y maneja el borde (vacío, frontera exacta del presupuesto). |

### C2 — Comprensión: codificar vs bloquear (la asimetría LLM05) · mapea: O2, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El write-up no distingue por qué el `<script>` se escapa y el secreto se bloquea; los trata igual. |
| **en-progreso** | Intuye que "uno se muestra y otro no" pero no lo liga al **sink** ni a "no hay codificación que vuelva seguro mostrar un secreto". |
| **competente** | Explica que el HTML peligroso se **neutraliza por codificación** (queda inerte para el sink HTML), mientras que una fuga **no tiene codificación segura**: se bloquea. |
| **excelente** | Generaliza: la defensa de LLM05 es **context-aware**: el mismo texto es seguro para un sink (texto plano) y peligroso para otro (HTML/SQL/shell); la decisión depende del **destino**. |

### C3 — Mapeo OWASP y testing (calidad de ingeniería) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin mapeo OWASP, o inventado. |
| **en-progreso** | Nombra LLM05 pero no conecta la capa de fuga (LLM07/LLM02) ni el presupuesto (LLM10). |
| **competente** | Cada capa mapeada: codificación → LLM05, fuga → LLM07/LLM02, presupuesto → LLM10; los tests verifican política, no implementación. |
| **excelente** | Reconoce que `html.escape` es una defensa parcial y que en **prod** usaría una librería vetada (bleach/DOMPurify); nombra que hacer un sanitizador HTML a mano es **en sí** una vulnerabilidad. |

## Errores típicos a marcar
- **Bloquear el `<script>` en vez de escaparlo** — confunde "peligroso" con "prohibido"; para el sink HTML la defensa correcta es codificar.
- **Renderizar un secreto "porque no tiene HTML"** — la fuga manda sobre todo lo demás.
- **Orden invertido** — revisar longitud o codificar antes de escanear fugas deja salir un secreto largo.
- **Escaper a mano** (reemplazar `<` por `&lt;` manualmente) — frágil y, en prod, anti-patrón; usa la stdlib / librería vetada.
- **Denylist de "frases peligrosas" en la salida** — mismo error que en la entrada: el espacio de paráfrasis es infinito.
- (transversales) confiar en la salida del LLM sin validar; no loguear la decisión (sin observabilidad no hay auditoría).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución impecable con `motivo` y bordes cubiertos, pero el alumno no sabe explicar **por qué** se escapa el `<script>` y se bloquea el secreto cuando se le pregunta.
- Usa una librería pesada o un regex sofisticado que no calza con el nivel del ejercicio ni con el contrato (que pide `html.escape`).
- **Verificación sugerida:** pídele que diga qué cambiaría si el sink fuera **SQL** o **un correo a otro agente** en vez de HTML. Si entendió LLM05 (context-aware), responde; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca escribir la solución por el alumno.
- **Pista (nivel 1):** "Tu gate funciona, pero ¿por qué bloqueas el `<script>`? Piensa en qué le pasa a `<script>` después de `html.escape`: ¿sigue siendo ejecutable?"
- **Pregunta socrática (nivel 2):** "¿Existe alguna forma de **codificar** un secreto para que sea seguro mostrarlo? ¿Y de codificar un `<script>` para que sea seguro mostrarlo? ¿Por qué la respuesta es distinta?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "La asimetría es el punto: el HTML peligroso se vuelve inerte al codificarlo para su sink (queda como texto), así que se RENDERIZA escapado. Un secreto no tiene codificación que lo haga seguro de mostrar, así que se BLOQUEA. Por eso el orden es fuga → presupuesto → codificación, y por eso LLM05 es 'output handling según el destino', no 'borrar lo feo'."

## Conexión con el proyecto / capstone
- Este gate es un componente real del Definition of Done del capstone (validación de
  salida antes de mostrar/ejecutar) y de la capa de output handling del agente de Fase 7.
  Lo que escribas aquí se conecta con la seguridad que profundiza
  [6.14](/fase-6-ai-engineering/6-14-seguridad-llm/) y queda registrado en el ADR de
  seguridad del proyecto.
