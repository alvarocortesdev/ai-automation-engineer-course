# Sistema 1 — "AskDocs" (RAG multi-tenant B2B)

> Diséñalo **en papel**: diagrama + decisiones + ADR. Trabájalo a mano, sin IA, dentro del timebox.
> Si ya hiciste el ejercicio `disenar-rag-multitenant-escala` de 8.5, aquí **pules** ese diseño a
> calidad de portafolio (no lo rehaces de cero).

## Qué es

AskDocs es un SaaS B2B. Cada empresa-cliente (**tenant**) sube sus documentos internos (políticas de
RRHH, manuales, contratos) y sus empleados preguntan en lenguaje natural por un chat web. El sistema
recupera los fragmentos relevantes **de los documentos de ese tenant** y responde con un LLM.

## Números (los que importan para el diseño)

- **Tenants:** 40 empresas, de tamaños dispares (de 10 a 2.000 empleados). 3 de ellas están **reguladas**
  (banca/salud) y exigen aislamiento estricto.
- **Tráfico:** pico de **50 preguntas por segundo** en total (sumando todos los tenants), muy desigual a
  lo largo del día (picos al almuerzo y al cierre).
- **Patrón de preguntas:** ~**45%** de las preguntas de un tenant son semánticamente repetidas dentro de
  ese tenant ("¿cómo pido vacaciones?").
- **Por pregunta (peor caso):** 1 embedding de la query + 1 búsqueda vectorial + 1 generación.
- **Generación:** ~2 s de latencia, ~3.000 tokens de entrada (contexto + prompt) y ~500 de salida.
- **Tarifas (ilustrativas):** modelo **caro** USD 5 / millón de tokens de entrada, USD 25 / millón de
  salida. Modelo **barato** USD 1 / millón entrada, USD 5 / millón salida.
- **Cuota del proveedor:** límite de tokens por minuto compartido por toda la cuenta; un pico lo agota y
  el proveedor responde 429.

## Restricciones de negocio

- Los documentos de un tenant **no pueden** filtrarse a otro tenant **bajo ninguna circunstancia**
  (incidente de seguridad grave; hay clientes regulados). **Este es el "nunca" del sistema.**
- El chat es **interactivo**: el usuario espera mirando la pantalla. Más de unos pocos segundos es
  inaceptable.
- Hay un flujo **batch** secundario: resúmenes nocturnos de documentos nuevos, que NO son interactivos.
- Los documentos cambian: un tenant puede re-subir o editar en cualquier momento.

## Pistas de qué decisiones esperar (no las respuestas)

Aislamiento de tenants (índice-por-tenant vs compartido-con-filtro), caché semántico por tenant, ruteo
multi-modelo, cola de inferencia vs fallback rápido (interactivo vs batch), y **una** decisión consciente
del triángulo latencia/costo/calidad. El **cuello de botella propio**: la cuota de tokens y el costo.
