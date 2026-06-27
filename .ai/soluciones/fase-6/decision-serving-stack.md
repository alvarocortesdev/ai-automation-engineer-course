---
ejercicio_id: fase-6/decision-serving-stack
fase: fase-6
sub_unidad: "6.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir** de un ejercicio de diseño: hay varias respuestas defendibles. Úsala para juzgar
> la **calidad del trade-off**, no para exigir coincidencia literal.

# Solución de referencia — Decisión: stack de serving para tres escenarios

> Estas son respuestas **canónicas y defendibles**, no las únicas. Lo que importa es que la
> decisión **se derive de la restricción dominante** y que el motor/cuantización tengan un
> porqué.

## Escenario 1 — Asistente de código en la laptop de un dev

- **Restricción dominante:** privacidad (código propietario) + single-user. No es el costo.
- **Local o API:** **local** — los datos no deben salir y lo usa una sola persona.
- **Motor:** **MLX** (Mac, aprovecha la memoria unificada del chip M) u **Ollama** (cero
  fricción, portable). Ambos son **single-user**, perfectos para uso intermitente de uno.
- **Cuantización:** **GGUF** (Ollama) o el formato MLX cuantizado (repos `mlx-community`,
  p. ej. 8 bits). Corre en CPU/GPU integrada del Mac, no en una GPU NVIDIA → GGUF/MLX, no
  AWQ. A 8 bits casi no se pierde calidad; a 4 bits es un trade-off razonable para un Mac
  con menos RAM.
- **Mecanismo clave:** N/A — no hay concurrencia, no se necesita continuous batching.
- **Privacidad/seguridad:** el código no sale de la máquina (bien), pero ojo con los logs
  locales del runtime y con extensiones del editor que podrían reenviar contexto. Mitigación:
  revisar qué loguea Ollama/MLX y no encadenar el local con una tool en la nube.

Modelo razonable: **Qwen2.5-Coder** (SOTA abierto para código, corre cómodo en un Mac de
32–64 GB).

## Escenario 2 — Chatbot interno para 500 empleados, on-prem

- **Restricción dominante:** privacidad/cumplimiento **legal** (los datos no pueden salir).
  La concurrencia alta (500) es la segunda restricción.
- **Local o API:** **local / on-prem** — la API queda descartada por **ley**, no por costo.
- **Motor:** **vLLM** (o **TGI**) en las GPUs del datacenter. Ollama/MLX servirían un stream
  a la vez y el usuario 500 esperaría su turno; vLLM está hecho para concurrencia.
- **Cuantización:** **AWQ** (GPU-native, se integra con el continuous batching de vLLM) o
  FP8 si la GPU lo soporta. Permite que el modelo quepa y deja más memoria para el KV cache
  (= más requests concurrentes). GGUF aquí sería un error: vLLM no lo carga.
- **Mecanismo clave:** **KV cache** evita recomputar la atención token a token (a cambio de
  ocupar memoria de GPU, que es el recurso que limita la concurrencia) y **continuous
  batching** mantiene la GPU siempre llena (cuando un request termina, entra otro), lo que
  dispara el **throughput** para servir a muchos. Trade-off: subir el batch sube el
  throughput pero puede subir la latencia por request → se tunea contra un techo de latencia.
- **Privacidad/seguridad:** local **habilita** la privacidad pero no la garantiza: hay que
  añadir control de acceso por empleado, cifrado en tránsito/reposo, retención mínima de
  logs (los prompts pueden traer PII) y cuidado con el KV cache en memoria. Enlaza con 6.14.

## Escenario 3 — Feature de IA en una startup que recién valida

- **Restricción dominante:** **costo + velocidad de salida** a volumen bajo/variable y sin
  equipo de ops.
- **Local o API:** **API** — a 100 usuarios con tráfico variable, una GPU dedicada estaría
  casi siempre ociosa y se paga igual (costo fijo). La API por token es ínfima a ese volumen
  y elimina toda la operación. Local ganaría solo a volumen alto y sostenido (mira el punto
  de equilibrio del otro ejercicio).
- **Motor:** **N/A** (API gestionada). Si más adelante el volumen crece y se sostiene, o
  aparece un requisito de privacidad, se reevalúa migrar a vLLM.
- **Cuantización:** N/A (la maneja el proveedor de la API).
- **Mecanismo clave:** N/A.
- **Privacidad/seguridad:** los datos sí salen a un tercero → revisar la política de
  retención del proveedor y no mandar PII innecesaria; segregar contenido no confiable del
  usuario (enlaza con 6.2/6.14). Mitigación: minimizar lo que se envía y elegir un proveedor
  con retención cero si el dato es sensible.

## Cómo juzgar (para el corrector)

- **Lo esencial:** que cada escenario **derive** la decisión de su restricción y que E2 use
  un motor de producción **con** mención de KV cache/continuous batching. Si propuso Ollama
  para 500 usuarios, es el error central del ejercicio.
- **Respuestas alternativas válidas:** TGI en vez de vLLM en E2; Ollama en vez de MLX en E1;
  en E3, empezar con API y declarar explícitamente el disparador de migración a local. Todas
  defendibles si la justificación es sólida.
- **Excelente:** separa el eje legal (E2) del eje costo (E3), nombra el trade-off throughput
  vs latencia, y reconoce que "local no es automáticamente privado".
- **No exigir** números exactos de pricing ni versiones de herramientas; este ejercicio es
  de criterio, no de memoria de comandos.
