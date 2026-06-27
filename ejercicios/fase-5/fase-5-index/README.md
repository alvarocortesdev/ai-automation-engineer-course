# fase-5-index — Diagnóstico de Fase 5 y plan de ruta a producción

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 35 min · **Modalidad:** a-mano (razonamiento/diseño, sin tests)

## 🎯 Objetivo

Orientarte antes de empezar la fase: autoevaluar honestamente tu punto de partida
en DevOps, diseñar un plan de estudio sostenible **y** trazar el orden en que vas a
apilar un pipeline a producción sobre la app que ya construiste, evidenciando cada
punto del Definition of Done del capstone.

## 📋 Contexto

La Fase 5 no inventa una app nueva: lleva tu API (Fase 3) y tu frontend (Fase 4) a
producción. Este ejercicio es tu **placement** (qué ya sabes y qué no) y tu
**contrato** (cómo y cuándo lo vas a estudiar y aplicar). No tiene respuesta única
correcta: se corrige por honestidad, concreción y por si tus evidencias son
verificables.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Autoevaluación honesta, no la que
   te gustaría tener.
2. Solo entonces, si quieres calibrar, hojea la portada de la fase
   (`/fase-5-devops/`) — pero el diagnóstico es **tuyo**, no de un chat.
3. **Solo al final**, usa IA para *revisar* tu plan — no para *generarlo*.
4. Al cerrar cada sub-unidad, vuelve y actualiza tu diagnóstico.

## 🛠️ Instrucciones

Crea **tres archivos markdown** en este directorio:

1. **`diagnostico.md`** — tabla con las 8 sub-unidades de ruta-crítica (5.1, 5.2,
   5.3, 5.4, 5.5, 5.8, 5.9, 5.10). Por cada una: nivel (`nuevo` · `lo reconozco` ·
   `lo sé hacer sin notas`) **y una razón**. Prueba de "lo sé hacer": ¿lo
   resolverías ahora sin notas y sin IA?
2. **`plan-fase-5.md`** — bloques semanales concretos (día/hora/duración) + ritual
   de repaso (cuándo reescribes de memoria) + el **orden de apilado** del pipeline
   sobre tu app (contenedor → config por entorno → CI con tests → gates de
   seguridad → deploy → observabilidad) + **cómo conseguirás ≥3 usuarios reales**.
3. **`definicion-de-listo.md`** — los 7 puntos del DoD del Capstone F5 con tus
   palabras y, junto a cada uno, **cómo lo evidenciarás** (algo que alguien pueda
   abrir y ver: un link, una captura, un nombre).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `diagnostico.md` cubre las **8** sub-unidades de ruta-crítica con nivel **y** razón por fila.
- [ ] El nivel es **defendible**: no todo en "lo sé hacer" sin evidencia, ni todo en "nuevo" si declaraste experiencia.
- [ ] `plan-fase-5.md` tiene bloques con **día, hora y duración** reales + un ritual de repaso explícito.
- [ ] El plan incluye un **orden de apilado** coherente con el flujo de la fase y termina en **≥3 usuarios reales**.
- [ ] `definicion-de-listo.md` traduce los **7 puntos del DoD** en **evidencias verificables**, no intenciones.
- [ ] Puedes **defender en voz alta** por qué pusiste el nivel que pusiste en al menos dos filas (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El error #1 en DevOps es la sobreconfianza: "ya usé `docker compose up`" no es
"sé escribir un Dockerfile multi-stage sin notas". Si nunca configuraste un gate
de seguridad que rompa el build, 5.4 es `nuevo`. Para el orden de apilado, no
automatices el deploy de algo que aún no empaquetaste ni hiciste configurable.
Para la definición de listo, cambia "tendré observabilidad" por "mostraré **esta**
traza con **este** correlation ID": cada punto necesita una evidencia abrible.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, los tres `.md`),
- la **rúbrica**: `.ai/rubricas/fase-5/fase-5-index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/fase-5-index.md` — es
un exemplar para el corrector, no una plantilla a copiar. No la mires antes de
intentarlo de verdad.
