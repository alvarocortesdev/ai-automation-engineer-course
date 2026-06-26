# ADR-0001 — Arquitectura ports & adapters (hexagonal light)

- Estado: aceptada
- Fecha: <YYYY-MM-DD>

> Plantilla. Reemplaza los `<...>` con tu razonamiento real. Un ADR no es burocracia: es la decisión
> que tu yo de la Fase 6 va a agradecer (o pagar). Justifica una decisión técnica de verdad.

## Contexto

Estoy construyendo una API REST que en la Fase 6 voy a extender con un pipeline RAG sobre los mismos
documentos, y en la Fase 4 con un frontend que la consume. Necesito que esa extensión no me obligue a
reescribir la lógica de negocio, y quiero poder testear el dominio sin levantar PostgreSQL.

## Decisión

Organizo el código en ports & adapters *light*:

- **Núcleo (dominio + casos de uso):** entidades y reglas de negocio. **No importa** `fastapi` ni
  `sqlalchemy`. Define **puertos** como interfaces: `<RepositorioRecurso>`, `<ClienteHTTP>`, `<Reloj>`.
- **Adapters de entrada:** routers FastAPI que traducen HTTP a llamadas a casos de uso.
- **Adapters de salida:** repos SQLAlchemy (Postgres) y cliente httpx (con guardia SSRF) que
  *implementan* los puertos. Se inyectan con `Depends`.

## Alternativas consideradas

- **CRUD acoplado (router llama directo a SQLAlchemy):** más rápido de escribir hoy. Lo descarto porque
  en F6 el indexador RAG y los tests del dominio quedarían atados a HTTP y a la base de datos. El costo de
  acoplar se paga tres fases después.
- **Hexagonal "completo" con CQRS / event sourcing:** sobre-ingeniería para el tamaño de este proyecto.
  Lo descarto por YAGNI; lo reconsideraría si el dominio creciera.

## Consecuencias

- (+) El RAG de F6 entra como un adapter más (un `Indexador` que implementa un puerto) sin tocar el dominio.
- (+) Los tests de dominio corren sin Postgres (uso un repo en memoria que implementa el mismo puerto).
- (+) El frontend de F4 programa contra un contrato (OpenAPI + RFC 9457) estable.
- (−) Más archivos y una capa de indirección desde el día 1. Lo acepto: la legibilidad del límite vale más
  que el ahorro inicial.
