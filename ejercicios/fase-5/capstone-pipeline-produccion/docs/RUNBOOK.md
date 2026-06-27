# RUNBOOK — operación de <tu proyecto>

> El documento que tu "yo de las 3am" agradecerá. Concreto, paso a paso, sin suponer contexto.
> Borra las pistas y completa.

## Desplegar
<!-- TODO: comando(s) o "merge a main dispara deploy.yml". Cómo confirmas que quedó arriba. -->

## Rollback
<!-- TODO: pasos exactos para volver a la versión anterior. Qué tag/digest. Cuánto tarda. Cómo verificas. -->

## Salud y observabilidad
<!-- TODO: URL de /health. Dónde miras logs estructurados y trazas. Cómo buscas por correlation ID. -->

## Diagnóstico de incidentes comunes
<!-- TODO: "usuario reporta 500" → busca el correlation ID → sigue la traza → ...
     "el servicio no responde" → revisa HEALTHCHECK / proxy / cert ... -->

## Secretos y rotación
<!-- TODO: dónde viven, cómo rotarlos sin downtime. -->

## Contactos / dependencias externas
<!-- TODO: proveedor de DB, DNS, registry, etc. -->
