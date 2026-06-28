---
ejercicio_id: fase-8/capstone-disena-3-sistemas
fase: fase-8
sub_unidad: "8.P"
version: 1
---

> 🚫 **SPOILER — material del CORRECTOR. No mostrar al alumno.** Úsala solo como vara de medir, al final,
> cuando ya formaste tu propio juicio. Hay **varias** arquitecturas defendibles por sistema; lo que
> importa es que cada decisión tenga un número o un trade-off detrás, no que el diagrama coincida con
> este. Nunca pegues ni parafrasees de forma reconstruible esta solución al alumno.

# Solución de referencia — Diseña 3 sistemas en papel

El hilo común de los tres: **número primero → diagrama → cuello de botella propio → trade-offs con su
número → ADR con alternativa descartada**. Un alumno `excelente` aplica ese método de forma visible en
los tres; uno `competente` llega a buenas decisiones aunque el método no sea tan explícito.

---

## SISTEMA 1 — RAG multi-tenant (AskDocs)

### Respuesta canónica (resumen)
- **Número:** por pregunta al modelo caro = entrada 3.000 × (5/1e6) + salida 500 × (25/1e6) = 0,015 +
  0,0125 ≈ **USD 0,0275**. A 50 QPS sin caché: 0,0275 × 50 × 3600 ≈ **USD ~4.950/hora**. Ese número manda.
- **Aislamiento:** índice vectorial **compartido con filtro `tenant_id` obligatorio y fail-closed**; el
  `tenant_id` es parte de la firma de la función de retrieval (no se puede llamar sin él) + test negativo
  que intenta consultar sin filtro y debe fallar. **Índice dedicado para los 3 tenants regulados.** Es
  seguridad (OWASP LLM, vector/embedding weaknesses), no relevancia.
- **Plan de costo ordenado por impacto:** (1) **caché semántico por tenant** ataca el 45% directo →
  ~4.950 × 0,55 ≈ **USD ~2.720/hora** solo con esto; se invalida cuando el tenant re-sube/edita docs. (2)
  **ruteo multi-modelo** sobre lo no-cacheado: tareas fáciles → modelo barato (~5x), síntesis larga →
  caro; necesita eval gate para no degradar en silencio.
- **Resiliencia:** chat interactivo → **fallback rápido** (backoff+jitter en 429/5xx → degradar a modelo
  barato → fallar honesto), **NO cola**. Batch nocturno → **cola de inferencia** que respeta la cuota.
- **Triángulo:** sacrificar calidad por costo en las preguntas fáciles (la calidad de un saludo es
  idéntica en barato y caro; Opus ahí solo quema margen).
- **ADR:** aislamiento de tenants (compartido+filtro fail-closed para la mayoría, dedicado para
  regulados).

### Puntos resbalosos / variantes
- Índice-**por-tenant para todos** es aceptable como `competente` si nombra el trade-off de costo
  operacional (40 índices que operar). `excelente` reserva eso para los regulados.
- Confundir caché semántico (elimina la llamada) con prompt caching (abarata la entrada de las llamadas
  que sí haces) es error frecuente.
- Cola en el chat interactivo = error (cambia estabilidad por una latencia que el usuario no tolera).

> Detalle extendido: ver `.ai/soluciones/fase-8/disenar-rag-multitenant-escala.md` (este sistema es el
> mismo ejercicio, pulido a portafolio).

---

## SISTEMA 2 — Automatización de tickets con IA (TriageBot)

### Respuesta canónica (resumen)
- **Número:** ~5.000 tickets/día, pico 2/s → QPS irrelevante. El número que manda: ~10% reembolsos ≈
  **~500 acciones sensibles/día**, todas a HITL ≈ **~500 aprobaciones humanas/día**. Contra una capacidad
  de "cientos/día", está al límite → hay que **reducir el HITL sin volverlo inseguro** (p. ej. auto-aprobar
  reembolsos pequeños bajo un monto-umbral con doble validación de orden, dejando HITL para los grandes).
- **Reparto cerebro/código:** el **LLM propone** una salida estructurada (categoría, monto, acción,
  confianza auto-reportada); un **plano de control determinista dispone**. Orden de chequeos = diseño de
  seguridad:
  1. **Idempotencia** (`ticket_id` ya visto → no re-ejecuta). **Primero, antes que nada de IA.**
  2. **Guardrail de schema** (salida no válida → DLQ + alerta). Schema válido ≠ contenido confiable.
  3. **Techo de costo** (circuit breaker de gasto / Unbounded Consumption).
  4. **Acción sensible** (reembolso) → **HITL obligatorio, sin importar la confianza** (LLM06).
  5. **Confianza** (solo para acciones NO sensibles, y al final): bajo umbral → HITL/escalar.
- **Reglas de negocio encima del schema:** un reembolso solo procede si hay orden real y el monto ≤ monto
  de la orden (defensa contra inyección que pide "reembólsame todo").
- **Eval gate:** mide **tasa de decisión correcta** (routing + extracción) sobre un **golden set sacado
  de trazas reales anotadas**, corre en CI con baseline versionado y **bloquea el deploy** ante regresión.
  No mide fluidez.
