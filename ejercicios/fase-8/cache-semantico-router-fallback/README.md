# Ejercicio 8.5b — Caché semántico + router con fallback

> **Modalidad: código (Python puro, sin LLM real).** Las dos piezas que más bajan la factura de un
> sistema de IA sin tocar la calidad: un **caché semántico** y un **router multi-modelo con fallback**.
> El embedding y la llamada al modelo se **inyectan**, así los tests son deterministas (sin red, sin
> sleep, sin flakiness) — exactamente la disciplina de testabilidad de [2.8](/fase-2-ingenieria/2-8-diseno-de-tests/).

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.5` Arquitectura de sistemas de IA a escala
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Implementar `SemanticCache`: un `get` devuelve un hit solo si hay un vecino **del mismo
  tenant** con similitud coseno **≥ umbral**, y un tenant **nunca** recibe el hit de otro.
- **O2** — Implementar `elegir_modelo`: la tarea fácil al modelo barato, la difícil al caro.
- **O3** — Implementar `responder_con_fallback`: degrada **solo** ante errores reintentables (429/5xx) y
  **no enmascara** un error del request (400) — lo deja propagar.

## 📋 Contexto

El caché semántico **elimina** llamadas al LLM (no las abarata: eso es prompt caching) y el router
manda lo fácil a un modelo ~5x más barato. Juntos atacan el costo, que es el cuello de botella de un
sistema de IA a escala. El aislamiento por tenant es **seguridad**, no solo relevancia: un hit cruzado
entre clientes es una fuga de datos. Esto alimenta el [capstone de la fase](/fase-8-system-design/proyecto/).

## 📏 Primero-Sin-IA

1. Implementa los `TODO` **solo**, a mano, dentro del timebox. Está bien que sea feo y lento.
2. Solo entonces consulta la sección de la lección sobre caché semántico y fallback chain.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescríbelo de memoria. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `cache_router.py` y completa los `TODO` (no cambies las firmas públicas). El helper `coseno`
   y las clases de error (`ModeloSaturado` = 429/5xx, `RequestInvalido` = 400) ya están hechos.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test propio** (un caso borde tuyo). Ideas: que dos preguntas **idénticas** de
   tenants distintos **no** comparten caché; que subir el umbral convierte un hit en miss; que la cadena
   de fallback **deduplica** modelos repetidos.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan (`pytest` en verde).
- [ ] El caché hace **hit por similitud** (no solo por igualdad exacta) y **miss bajo umbral**.
- [ ] El caché **aísla por tenant**: un tenant nunca recibe el hit de otro (seguridad).
- [ ] El router manda lo fácil al barato y lo difícil al caro.
- [ ] El fallback **degrada en 429/5xx** y **propaga el 400** sin convertirlo en otra cosa.
- [ ] **Cero** llamadas a un LLM real o a la red dentro de `cache_router.py`.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Caché:** una lista de tuplas `(tenant_id, embedding, respuesta)` basta. En `get`, **filtra primero
  por tenant** (esa es la barrera de seguridad), luego busca el de mayor `coseno`, y compara contra
  `self.umbral`. Si no hay entradas de ese tenant, es un miss.
- **Fallback:** recorre la cadena; envuelve `call_fn` en `try/except`. Captura **solo** `ModeloSaturado`
  para pasar al siguiente; **no** captures `RequestInvalido` (déjalo propagar). Para deduplicar
  preservando el orden: `dict.fromkeys(cadena)`. Si terminas el bucle sin éxito, `raise RuntimeError`.

Revisa la sección de la lección sobre caché semántico y fallback chain antes de mirar la solución de
referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-8/cache-semantico-router-fallback.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-8/cache-semantico-router-fallback.md` — no la
mires antes de intentarlo de verdad.
