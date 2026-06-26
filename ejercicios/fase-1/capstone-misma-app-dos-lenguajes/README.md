# 1.P — Capstone F1: La misma app, dos lenguajes (despensa HomeHub)

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.P` Capstone
**Ruta:** crítica · **Timebox:** 45 min por sesión (proyecto multi-sesión, ~6–10 h en total)

> Lee primero la lección: [Capstone F1 — La misma app, dos lenguajes](../../../src/content/docs/fase-1-lenguajes/proyecto.mdx).
> Este README es el **enunciado operativo**; la lección tiene el porqué y el ejemplo modelado.

## 🎯 Objetivo

Construir **la misma mini-API de despensa dos veces** —en Python y en
TypeScript/Node— a partir de una mini-spec compartida, con validación declarativa
(`pydantic` / `zod`), tests de aserciones reales (`pytest` / `vitest`) y un
write-up de los trade-offs entre ambas versiones.

## 📋 Contexto

Es la versión mínima del inventario de HomeHub: guarda ítems
`{ id, name, quantity, unit }` en un archivo JSON y expone 5 rutas HTTP. Sin base
de datos ni framework web (eso llega en la Fase 3): **solo la librería estándar**
de cada lenguaje, porque lo que se entrena aquí son **los lenguajes**. Este
proyecto es el insumo del Capstone de la Fase 2 (refactor + SOLID + mutation
testing), así que la separación dominio/HTTP que dejes aquí importa.

## 📏 Primero-Sin-IA

Este capstone **consolida** la fase: trabaja **sin IA de entrada**.

1. Diseña la mini-spec y escribe el código **tú**. Está bien que sea lento.
2. Consulta solo **documentación oficial** (enlaces en la lección).
3. **Solo al final**, usa IA para que *revise* tu código y tu write-up —nunca para
   que decida la estructura ni genere las dos versiones por ti—.
4. **Mañana**, reescribe de memoria el modelo de datos en `pydantic` y `zod`. Si no
   puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones (plan de 6 pasos)

1. **Mini-spec.** Completa [`SPEC.md`](./SPEC.md) (entradas, salidas, casos borde).
   No escribas código todavía.
2. **Python — dominio (TDD).** Corre los tests (fallan en rojo) e implementa
   `PantryStore` hasta verlos verdes:
   ```bash
   cd python
   uv run pytest            # o:  pip install pydantic pytest && pytest
   ```
3. **Python — HTTP.** Completa las rutas en `python/server.py`, levántalo y pruébalo:
   ```bash
   uv run python server.py  # escucha en http://127.0.0.1:8000
   curl -s localhost:8000/health
   curl -s -X POST localhost:8000/items -d '{"name":"arroz","quantity":2,"unit":"kg"}'
   ```
4. **TypeScript — dominio (TDD).** Mismo patrón, en `typescript/`:
   ```bash
   cd typescript
   npm install
   npm test                 # vitest
   ```
5. **TypeScript — HTTP.** Completa `typescript/server.ts` y pruébalo:
   ```bash
   npm start                # tsx server.ts, escucha en http://127.0.0.1:8001
   curl -s localhost:8001/health
   ```
6. **Documentación.** Escribe el `README.md` **en inglés** de tu proyecto (cómo se
   corre cada versión) con el **write-up de trade-offs**, y completa
   [`DECISIONES.md`](./DECISIONES.md) con ≥2 mini-ADRs.

> El **contrato HTTP** que ambas versiones deben cumplir está en
> [`CONTRATO-HTTP.md`](./CONTRATO-HTTP.md). Es idéntico para Python y TS.

## ✅ Criterios de "hecho" (Definition of Done del capstone)

- [ ] `SPEC.md` completado + `DECISIONES.md` con **≥2 mini-ADRs**. *(DoD §1)*
- [ ] **Ambas** versiones corren y cumplen el contrato HTTP (verificado con `curl`). *(DoD §8)*
- [ ] `pytest` **y** `vitest` en verde; cada suite con los tests del starter **+ uno tuyo**. *(DoD §2)*
- [ ] Un `POST /items` con `quantity: 0` o `name: ""` devuelve **422** en las dos versiones y **no** persiste el dato. *(DoD §2)*
- [ ] `README.md` en **inglés** con write-up de trade-offs (5–8 frases Python vs TS). *(DoD §8)*
- [ ] **Conventional Commits** en todo el historial. *(DoD §9)*
- [ ] Puedes **explicar tu diseño sin notas** (check de dominio de la lección).
- [ ] *(Opcional, victoria-IA)* ruta `POST /items/suggest` que llama a un LLM,
      **valida** la salida y registra **tokens/costo**.

## 💡 Pista (ábrela solo si te trabas al empezar)

<details>
<summary>Mostrar pista</summary>

Termina **Python completo primero** (dominio + tests + HTTP + `curl`) y úsalo como
**oráculo** para la versión TS. El dominio es: leer JSON → operar en memoria →
escribir JSON; el `id` nuevo es `max(ids, default 0) + 1`. La capa HTTP solo
**traduce**: parsea, llama al `PantryStore`, elige el status. Si una rama del
servidor tiene lógica de negocio, está en el lugar equivocado. Revisa las
sub-unidades 1.4 (validación), 1.5 (archivos/JSON) y 1.6 (tests) antes de mirar la
solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-1/capstone-misma-app-dos-lenguajes/` usando el
> framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

Le entregas: tu solución (este directorio), la **rúbrica**
(`.ai/rubricas/fase-1/capstone-misma-app-dos-lenguajes.md`) y las
`INSTRUCCIONES-CORRECTOR.md`. La **solución de referencia** vive en
`.ai/soluciones/fase-1/capstone-misma-app-dos-lenguajes.md` — no la mires antes de
intentarlo de verdad.
