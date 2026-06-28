---
ejercicio_id: fase-8/disenar-rag-multitenant-escala
fase: fase-8
sub_unidad: "8.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir. Hay
> varias arquitecturas defendibles; lo que importa es que cada caja tenga un número o un trade-off
> detrás, no que el diagrama coincida con este.

# Solución de referencia — Diseña un RAG multi-tenant para escala y costo

## Sección 1 — Números primero

Por pregunta, peor caso (todo al modelo caro tier-Opus, USD 5/M entrada, USD 25/M salida):
- Entrada: 3.000 tokens × (5 / 1.000.000) = USD 0,015
- Salida: 500 tokens × (25 / 1.000.000) = USD 0,0125
- **Total por pregunta ≈ USD 0,0275**

A 50 QPS, sin caché:
- Por segundo: 50 × 0,0275 = **USD 1,375/s**
- Por hora: 1,375 × 3.600 ≈ **USD 4.950/hora**

Ese número manda el resto del diseño. La prioridad es bajarlo sin tocar la calidad donde importa.

## Sección 2 — Aislamiento de tenants

**Decisión: índice vectorial compartido con filtro `tenant_id` OBLIGATORIO** (con la salvedad de abajo).

- **Trade-off:** aislamiento vs costo operacional. Índice-por-tenant da aislamiento físico (blast radius
  = 1 cliente) pero 40 índices que operar y escalar; índice compartido es más barato y simple pero el
  aislamiento depende del filtro.
- **Blindaje del filtro (lo no-negociable):** el `tenant_id` no es un parámetro opcional de la función
  de retrieval — es parte de su **firma**, no se puede llamar sin él. La capa de acceso a la vector DB
  rechaza (fail-closed) cualquier query sin `tenant_id`. Hay un **test** que intenta consultar sin
  filtro y debe fallar. Es **seguridad** (OWASP LLM, vector/embedding weaknesses), no relevancia: una
  fuga cruzada es un incidente grave con clientes regulados.
- **Salvedad excelente:** para los pocos tenants grandes y regulados (banca/salud), reconsiderar
  índice-por-tenant para esos específicamente — un modelo híbrido es defendible.

## Sección 3 — Plan de costo ordenado por impacto

1. **Caché semántico (ataca el 45% directo) → va primero.** Guarda respuestas indexadas por el
   embedding de la pregunta, **por tenant**. Ante una pregunta con similitud coseno ≥ 0,95 a una previa
   del mismo tenant, devuelve la cacheada **sin llamar al LLM**. Captura el ~45% de repetidas →
   ~USD 4.950 × 0,55 ≈ **USD 2.720/hora** solo con esto.
   - *Trade-off:* puede servir una respuesta levemente obsoleta → la caché es **por tenant** y se
     **invalida** cuando ese tenant re-sube/edita documentos. Distinto de prompt caching: el semántico
     **elimina** la llamada; el prompt caching **abarata** la entrada de las llamadas que sí haces.
2. **Ruteo multi-modelo (sobre lo que queda).** Clasificaciones, saludos y extracciones simples →
   modelo barato (tier-Haiku, ~5x más barato). Solo la síntesis larga sobre varios documentos → el
   caro. Si, digamos, el 30% del tráfico no-cacheado es "fácil", ese 30% pasa de USD 0,0275 a
   ~USD 0,006 por pregunta.
   - *Trade-off:* calidad en las tareas fáciles (mínima) y necesita un **eval gate** para confirmar que
     el barato no degrada en silencio.

## Sección 4 — Resiliencia bajo pico

- **Chat interactivo → fallback rápido, NO cola.** El usuario espera mirando la pantalla; una cola larga
  es veneno. Cadena: primario → backoff+jitter (1–2 intentos ante 429/5xx) → degradar a modelo barato →
  fallar con mensaje honesto. Degradar la calidad es mejor que caerse.
- **Batch nocturno (resúmenes) → cola de inferencia.** No es interactivo: una cola con workers que
  respetan la cuota de tokens convierte un pico en latencia tolerable y protege contra el 429. Aquí sí
  cambias latencia por estabilidad, y está bien porque nadie espera en vivo.

## Sección 5 — Decisión del triángulo

Ejemplo defendible: **sacrifico calidad por costo en las preguntas "fáciles"** mandándolas al modelo
barato. Por qué es correcto para DocsAI: la calidad de una clasificación o un saludo es idéntica en
Haiku y Opus, pero Opus cuesta ~5x; gastar el modelo caro ahí no compra calidad, solo quema margen. La
calidad alta se reserva para la síntesis larga, donde sí mueve la aguja. (Alternativa igualmente válida:
sacrificar **latencia por estabilidad** encolando el batch nocturno.)

## Sección 6 — Diagrama + ADR

Diagrama (esquema): `Usuario → API (correlation ID) → rate limit por tenant → ¿hit caché semántico
(mismo tenant)? → [sí] respuesta : [no] embedding → vector DB (filtro tenant_id obligatorio) →
retrieval+rerank → router → {barato | caro+fallback} → respuesta (stream) → guarda en caché`. Batch:
`documentos nuevos → cola → workers (respetan cuota) → resúmenes`. Observabilidad: tokens/latencia/costo
por paso + eval gate.

**ADR — Aislamiento de tenants en la vector DB**
- **Contexto:** 40 tenants comparten infraestructura; los documentos no pueden filtrarse entre clientes;
  algunos están regulados.
- **Decisión:** índice vectorial compartido con filtro `tenant_id` obligatorio y fail-closed en la capa
  de acceso; índice dedicado para los tenants regulados.
- **Consecuencias:** (+) costo operacional bajo para la mayoría; (+) blast radius acotado para los
  regulados; (−) **alternativa descartada:** índice-por-tenant para todos (más aislamiento, mucho más
  costo operacional); (−) **costo aceptado:** la seguridad del caso compartido depende de que el filtro
  fail-closed y su test no se rompan nunca — se cubre con CI y un caso negativo obligatorio.

## Rango de soluciones aceptables
- Índice-por-tenant para **todos** es aceptable como `competente` si nombra el trade-off de costo
  operacional; `excelente` reserva esa decisión para tenants regulados.
- En la sección 5 cualquiera de las dos decisiones (calidad↔costo o latencia↔estabilidad) cuenta como
  `excelente` si nombra qué sacrifica y por qué. La decisión concreta no fija el nivel; el razonamiento sí.
- Los números exactos pueden variar con supuestos declarados; lo que se exige es la **aritmética
  mostrada y coherente**, no que dé exactamente USD 4.950.
