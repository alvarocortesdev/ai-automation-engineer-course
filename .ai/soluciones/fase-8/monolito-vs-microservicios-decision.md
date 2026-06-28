---
ejercicio_id: fase-8/monolito-vs-microservicios-decision
fase: fase-8
sub_unidad: "8.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Los escenarios 1–4 tienen respuesta
> clara; el 5 es deliberadamente ambiguo y admite ambas decisiones bien defendidas.

# Solución de referencia — Decisor: ¿monolito modular o microservicios?

## Respuestas canónicas (escenarios 1–4)

### Escenario 1 — MVP de equipo chico → **Monolito modular**
- **Restricción dominante:** equipo pequeño + **dominio incierto**. Ninguna de las cuatro razones reales
  está presente.
- **Por qué:** con el modelo de datos aún en flujo, los límites correctos todavía no se conocen; cortar
  servicios ahora casi garantiza cortar mal, y reordenar entre servicios es carísimo. El monolito modular
  da ownership y límites hoy, y deja la puerta abierta a extraer después.
- **Gatillo de extracción esperado:** "cuando un módulo necesite escalar muy distinto al resto, o cuando
  entre un segundo/tercer equipo que bloquee releases".

### Escenario 2 — Organización grande que se pisa → **Microservicios**
- **Restricción dominante:** **organizacional** — 15 equipos pisándose en un solo despliegue (Ley de
  Conway). Releases de dos semanas de coordinación es el síntoma clásico.
- **Costo asumido:** consistencia distribuida (sagas donde había transacciones), N pipelines, observabilidad
  distribuida. Se pagan porque el cuello de botella ya no es técnico, es de coordinación humana.
- Matiz excelente: la extracción debería ser **incremental** (Strangler Fig), no un big-bang.

### Escenario 3 — Componente caliente (transcodificación) → **Extraer ESE componente a un servicio**
- **Restricción dominante:** **escala desigual** (un módulo necesita ~50 máquinas, el resto una). Posible
  también tech divergente (transcodificación suele ser CPU/GPU intensiva).
- **Por qué:** en un monolito tendrías que escalar TODO el proceso para alimentar un solo componente
  hambriento. Extraer solo transcodificación permite escalarla sola. **No** es "pásate a microservicios
  para todo": es extraer **un** servicio del monolito modular.
- **Costo asumido:** la llamada a transcodificación pasa a ser por red (asíncrona, idealmente por cola →
  encaja con DLQ/idempotencia de 7.2).

### Escenario 4 — Arquitectura por estética → **Monolito modular**
- **Restricción dominante:** **ninguna real** — "para que quede bien arquitecturado" es estética, no un
  problema presente. Es el gemelo del escenario 1 y primo de la pattern-itis de 2.5.
- **Por qué:** pagarían latencia de red, sagas y N despliegues sin resolver nada que tengan hoy. La
  arquitectura sigue al dolor, no a la aspiración.
- **Gatillo:** el mismo del escenario 1.

## Escenario 5 — Caso ambiguo (ambas defendibles)

No hay respuesta única. Lo que se evalúa es el **trade-off explícito**.

**Defensa A — Monolito modular bien gobernado (decisión recomendada por defecto):**
- El dolor existe (conflictos de despliegue) pero **no es crítico** (un par al mes, nadie bloqueado).
- Antes de pagar el costo distribuido completo, hay palancas más baratas: **ownership por módulo**, dueños
  de despliegue, feature flags, mejor modularización interna. Resuelven la mayoría de los conflictos sin
  red, saga ni N pipelines.
- **Renuncia/riesgo aceptado:** si los equipos crecen o los conflictos escalan, habrá que extraer servicios
  más tarde (y se aceptó posponer esa inversión).
- **Desempate:** la fuerza pro-microservicios (conflictos) es **real pero leve**; no justifica aún el salto.

**Defensa B — Empezar a extraer el primer servicio (también válida):**
- 30 ingenieros / 4 equipos está en la zona donde la independencia de despliegue empieza a pagar.
- Extraer **un** servicio (el de menor acoplamiento transaccional) de forma incremental valida el camino
  sin comprometerse a partir todo.
- **Renuncia/riesgo aceptado:** introduce su primera saga / llamada por red y la operación asociada; hay
  que instrumentar trazas distribuidas desde ya.
- **Desempate:** apuesta a que los conflictos crecerán con el equipo y prefiere adelantarse de forma
  controlada.

> Ambas son **excelentes** si nombran una fuerza a favor, una en contra (la renuncia) y el desempate.
> Es **en-progreso** si decide sin nombrar qué renuncia. Es **incompleto** si esquiva el caso o lo trata
> como si tuviera respuesta obvia.

## Patrón de cierre (lo que debería notar)
Las decisiones de **monolito** (1, 4) comparten "no hay restricción real presente". Las de
**microservicios** (2, 3) comparten "hay una restricción real y concreta —organizacional o de escala—".
El caso 5 es exactamente la frontera: dolor real pero sub-crítico. Reconocer esa frontera **es** el
objetivo del ejercicio.

## Rango de soluciones aceptables
- Llamar al escenario 3 "microservicios" en vez de "extraer ese componente" es aceptable como
  `competente` si el razonamiento es de escala desigual; es `excelente` si nota que solo se extrae el
  componente caliente, no todo.
- En el escenario 5 cualquiera de las dos defensas cuenta como `excelente` con su trade-off; la decisión
  concreta no determina el nivel, el razonamiento sí.