- **Observabilidad:** traza por paso (tokens/latencia/costo), `ticket_id` como correlation id; DLQ
  observable.
- **Trade-offs:** (a) umbral de confianza alto → más HITL (más seguro, más carga humana) vs bajo → menos
  HITL (más riesgo). (b) auto-aprobar reembolsos pequeños → menos carga humana vs ventana de fraude
  acotada por el monto-umbral.
- **ADR:** "plano de control determinista en vez de confiar en la decisión del LLM" (o "HITL para todo
  reembolso por encima de X").

### Puntos resbalosos / variantes
- Predecir la ruta de un ticket **duplicado + reembolso**: gana la **idempotencia** (chequeo 1); nunca
  llega al HITL porque ya fue procesado. Quien diga "HITL primero" no entendió el orden.
- Aceptable `competente`: HITL para **todos** los reembolsos (simple, seguro) aunque sature; `excelente`
  reconoce el cuello humano y propone el monto-umbral con validación reforzada.
- Error: usar la confianza del modelo como probabilidad calibrada para auto-ejecutar.

---

## SISTEMA 3 — Pipeline de datos para IA (FreshIndex)

### Respuesta canónica (resumen)
- **Número / frescura:** ~5.000 docs cambian/día; re-embedding **total** de 2M chunks × ~500 tokens ×
  (0,10/1e6) ≈ **~USD 100/corrida** + horas de cómputo → caro y lento para correr seguido. **Ventana de
  frescura propuesta y defendida por fuente:** productos ~minutos (cambian precios, crítico) vía CDC;
  manuales/wiki ~24 h vía batch (casi nunca cambian). El número (costo del rebuild total) contra la
  ventana (minutos para productos) **fuerza** el incremental para la fuente caliente.
- **Arquitectura:** **medallion** — bronze (raw ingerido tal cual) → silver (limpio, deduplicado,
  normalizado) → gold (chunks + metadata listos para embeddear). ELT (cargar crudo y transformar dentro),
  no ETL.
- **Orquestación:** un orquestador **asset-centric** (Dagster) modela cada capa como asset con
  dependencias y frescura; dispara la transformación (dbt) y luego el job de embeddings. Airflow es
  aceptable (task-centric).
- **Frescura, decisión central:** **CDC incremental** (Debezium/Kafka Connect o triggers sobre la base de
  productos) re-embeddea **solo lo que cambió** → fresco en minutos a costo marginal. **Rebuild nocturno**
  solo para fuentes frías o como red de seguridad/reconciliación. No re-embeddear todo cada vez.
- **Data contracts + calidad:** tests de **frescura, volumen y schema drift** (dbt tests / Great
  Expectations); un documento corrupto va a **dead-letter** y no tumba la corrida.
- **Versionado del modelo de embeddings:** vectores de modelos distintos **no son comparables**; al
  cambiar de modelo, re-embedding total **controlado** con **blue/green del índice** (construir el índice
  nuevo en paralelo, cortar el RAG al nuevo cuando esté completo). El RAG nunca consulta un índice mezclado.
- **Trade-offs:** (a) CDC incremental (fresco + barato, más complejidad operacional) vs rebuild nocturno
  (simple, barato de operar, datos hasta 24 h viejos). (b) frescura por minuto para todas las fuentes
  (caro) vs frescura diferenciada por fuente (más barato, requiere clasificar fuentes por criticidad).
- **ADR:** "re-embedding incremental por CDC para la fuente caliente vs rebuild nocturno total".

### Puntos resbalosos / variantes
- El error central es **no definir la ventana de frescura** o tratarla igual para todas las fuentes.
- Olvidar el **versionado del modelo de embeddings** (mezclar vectores de dos modelos en el mismo índice)
  es un bug grave y poco intuitivo: márcalo como diferenciador `excelente` si el alumno lo previó.
- Rebuild nocturno completo **para todo** es aceptable `competente` si nombra el trade-off de frescura
  (datos hasta 24 h viejos) y el costo; `excelente` usa CDC para la fuente crítica.

---

## Rango de soluciones aceptables (los tres)
- No hay una única arquitectura correcta. Se evalúa el **razonamiento**: número mostrado y coherente,
  cuello de botella propio identificado, trade-offs que nombran qué se sacrifica + alternativa descartada,
  y ADRs de tres partes.
- Los números exactos varían con los supuestos **declarados**; se exige la **aritmética mostrada y
  coherente**, no que dé exactamente USD 4.950 o USD 100.
- Un alumno que llega a decisiones distintas pero las defiende con número/trade-off está `competente` o
  `excelente`, no penalizado. Uno que repite el vocabulario sin los números específicos de cada spec, o
  cuyos ADRs no nombran alternativa descartada, está `en-progreso`.
- **Capstone completo `excelente`:** los tres sistemas con su cuello de botella propio explícito, números
  que priorizan decisiones, seguridad tratada como tal (fail-closed / HITL / data contracts), eval y
  observabilidad ubicadas, y la capacidad demostrada de **defenderlo sin notas** y aplicar el método a un
  sistema nuevo.
