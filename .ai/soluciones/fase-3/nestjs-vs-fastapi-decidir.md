---
ejercicio_id: fase-3/nestjs-vs-fastapi-decidir
fase: fase-3
sub_unidad: "3.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio **no tiene respuesta única**: lo que sigue son las decisiones más defendibles y los criterios para juzgar otras.

# Solución de referencia — Decide: FastAPI, NestJS o Express

## Principio rector para corregir

No corrijas *qué* framework eligió, corrige *cómo* lo justificó. El criterio que más pesa, casi siempre, es **el lenguaje y ecosistema del equipo y del resto del sistema**: el framework no debería forzar un cambio de lenguaje. El segundo eje es el **tamaño/complejidad del proyecto** (cuántos dominios, cuántos devs, cuántos años): a más complejidad, más se paga la estructura de NestJS; a menos, gana la simplicidad de Express/FastAPI. Una elección "contraria a la esperada" bien argumentada con trade-offs vale más que la "esperada" con un eslogan.

## Decisiones defendibles por escenario

### Escenario A — Plataforma RAG en Python
- **Elección esperada: FastAPI.**
- **Criterios:** el equipo es 100% Python y la app vive **entre librerías de IA de Python** (embeddings, parsing, evals, cliente del LLM). FastAPI es el estándar para servir IA y comparte ecosistema con todo el resto; el streaming token-por-token es de primera clase. Meter NestJS/Express obligaría a un servicio Node aislado del stack de IA, sin beneficio.
- **Costo a nombrar:** si más adelante el frontend (TS) quisiera **compartir tipos** con el backend, FastAPI no los comparte como lo haría un backend TS.
- **Dato que cambia la decisión:** que el equipo fuera en realidad TypeScript y existiera un SDK Node maduro para todo el pipeline RAG.

### Escenario B — Backend grande de fintech, equipo TypeScript
- **Elección esperada: NestJS.**
- **Criterios:** equipo 100% TS (front Next.js) + ~40 endpoints en muchos dominios + varios devs + años de vida. Aquí la **estructura impuesta** de NestJS (módulos, DI, consistencia, onboarding rápido) se paga sola: todos los recursos se ven igual y la gente nueva se ubica rápido. Express obligaría a inventar y mantener esa estructura a mano; FastAPI obligaría a cambiar de lenguaje.
- **Costo a nombrar:** más ceremonia y curva de aprendizaje de NestJS (decoradores, DI, módulos) para quien llega de Express puro.
- **Dato que cambia la decisión:** que en realidad fueran a partir el sistema en microservicios chicos e independientes desde el día 1 (donde la estructura monolítica de Nest pesa menos).
- **Tensión (nivel excelente):** reconocer que Express **también** podría servir con una estructura propia disciplinada; la apuesta por NestJS es por consistencia a escala, no por imposibilidad de Express.

### Escenario C — Microservicio webhook chico (Node)
- **Elección esperada: Express** (o un FastAPI mínimo si el equipo prefiriera Python, pero el sistema ya es Node).
- **Criterios:** 3 endpoints que casi nunca cambian = la ceremonia de NestJS es **overkill**. Express arranca en minutos y hace exactamente lo necesario (recibir webhook, validar HMAC, encolar, responder 200). El sistema ya está en Node, así que no hay fricción de lenguaje.
- **Costo a nombrar:** si el servicio creciera inesperadamente (más dominios, más devs), faltaría la estructura que NestJS daría gratis; habría que refactorizar.
- **Dato que cambia la decisión:** que el "microservicio" fuera en realidad la semilla de un backend grande planificado.

## Qué hace que una entrega sea "competente" vs "excelente"

- **Competente:** las tres decisiones se apoyan en lenguaje/ecosistema + tamaño del proyecto y nombran un costo real por escenario.
- **Excelente:** además expone la tensión del escenario ambiguo (típicamente B o un caso límite), no finge que todo es obvio, y los costos/datos-que-cambian-la-decisión son específicos (no genéricos como "tiene curva").

## Errores a marcar (resumen)
- Decidir por moda/popularidad o por chovinismo de lenguaje.
- NestJS para el webhook chico "porque es más profesional" (overkill).
- FastAPI en el equipo 100% TS "porque Python es mejor" (forzar cambio de lenguaje).
- Vender una opción como perfecta (sin costo).
- No reconocer ninguna ambigüedad en los tres.

## Variante de control anti-IA
Pedir el **contrafactual** del escenario A: "¿qué tendría que ser verdad para que NestJS fuera la mejor opción en la plataforma RAG?". Respuesta razonada esperada: que el equipo fuera TS y existiera un ecosistema Node maduro para embeddings/vector store/LLM que evitara aislarse del stack de IA. Quien copió una comparativa genérica no puede construir el contrafactual.
