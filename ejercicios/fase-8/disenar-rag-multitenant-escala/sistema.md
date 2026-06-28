# Especificación del sistema — "DocsAI" (RAG multi-tenant B2B)

> Esta es la especificación que recibes como arquitecto. Tu trabajo NO es construir el sistema, sino
> **diseñarlo en papel** (diagrama + decisiones + ADR). Trabájalo a mano, sin IA, dentro del timebox.

## Qué es

DocsAI es un SaaS B2B. Cada empresa-cliente (**tenant**) sube sus propios documentos internos
(políticas de RRHH, manuales, contratos) y sus empleados hacen preguntas en lenguaje natural vía un
chat web. El sistema recupera los fragmentos relevantes **de los documentos de ese tenant** y genera
una respuesta con un LLM.

## Números (los que importan para el diseño)

- **Tenants:** 40 empresas, de tamaños dispares (desde 10 hasta 2.000 empleados).
- **Tráfico:** pico de **50 preguntas por segundo** en total (sumando todos los tenants). El tráfico es
  muy desigual a lo largo del día (picos a la hora de almuerzo y al cierre).
- **Patrón de preguntas:** se estima que ~**45%** de las preguntas de un tenant son semánticamente
  repetidas dentro de ese tenant ("¿cómo pido vacaciones?", "¿cuál es la política de gastos?").
- **Por pregunta (peor caso):** 1 embedding de la query + 1 búsqueda vectorial + 1 generación.
- **Generación:** ~2 s de latencia, ~3.000 tokens de entrada (contexto recuperado + prompt) y ~500
  tokens de salida.
- **Tarifa del modelo caro (tier-Opus):** USD 5 / millón de tokens de entrada, USD 25 / millón de
  salida.
- **Tarifa del modelo barato (tier-Haiku):** USD 1 / millón de entrada, USD 5 / millón de salida.
- **Cuota del proveedor del LLM:** límite de tokens por minuto compartido por toda la cuenta (no es
  infinito; un pico lo puede agotar y el proveedor responde 429).

## Restricciones de negocio

- Los documentos de un tenant **no pueden** filtrarse a otro tenant bajo ninguna circunstancia (es un
  incidente de seguridad grave; varios clientes están regulados).
- El chat es **interactivo**: el usuario espera la respuesta mirando la pantalla. Una espera de más de
  unos pocos segundos es inaceptable.
- También hay un flujo **batch** secundario: resúmenes nocturnos de documentos nuevos, que NO son
  interactivos.
- Los documentos cambian: un tenant puede re-subir o editar sus documentos en cualquier momento.

## Qué entregar

Lee el `README.md` de esta carpeta para el detalle de las 6 secciones que debe tener tu `diseno.md`.
