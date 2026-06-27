---
ejercicio_id: fase-6/diseno-evals-agente-y-juez
fase: fase-6
sub_unidad: "6.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir** de un diseño **competente**, no la única respuesta correcta. El alumno debe
> defender su propio diseño; usa esto para detectar huecos y graduar pistas.

# Solución de referencia — Plan de evals para un agente + un juez calibrado

> No hay "la" solución: es un ejercicio de diseño. Lo que sigue es un plan defendible que el
> corrector usa como referencia. Otros diseños razonables y bien justificados son válidos.

## 1. Métricas del agente (qué es determinista, qué necesita juez)

| Métrica | Determinista / con-juez | Cómo se mide | Por qué |
|---|---|---|---|
| **Tool-call accuracy** | **Determinista** | Comparar `(tool, args)` de cada paso contra el golden | "¿Llamó `consultar_pedido` con el id correcto?" es comparación exacta, no juicio |
| **Trajectory** | **Determinista** (flexible) | Comparar la secuencia contra una golden trajectory (exacta, por orden, o por conjunto de tools) | La forma del camino es verificable; se usa comparación flexible porque hay caminos válidos distintos |
| **Task completion** | **Con-juez** (o estado final) | LLM-as-judge sobre la respuesta + estado, o chequeo del estado final cuando existe | "¿Resolvió la duda del cliente?" es juicio abierto; solo si hay un estado final inequívoco (reembolso emitido) se vuelve determinista |
| **Costo / pasos** | **Determinista** | Sumar tokens/USD y contar vueltas; gate de presupuesto | Aritmética; un agente que acierta pero gasta USD 40 en 30 pasos **falló** en producción |

Punto fino: **costo/pasos no es opcional** y conecta con el **techo de pasos** del agent loop
de 6.8 — el guardrail de seguridad es, además, una métrica de eval. La mayoría de métricas de
agente son deterministas; el juez se reserva para task completion abierta.

## 2. Dataset desde trazas de prod

- El golden set se **promueve desde las trazas** registradas (entrada + trayectoria + salida),
  no se inventa. Mide lo que de verdad pasa, no lo imaginado.
- Se priorizan **fallidos y raros**: un reembolso emitido por error, un ticket que el agente
  escaló mal, un caso límite con argumentos ambiguos. Un fallo enseña más que diez éxitos
  triviales. Ejemplos a promover: (a) un ticket donde el agente llamó `emitir_reembolso` sin
  confirmación humana; (b) un ticket multi-intención ("me cobraron doble y la app no abre")
  donde la trayectoria correcta no es obvia.
- El dataset se **versiona** (v1, v2, …) para que las corridas sean comparables. Bucle de
  mejora: pulgar abajo del usuario en prod → caso nuevo del dataset.

## 3. LLM-as-judge para task completion

**Rúbrica:**
- *Criterio:* "¿La respuesta resuelve la intención del cliente usando solo información válida
  del sistema, sin inventar políticas ni datos?"
- *Escala:* 0.0–1.0 (o pass/fail con umbral 0.7).
- *Formato de salida del juez:* JSON `{"score": <float>, "razon": "<1-2 frases>"}` — fuerza
  una justificación y facilita auditar.

**Sesgos y mitigación (al menos dos):**
- **Position bias** (si se compara A vs B, prefiere la primera): correr el juicio en **ambos
  órdenes** y promediar; o evitar la comparación pareada usando **scoring absoluto** por
  rúbrica.
- **Verbosity bias** (premia lo largo): la rúbrica puntúa **sustento y exactitud**, no
  extensión, y **penaliza el relleno** explícitamente.
- **Self-enhancement bias** (prefiere su propia familia de modelos): usar un juez de **otra
  familia** que el modelo evaluado, o varios jueces.

**Validación del juez:** etiquetar a mano una **muestra** (p. ej. 50 casos) y medir el
**acuerdo juez-humano**; aceptar el juez solo si concuerda en ≥0.9 (o el umbral que el equipo
fije). Un juez no calibrado es ruido caro disfrazado de número.

## 4. Gate en CI + budget

- **Gate de regresión** sobre la métrica clave (p. ej. task completion media): bloquea si
  `score &lt; umbral` (barra absoluta) **o** si `score &lt; baseline - tolerancia` (regresión vs la
  versión en prod). La tolerancia absorbe el ruido del LLM no determinista.
- **Budget de costo/pasos:** techo de USD por tarea y de número de pasos; un PR que sube el
  costo medio por encima del techo **falla el build** aunque la calidad no baje.
- **Dónde corre:** en los PRs que tocan el agente (prompt, tools, modelo), con DeepEval
  (`assert_test` en pytest) o promptfoo en GitHub Actions; un score bajo umbral → exit code
  distinto de cero → build rojo.

## 5. Trazabilidad

- Cada score se ata a **prompt (versión) + modelo + versión de dataset** usando **Langfuse**
  como single source of truth: la traza registra la llamada y `score_current_trace` le adjunta
  el número, ligado a esa configuración exacta.
- Por qué importa: "task completion 0.92" sin contexto no vale nada. Con la cadena (prompt v7,
  modelo X, dataset v3) el número es **reproducible y comparable** entre corridas. Sin ella,
  comparas cosas no comparables y tus conclusiones son basura con decimales.

## Rango de soluciones aceptables
- Elegir **3 de las 4** métricas con buena justificación es `competente`; incluir costo/pasos
  es casi obligatorio para `competente` (es lo que la gente olvida).
- Usar **estado final** para task completion (cuando es inequívoco) en vez de un juez es válido
  e incluso preferible: lo determinista es más barato y estable.
- Cualquier par de sesgos bien mitigados cuenta; lo que NO se acepta es tratar al juez como
  objetivo o no validarlo contra humanos.
- El gate puede gatear sobre distintas métricas mientras distinga **umbral** de **regresión** e
  incluya un **budget de costo/pasos**. Un gate de solo-umbral es `en-progreso`.
- Mencionar HITL para el reembolso (acción irreversible) al evaluar acciones suma a `excelente`
  (conexión con seguridad de 6.8/6.14), pero no es obligatorio para `competente`.
