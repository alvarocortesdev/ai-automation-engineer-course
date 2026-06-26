---
ejercicio_id: fase-3/graphql-rest-decidir
fase: fase-3
sub_unidad: "3.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio **no tiene respuesta única**: lo que sigue son las decisiones más defendibles y los criterios para juzgar otras.

# Solución de referencia — Decide: REST o GraphQL

## Principio rector para corregir

No corrijas *qué* estilo eligió, corrige *cómo* lo justificó. El criterio que más pesa, casi siempre, es **cuántos clientes distintos consumen la API y cuán distintas son sus necesidades de datos**. Un cliente único y estable rara vez justifica el costo de GraphQL; muchos clientes heterogéneos pidiendo formas distintas es donde GraphQL paga. El segundo eje: **cuánto te duele el over/under-fetching real** (el móvil con red mala lo sufre más). Una elección "contraria a la esperada" bien argumentada con trade-offs vale más que la "esperada" con un eslogan.

## Decisiones defendibles por escenario

### Escenario A — SPA contra su propio backend
- **Elección esperada: REST.**
- **Criterios:** un solo cliente, estable, mismo equipo a ambos lados. El over/under-fetching es manejable con buenos endpoints. Ganas **gratis** el caching HTTP del navegador/CDN (los `GET` se cachean por URL) y las métricas por ruta. GraphQL aquí añade complejidad (un solo endpoint, autorización por campo, límites de query) por un beneficio marginal.
- **Costo a nombrar:** si las pantallas crecen y se vuelven heterogéneas, podrías terminar con algo de over-fetching o con una segunda llamada por pantalla.
- **Dato que cambia la decisión:** que aparezcan varios clientes (móvil, partners) con necesidades de datos muy distintas.

### Escenario B — Web + móvil + partners externos
- **Elección esperada: GraphQL.**
- **Criterios:** **tres** clientes heterogéneos pidiendo formas distintas de los mismos datos + un backend que ya vive creando endpoints a medida (`/productos-para-movil`, ...). GraphQL deja que cada cliente arme su query sin multiplicar endpoints; el móvil con red mala pide el payload mínimo (mata el over-fetching donde más duele). Aquí la flexibilidad de consulta paga su costo.
- **Costo a nombrar:** pierdes el caching por URL (todo es `POST /graphql`), debes autorizar **por campo**, limitar profundidad/complejidad de las queries (DoS / Unbounded Consumption) y montar observabilidad a nivel de campo.
- **Dato que cambia la decisión:** que los tres clientes en realidad necesitaran formas casi idénticas y el caching HTTP importara mucho → REST volvería a ganar.
- **Tensión (nivel excelente):** reconocer que REST con endpoints bien pensados (o REST + un BFF por cliente) **también** podría servir; la apuesta por GraphQL es por no multiplicar endpoints a medida a escala, no por imposibilidad de REST.

### Escenario C — Microservicio de webhooks
- **Elección esperada: REST** (o ni siquiera eso: un endpoint plano que recibe el `POST`).
- **Criterios:** no hay un cliente que **elija** campos; lo "consume" otra máquina con un contrato fijo. 3 endpoints que no cambian. GraphQL no aporta un solo beneficio y suma complejidad inútil.
- **Costo a nombrar:** ninguno relevante; REST es lo correcto. (Si el alumno fuerza GraphQL aquí, es la señal #1 de decidir por moda.)
- **Dato que cambia la decisión:** prácticamente ninguno realista; quizá si el "webhook" evolucionara a una API de consulta rica con muchos clientes.

## Qué hace que una entrega sea "competente" vs "excelente"
- **Competente:** las tres decisiones se apoyan en heterogeneidad de clientes + over/under-fetching real y nombran un costo por escenario (A→REST, B→GraphQL, C→REST).
- **Excelente:** además expone la tensión del escenario ambiguo (típicamente B, o A si la SPA crece), no finge que todo es obvio, y los costos/datos-que-cambian son específicos (no genéricos como "tiene curva").

## Errores a marcar (resumen)
- Decidir por moda ("GraphQL es más moderno") o simplismo ("REST es más fácil") sin atarlo al contexto.
- GraphQL para el webhook (overkill, sin cliente que elija campos).
- GraphQL para la SPA única sin reconocer la pérdida de caching HTTP.
- Vender una opción como perfecta (sin costo).
- No reconocer ninguna ambigüedad en los tres.

## Variante de control anti-IA
Pedir el **contrafactual** del escenario B: "¿qué tendría que ser verdad para que REST siguiera ganando con 3 clientes distintos?". Respuesta razonada esperada: que las tres formas de datos fueran casi iguales y el caching HTTP importara mucho (entonces el costo de GraphQL no se paga). Quien copió una comparativa genérica no puede construir el contrafactual.
