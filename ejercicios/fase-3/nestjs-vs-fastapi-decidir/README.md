# Ejercicio 3.10b — Decide: FastAPI, NestJS o Express

> **Modalidad: razonamiento (sin código, sin IA).** No se ejecuta nada. Eliges un framework de backend para tres proyectos y **defiendes** la elección con criterios concretos y trade-offs. Lo que se evalúa es la **calidad del criterio**, no qué framework elegiste.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.10` Backend con Node.js + NestJS
**Ruta:** opcional / profundización · **Timebox:** 30–35 min

## 🎯 Objetivo

Decidir, para cada uno de tres escenarios, entre **FastAPI** (Python), **NestJS** (Node/TS estructurado) y **Express** (Node/TS minimalista), justificando con criterios reales (lenguaje del equipo y del sistema, tamaño/complejidad, integración con IA, cuánta estructura hace falta) y nombrando el **costo** de cada elección.

## 📋 Contexto

La decisión "qué framework de backend" es un **ADR** real del capstone de la fase, y una pregunta de entrevista clásica. El error de junior es decidir por moda ("NestJS es más profesional") o por chovinismo de lenguaje ("Python es mejor"). El semi-senior decide por **contexto** y sabe nombrar lo que pierde con su elección. Este ejercicio entrena justo eso.

## 📏 Primero-Sin-IA

1. Decide y argumenta **solo**, a mano (timebox arriba).
2. Solo entonces, consulta documentación oficial si necesitas confirmar una característica.
3. **Solo al final**, usa IA para *cuestionar* tu razonamiento (pídele que defienda la elección opuesta) — no para que decida por ti.
4. Mañana, reescribe de memoria los dos criterios que más pesan al elegir framework.

## 🧩 Los tres escenarios

**Escenario A — Plataforma RAG en Python.**
Un equipo de 3 ingenieros, todos Python, construye un servicio que sirve un pipeline RAG: recibe preguntas, busca en un vector store (`pgvector`), llama a un LLM y devuelve la respuesta en streaming. Convive con librerías de embeddings, parsing de documentos y evals, todas de Python.

**Escenario B — Backend grande de una fintech, equipo TypeScript.**
Una fintech con 8 desarrolladores, todos en TypeScript (su frontend es Next.js). Van a construir un backend con ~40 endpoints repartidos en muchos dominios (cuentas, pagos, KYC, notificaciones), con varios equipos tocando el mismo repo durante años. Necesitan consistencia y onboarding rápido de gente nueva.

**Escenario C — Microservicio webhook chico.**
Un solo desarrollador necesita un servicio diminuto: recibe un webhook de un proveedor de pagos, valida una firma HMAC, escribe una fila en una cola y responde 200. Tres endpoints como mucho, y casi nunca cambiará. El resto del sistema es Node/TS.

## 🛠️ Instrucciones

Crea un archivo **`DECISION.md`**. Para **cada** escenario (A, B, C):

1. **Elige** un framework: FastAPI, NestJS o Express.
2. **Justifica** con al menos dos criterios concretos (lenguaje del equipo/sistema, tamaño y número de dominios, integración con IA, cuánta estructura vale la pena).
3. **Nombra un costo o riesgo** real de tu elección (ninguna opción es gratis).
4. **Di qué dato adicional** te haría cambiar de opinión.

Cierra con un párrafo: **¿cuál es el criterio que, casi siempre, descarta media decisión de entrada?** (pista: tiene que ver con en qué lenguaje ya vive el equipo y el resto del sistema).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las tres decisiones están justificadas con criterios concretos, no con eslóganes ("más moderno", "más profesional", "mejor lenguaje").
- [ ] Reconoces al menos un escenario donde la elección **no** es obvia y explicas la tensión.
- [ ] Cada elección nombra un costo real (no vendes ninguna como perfecta).
- [ ] Puedes defender, sin notas, por qué en el escenario A **FastAPI** suele ganar por ecosistema aunque alguien del equipo "sepa Node".
- [ ] El párrafo de cierre identifica el lenguaje/ecosistema del equipo como el criterio dominante.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **A (RAG en Python):** el eje dominante es el ecosistema. FastAPI vive donde viven las librerías de IA; meter un servicio Node sería un cuerpo extraño. Costo a nombrar: si en el futuro el frontend quisiera compartir tipos, no los compartiría con Python.
- **B (fintech grande, equipo TS):** muchos dominios + muchos devs + años = la estructura de NestJS (módulos, DI, consistencia) se paga sola. Express obligaría a inventar la estructura; FastAPI obligaría a cambiar de lenguaje. Costo: más ceremonia y curva de NestJS para gente nueva.
- **C (webhook chico, Node):** Express (o un FastAPI mínimo) gana por simplicidad; NestJS es overkill para 3 endpoints que no cambian. Costo: si el servicio crece inesperadamente, te faltará estructura.

El truco: el "mejor framework" depende del **lenguaje y el contexto**, no de una superioridad abstracta. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu `DECISION.md`, la **rúbrica** (`.ai/rubricas/fase-3/nestjs-vs-fastapi-decidir.md`) y las instrucciones (`.ai/INSTRUCCIONES-CORRECTOR.md`). La **solución de referencia** vive en `.ai/soluciones/fase-3/nestjs-vs-fastapi-decidir.md` — no la mires antes de intentarlo.
