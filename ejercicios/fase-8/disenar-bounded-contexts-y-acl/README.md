# 8.2 — Diseñar bounded contexts + un anti-corruption layer (sin código)

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.2` Arquitectura de aplicaciones + DDD táctico
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** diseño (a mano, sin código)

## 🎯 Objetivo

Diseñar las **fronteras** de un sistema de soporte con IA que integra un ERP externo legacy:
identificar sus **bounded contexts**, diseñar el **anti-corruption layer** que traduce el
modelo sucio del ERP a tu dominio (y valida lo no confiable), y **defender en un ADR** dónde
DDD táctico paga y dónde sería over-engineering. No escribes implementación: diseñas y justificas.

## 📋 Contexto

Es el músculo que el [Ejercicio Fase 8 — Diseña 3 sistemas en papel](/fase-8-system-design/proyecto/)
exige: pensar a nivel de sistema, dibujar fronteras y justificar decisiones. La integración
con un sistema externo que no controlas (un CRM/ERP, o la salida de un LLM) es el caso donde
el ACL deja de ser teoría: sin aduana, el modelo sucio del proveedor se filtra a tu dominio
y te acopla a él para siempre. Lee `escenario.md` antes de empezar.

## 📏 Primero-Sin-IA

1. Diséñalo **solo**, a mano (timebox arriba). Dibuja el mapa en papel primero si ayuda.
2. Solo entonces, consulta documentación oficial: el patrón
   [Anti-corruption layer (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)
   y [BoundedContext (Fowler)](https://martinfowler.com/bliki/BoundedContext.html).
3. **Solo al final**, usa IA para *revisar y cuestionar* tu diseño — no para *generarlo*.
4. Mañana, **redibuja el context map de memoria**. Si no puedes, no lo entendiste todavía.

## 🛠️ Instrucciones

Lee `escenario.md` (el flujo del sistema y el payload sucio del ERP). Produce **tres
documentos**:

### 1. `context-map.md` — el mapa de bounded contexts

- Identifica **2-3 bounded contexts** (p. ej. *Soporte*, *Facturación/ERP externo*, y quizá
  *Clasificación-IA* — defiende si lo separas o lo dejas dentro de Soporte).
- Dibújalos con un diagrama **Mermaid** (```mermaid```), mostrando la **relación** entre
  ellos: ¿upstream/downstream? ¿customer-supplier? ¿conformist? ¿anti-corruption layer?
- En 3-5 líneas, **argumenta por qué la frontera con el ERP externo exige un ACL** (no
  controlas su modelo, ya cambió antes, no quieres acoplarte a él).

### 2. `acl-diseno.md` — el diseño de la aduana

- Muestra el **modelo sucio** del ERP (el payload de `escenario.md`) y el **modelo limpio**
  de tu dominio (qué campos, qué tipos, qué value objects — p. ej. `Dinero`, un enum legible).
- Describe la **traducción campo por campo** (`pay_st: 3` → `MOROSO`, `bal: "15990.00"` →
  `Dinero(1599000)`, `nm` → nombre normalizado, etc.).
- Marca explícitamente **qué valida la aduana** y qué **rechaza** (el `pay_st: 4` mágico, el
  `bal` ausente o no numérico, etc.) y por qué eso es una **frontera de seguridad**, no solo
  de modelado (input externo = no confiable hasta validarlo; conecta con OWASP).

### 3. `adr-0001-acl.md` — la decisión, registrada

Formato ADR completo (contexto/problema · **≥2 opciones con pro/contra** · decisión justificada
· consecuencias con **gatillo**). La decisión central: **¿ACL propio vs conformist** (adoptar
el modelo del ERP tal cual en tu dominio)? Y cierra con un **párrafo de juicio**: ¿qué parte
de este sistema **merece** DDD táctico (aggregates/VOs) y qué parte es un **CRUD honesto** que
no lo necesita? Defiéndelo.

> ⚠️ **Esto no se implementa.** Si entregas código de la traducción, te desviaste del
> objetivo (diseñar fronteras y justificar). El valor está en el mapa, la traducción descrita
> y el ADR razonado.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `context-map.md` tiene **2-3 contexts** con fronteras claras y la **relación nombrada** (no solo cajas conectadas), en Mermaid.
- [ ] Argumentas por qué el límite con el ERP **necesita ACL** (modelo ajeno + ya cambió + acoplamiento).
- [ ] `acl-diseno.md` muestra **modelo sucio → modelo limpio** con traducción campo a campo.
- [ ] Identificas **qué valida/rechaza** la aduana y por qué es frontera de **seguridad** (input no confiable).
- [ ] El ADR tiene **≥2 opciones reales** (ACL vs conformist) con pro/contra, decisión atada al contexto y un **gatillo**.
- [ ] El párrafo de juicio nombra **una parte que merece DDD y una que no**, con razón defendible.
- [ ] Puedes **defender en voz alta** dónde DDD paga y dónde sería over-engineering en *este* sistema.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `context-map.md` — mapa de bounded contexts (Mermaid) + por qué el ERP exige ACL.
- `acl-diseno.md` — modelo sucio → limpio, traducción y validación/rechazo.
- `adr-0001-acl.md` — el ADR (ACL vs conformist) + el juicio DDD-sí / DDD-no.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el mapa: *Soporte* (tu core, donde vive el ticket) es **downstream** del *ERP*
(**upstream**, no lo controlas y no cambia por ti). Esa combinación —upstream ajeno +
downstream que debe protegerse— es la definición de libro de "aquí va un ACL". *Clasificación-IA*
puedes dejarlo como servicio dentro de Soporte o como context aparte: defiende tu elección
(¿tiene su propio lenguaje y reglas, o es un detalle de implementación de Soporte?).
Para el ACL: el payload sucio entra; sale un `EstadoPagoCliente` con un enum legible y un
`Dinero`. Valida que `pay_st` esté en tu conjunto conocido (rechaza `4`/`7`) y que `bal`
parseable. Para el juicio: el **estado de pago + la regla de qué hacer con un moroso**
probablemente merecen modelado rico (hay invariantes/decisiones); el **catálogo de categorías
de tickets** casi seguro es un CRUD plano que no gana nada con aggregates. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu diseño (este directorio: los tres `.md`),
- la **rúbrica**: `.ai/rubricas/fase-8/disenar-bounded-contexts-y-acl.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-8/disenar-bounded-contexts-y-acl.md`
— no la mires antes de intentarlo de verdad. Este ejercicio **no tiene una respuesta única**:
se evalúa si tus fronteras son defendibles y tu ADR pesa alternativas, no si coincidiste.
