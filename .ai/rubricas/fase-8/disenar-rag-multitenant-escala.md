---
ejercicio_id: fase-8/disenar-rag-multitenant-escala
fase: fase-8
sub_unidad: "8.5"
version: 1
---

# Rúbrica — Diseña un RAG multi-tenant para escala y costo

> Rúbrica **analítica** para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio
> de arquitectura** (números, trade-offs, aislamiento, decisión del triángulo), no si el diagrama es
> idéntico a la solución de referencia. Hay varias arquitecturas defendibles; lo que las separa de un
> diseño copiado es que cada caja tiene un número o un trade-off detrás.

## Objetivos evaluados
- **O1** — Diseñar la arquitectura para escala y costo (aislamiento, caché semántico, ruteo, cola,
  fallback).
- **O2** — Estimar el costo por hora con cálculo de servilleta y priorizar con él.
- **O3** — Defender una decisión del triángulo con un trade-off explícito, en un ADR.

## Criterios y niveles

### C1 — Estimación de costo (¿hay un número, y manda?) · mapea: O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay cálculo de costo, o el diseño no se apoya en ningún número. |
| **en-progreso** | Da un costo, pero la aritmética no se muestra o es incoherente (mezcla tarifas de entrada/salida, olvida el QPS o el factor 3600). |
| **competente** | Muestra la aritmética por pregunta (entrada×tarifa + salida×tarifa) y la escala a costo/hora con el QPS; el número es coherente (orden de magnitud ~USD miles/hora). |
| **excelente** | Usa el número para **priorizar**: ordena las intervenciones por impacto sobre ese costo (p. ej. "el caché ataca el 45% directamente, va primero"). |

### C2 — Aislamiento de tenants (seguridad, no solo relevancia) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No aborda el aislamiento, o propone mezclar índices sin filtro. |
| **en-progreso** | Menciona un `WHERE tenant_id = ?` pero como filtro **opcional**, sin reconocer el riesgo de fuga ni cómo blindarlo. |
| **competente** | Elige índice-compartido-con-filtro (o índice-por-tenant) **nombrando el trade-off** aislamiento vs costo operacional, y trata el filtro como **obligatorio**. |
| **excelente** | Blinda el filtro de verdad (parte de la firma, fail-closed, test que intenta consultar sin filtro y debe fallar) y lo enmarca como **seguridad / OWASP LLM / vector weaknesses**, no solo relevancia; reconsidera índice-por-tenant para tenants regulados. |

### C3 — Plan de costo: caché semántico + ruteo · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No propone caché ni ruteo, o "usa siempre el mejor modelo". |
| **en-progreso** | Propone una de las dos sin ahorro estimado ni trade-off. |
| **competente** | Propone caché semántico **y** ruteo multi-modelo, cada uno con ahorro estimado (usa el 45% / las dos tarifas) y un trade-off (obsolescencia, calidad en tareas fáciles). |
| **excelente** | Distingue caché semántico de prompt caching, hace la caché **por tenant e invalidable**, y nota que el ruteo necesita un eval gate para no degradar calidad en silencio. |

### C4 — Resiliencia (cola vs fallback, interactivo vs batch) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No aborda picos/429, o pone una cola en el chat interactivo sin notar el problema. |
| **en-progreso** | Menciona cola **o** fallback, pero sin distinguir interactivo de batch. |
| **competente** | Ubica la **cola** en el flujo batch (resúmenes) y el **fallback** rápido en el chat, justificando con la latencia tolerable de cada uno. |
| **excelente** | Detalla el fallback chain (backoff+jitter → degradar a modelo barato → fallar honesto), reintenta solo en 429/5xx, y conecta con idempotencia/resiliencia de 3.14. |

### C5 — Decisión del triángulo + ADR (juicio) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No señala ninguna decisión consciente del triángulo, o el ADR falta / no tiene las tres partes. |
| **en-progreso** | Señala una decisión pero sin nombrar qué sacrifica; el ADR es vago. |
| **competente** | Nombra un punto donde sacrifica calidad por costo (o latencia por estabilidad) **con su porqué de negocio**, y el ADR tiene Contexto/Decisión/Consecuencias. |
| **excelente** | El ADR nombra la **alternativa descartada** y la **consecuencia negativa aceptada**; la decisión del triángulo es defendible contra la opción contraria. |

## Errores típicos a marcar
- **Diagrama sin números:** cajas bonitas sin un solo cálculo de costo detrás (el error #1 de esta fase).
- **"Usa siempre el mejor modelo":** ignora el ruteo; quema costo donde la calidad no cambia.
- **Filtro `tenant_id` opcional:** lo trata como relevancia, no como seguridad; no blinda contra fugas.
- **Cola en el chat interactivo:** cambia estabilidad por una latencia que el usuario no tolera.
- **Confundir caché semántico con prompt caching:** dice que el caché "abarata" la llamada (eso es
  prompt caching) cuando el semántico la **elimina**, o viceversa.
- **Fallback que reintenta en 400** o que "degrada" hacia un modelo más caro.
- (transversal) **Cambiar de modelo sin eval gate** ni traza de costo: ahorro celebrado a ciegas.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diagrama exhaustivo y vocabulario impecable, pero **sin el cálculo de costo** o con un número que no
  cuadra cuando se le pide rehacerlo a mano.
- Las 6 secciones presentes con prosa genérica intercambiable, sin los números específicos de DocsAI
  (45%, 50 QPS, las dos tarifas).
- ADR que enumera "consecuencias" sin nombrar la alternativa descartada ni el costo aceptado.
- **Verificación sugerida:** pídele que cambie un número de la spec (p. ej. 40 → 4 tenants regulados de
  banca) y rehaga la decisión de aislamiento. Si razonó, cambia a índice-por-tenant y lo justifica; si
  dependió de la IA, repite el mismo diseño.

## Feedback sugerido (graduado)
> Nunca dar el diseño antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Empieza por el número. ¿Cuánto cuesta una hora si todas las 50 preguntas/s van
  al modelo caro y nada se cachea? Sin ese número no sabes qué intervención priorizar."
- **Pregunta socrática (nivel 2):** "Tu filtro `tenant_id`, ¿qué pasa si un día alguien llama a la
  función de retrieval y se le olvida pasarlo? Si la respuesta es 'fuga de datos entre clientes',
  ¿cómo haces que eso sea **imposible** y no solo improbable?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa que cada caja del diagrama tenga un
  número o un trade-off detrás. Y en el ADR, nombra explícitamente qué alternativa descartaste y qué
  consecuencia negativa aceptas: sin eso no es una decisión, es una preferencia."

## Conexión con el proyecto / capstone
- Es el músculo exacto del [capstone F8](/fase-8-system-design/proyecto/): el primer sistema en papel es
  un RAG multi-tenant, y este ejercicio entrena su diseño completo (número → aislamiento → costo →
  resiliencia → ADR). El segundo sistema (tickets con IA) es una variante del mismo método.
