# Ejercicio 3.11b — Decide: REST o GraphQL para tres escenarios

> **Modalidad: razonamiento (sin código, sin IA).** No se ejecuta nada. Eliges REST o GraphQL para tres escenarios y **defiendes** la elección con criterios concretos y trade-offs. Se evalúa la **calidad del criterio**, no qué elegiste.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.11` GraphQL: nociones
**Ruta:** opcional / profundización · **Timebox:** 30–35 min

## 🎯 Objetivo

Decidir, para cada uno de tres escenarios, entre **REST** y **GraphQL**, justificando con criterios reales (cuántos clientes distintos consumen la API y cuán distintas son sus necesidades de datos; cuánto importa el caching HTTP; complejidad del equipo/servidor; si hay over/under-fetching que duela de verdad) y nombrando el **costo** de cada elección.

## 📋 Contexto

"¿REST o GraphQL?" es un **ADR** real del capstone de la fase y una pregunta de entrevista de diseño clásica. El error de junior es decidir por moda ("GraphQL es más moderno") o por simplismo ("REST es más fácil"). El semi-senior decide por **contexto** y sabe nombrar lo que pierde con su elección. Este ejercicio entrena justo eso.

## 📏 Primero-Sin-IA

1. Decide y argumenta **solo**, a mano (timebox arriba).
2. Solo entonces, consulta documentación oficial si necesitas confirmar una característica.
3. **Solo al final**, usa IA para *cuestionar* tu razonamiento (pídele que defienda la opción contraria) — no para que decida por ti.
4. Mañana, reescribe de memoria los dos criterios que más pesan al elegir entre REST y GraphQL.

## 🧩 Los tres escenarios

**Escenario A — SPA contra su propio backend.**
Una aplicación web de página única (React) que consume **su propio** backend, mantenido por el mismo equipo de 3 personas. Un solo cliente, endpoints estables, datos que cambian poco de forma. Quieren aprovechar el caching del navegador/CDN y tener métricas claras por endpoint.

**Escenario B — API consumida por web + móvil + partners externos.**
Una empresa expone los mismos datos (productos, pedidos, usuarios) a **tres** consumidores muy distintos: una web rica, una app móvil con red mala que necesita payloads mínimos, y partners externos que arman integraciones impredecibles. Cada uno quiere una **forma distinta** de los mismos datos, y hoy el equipo backend vive creando endpoints a medida (`/productos-para-movil`, `/productos-con-stock`, ...).

**Escenario C — Microservicio de webhooks.**
Un servicio que recibe webhooks de un proveedor de pagos, valida una firma, escribe en una cola y responde 200. No lo consume ningún frontend; lo "consume" otra máquina. Tres endpoints como mucho, sin necesidad de elegir campos.

## 🛠️ Instrucciones

Crea un archivo **`DECISION.md`**. Para **cada** escenario (A, B, C):

1. **Elige** REST o GraphQL.
2. **Justifica** con al menos dos criterios concretos (número y heterogeneidad de clientes, caching HTTP, over/under-fetching real, complejidad que estás dispuesto a pagar en el servidor).
3. **Nombra un costo o riesgo** real de tu elección (ninguna es gratis).
4. **Di qué dato adicional** te haría cambiar de opinión.

Cierra con un párrafo: **¿cuál es el criterio que, casi siempre, inclina la decisión?** (pista: tiene que ver con cuántos clientes distintos piden formas distintas de los mismos datos).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las tres decisiones están justificadas con criterios concretos, no con eslóganes ("más moderno", "más simple", "lo que se usa").
- [ ] Reconoces al menos un escenario donde la elección **no** es obvia y explicas la tensión.
- [ ] Cada elección nombra un costo real (GraphQL: caching, autorización por campo, observabilidad, riesgo de DoS por queries no acotadas; REST: over/under-fetching, round trips, proliferación de endpoints a medida).
- [ ] Puedes defender, sin notas, por qué en A **REST** suele ganar y por qué en B **GraphQL** empieza a pagar su costo.
- [ ] El párrafo de cierre identifica la heterogeneidad de clientes/necesidades de datos como el criterio dominante.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **A (SPA + su backend):** un solo cliente estable rara vez justifica el costo de GraphQL; REST con buenos endpoints alcanza y te quedas el caching HTTP y las métricas por ruta gratis. Costo a nombrar: si la pantalla crece, podrías terminar con algo de over-fetching o una segunda llamada.
- **B (web + móvil + partners):** muchos clientes heterogéneos pidiendo formas distintas = donde GraphQL paga su costo; cada cliente arma su query sin que el backend multiplique endpoints, y el móvil con red mala se beneficia de pedir el payload mínimo. Costo: pierdes el caching por URL, debes autorizar por campo, limitar profundidad/complejidad (DoS) y montar observabilidad por campo.
- **C (webhook):** ni siquiera hay un cliente que elija campos; REST (o ni eso, un endpoint plano) es lo correcto. GraphQL sería overkill sin un solo beneficio.

El eje dominante: **cuántos clientes distintos piden formas distintas de los mismos datos**. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu `DECISION.md`, la **rúbrica** (`.ai/rubricas/fase-3/graphql-rest-decidir.md`) y las instrucciones (`.ai/INSTRUCCIONES-CORRECTOR.md`). La **solución de referencia** vive en `.ai/soluciones/fase-3/graphql-rest-decidir.md` — no la mires antes de intentarlo.
