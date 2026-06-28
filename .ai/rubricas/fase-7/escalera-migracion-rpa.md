---
ejercicio_id: fase-7/escalera-migracion-rpa
fase: fase-7
sub_unidad: "7.4"
version: 1
---

# Rúbrica — Plan de migración de un RPA frágil

> Rúbrica **analítica** para un ejercicio **a-mano** de diagnóstico y diseño. Lo que se evalúa es la
> **calidad del plan**, no la prosa. Un alumno puede recitar "RPA es frágil"; otro señala la línea
> exacta, clasifica cada paso en la escalera y propone un corte incremental. La rúbrica distingue
> ambos. El corrector **no** da el plan: guía con pistas hasta que el alumno lo reconstruya.

## Objetivos evaluados

- **O1** — Diagnosticar modos de falla del bot RPA anclados a líneas/pasos concretos.
- **O2** — Clasificar cada paso en la escalera de integración con la restricción dominante.
- **O3** — Planear la migración con Strangler Fig (incremental, reversible) + ADR honesto + BPMN mínimo.

## Criterios y niveles

### C1 — Diagnóstico anclado · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 4 modos, o genéricos ("puede fallar") sin atarlos a una línea/paso del bot. |
| **en-progreso** | 4 modos plausibles, pero alguno mal atribuido o sin nombrar la causa raíz (posición vs significado, sleep, etc.). |
| **competente** | ≥4 modos **distintos** anclados a líneas concretas (los `click(x,y)`, los `sleep`, la falta de verificación, el re-lanzado que duplica, el `continue` silencioso). |
| **excelente** | Además distingue el peor estado (alta duplicada, o RUT inválido descartado en silencio) y por qué es *invisible* para operaciones — el argumento de observabilidad. |

### C2 — Escalera por paso · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No clasifica, o pone todo en el mismo escalón. |
| **en-progreso** | Clasifica algunos pasos, pero baja de escalón sin justificar (p. ej. propone RPA donde es web). |
| **competente** | Cada paso en su escalón con la restricción dominante; reconoce que `cargar_proveedores` y `validar_rut` ya son código puro (no tocan UI) y que `dar_de_alta`, al ser web sin API, va a navegador semántico (no coordenadas). |
| **excelente** | Cuestiona el supuesto "no hay API" (¿quién lo confirmó?) y nota que si el alta fuera crítica/alto volumen la respuesta sería presionar por API en vez de automatizar la UI. |

### C3 — Plan Strangler Fig + ADR + BPMN · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Propone reescribir todo de golpe (big-bang), o no hay ADR ni BPMN. |
| **en-progreso** | Plan incremental pero sin paralelo/medición, o ADR sin trade-off honesto, o BPMN ausente/ilegible. |
| **competente** | Cortes ordenados (empieza por lo puro/seguro), corre viejo y nuevo en paralelo con una métrica de confianza; ADR con contexto/decisión/alternativas/trade-off; BPMN/carriles legible. |
| **excelente** | El ADR admite un trade-off real (migrar cuesta: negociar API, operar más infra, perder la "visibilidad" del low-code); el BPMN separa actores por carril y comunica a alguien no técnico. |

## Errores típicos a marcar

- Confundir "la red puede fallar" (cualquier sistema) con "el bot clickea el vacío porque el botón se
  movió" (lo específico de la RPA por posición).
- Decir que el `sleep` "es lento" en vez del problema real: es una **apuesta** (teclea antes de tiempo
  o desperdicia segundos) que un navegador con esperas web-first elimina.
- Proponer un **big-bang rewrite** en lugar de Strangler Fig (cortes pequeños, reversibles, medidos).
- Clasificar `dar_de_alta` como "RPA-UI" cuando el portal es **web** → corresponde navegador semántico.
- ADR que vende la migración como gratis: omite que graduar también tiene costo (el trade-off honesto
  es justo lo que se evalúa).
- Sobre-invertir en BPMN/UML (diagramas elaborados) cuando se pide el mínimo para comunicar.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Diagnóstico con vocabulario muy pulido ("idempotencia", "observabilidad") pero **sin señalar las
  líneas concretas** del `bot_legado.py` dado.
- Plan genérico de Strangler Fig copiado de un blog que no menciona `cargar_proveedores`/`validar_rut`
  como el primer corte natural (la pista de que el alumno leyó *este* bot).
- **Verificación sugerida:** pedir que señale el número de línea de cada falla y diga qué pasa si el
  proceso muere justo después del `click` de "Guardar". Si diagnosticó de verdad, responde al instante.

## Feedback sugerido (graduado)

> Nunca entregar el plan completo antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Recorre el bot línea a línea preguntándote: *si el portal cambia un píxel, o
  la red va lenta, o el RUT ya existía, ¿qué hace?*. Empieza por los dos `click(x, y)`."
- **Pregunta socrática (nivel 2):** "¿Cuáles funciones del bot **no tocan ninguna UI**? Esas son tu
  primer corte de Strangler Fig: las más baratas y seguras de migrar hoy. ¿Por qué empezar por ahí?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa por escalón: `cargar_proveedores`
  y `validar_rut` ya son código puro. `dar_de_alta` es web sin API → navegador con selectores
  semánticos, no coordenadas. Tu ADR debe decir qué CUESTA migrar, no solo qué ganas."

## Conexión con el proyecto / capstone

Diagnosticar y planear esta migración es el paso previo a integrar bien las acciones externas del
capstone agéntico de la fase: antes de que un agente "ejecute en sistemas externos" hay que decidir
**cómo** integra (escalera) y dejarlo en un ADR. Es la pregunta de entrevista "¿cómo migrarías un RPA
frágil sin romper producción?".
