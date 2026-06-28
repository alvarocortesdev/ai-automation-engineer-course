---
ejercicio_id: fase-7/criterio-de-salida-n8n
fase: fase-7
sub_unidad: "7.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ejercicio de razonamiento:
> **no hay respuesta única**. Esto es el rango de respuestas defendibles, no "la" respuesta.

# Solución de referencia — Criterio de salida: ¿n8n, código o Temporal?

## Cómo usar esta solución

El alumno entrega `decision.md` (tabla + ADR). Se corrige el **razonamiento**, no la coincidencia.
Una elección distinta a la de abajo puede ser perfectamente válida si la restricción que la justifica
es defendible. Lo que NO es defendible: mandar el caso durable a n8n, tratar el de IA como dicotomía,
o un ADR sin trade-off.

## Tabla de decisión de referencia (rango aceptable)

| # | Escenario | Elección esperada | Restricción dominante | Señal de cambio |
|---|-----------|-------------------|-----------------------|-----------------|
| 1 | Bienvenida a leads | **n8n** | Lineal, baja frecuencia, lo mantiene **ops/marketing (no-dev)** y la visibilidad importa | Si la lógica crece (segmentación compleja, muchas ramas) o el volumen sube fuerte → reconsiderar código |
| 2 | Motor de pricing | **código** (servicio + colas) | Lógica compleja/cambiante + **tests serios** + equipo de devs + alto volumen | Si las reglas se estabilizan y bajan a 2-3 simples mantenidas por ops → podría volver a n8n |
| 3 | Onboarding de proveedor | **Temporal** (durable execution) | **Esperas de días + reanudar exacto tras crash + exactamente-una-vez** (el cobro) | Si las esperas desaparecen y todo es síncrono en segundos → no necesita durabilidad, basta código |
| 4 | Triage de documentos con IA | **híbrido** (n8n orquesta + servicio en código extrae/evalúa) | Orquestación simple y visible para ops **+** core de IA que necesita evals y testabilidad | Si la extracción se vuelve trivial y estable → todo n8n; si la orquestación se complica mucho → todo código |

## Por qué cada una (lo que el alumno debe poder defender)

- **#1 n8n.** El error sería "código porque soy dev": acá n8n gana **porque** un no-dev tiene que poder
  ajustarlo y el flujo es trivial. La herramienta se elige por el mantenedor y la complejidad, no por ego.
- **#2 código.** Lógica que cambia seguido + casos borde + tests unitarios + review línea a línea + volumen
  = territorio de código testeable. Meter 12 reglas anidadas en nodos "Function" produce una bola de barro
  ingobernable (límite real del low-code).
- **#3 Temporal.** La firma inconfundible: **esperar días**, **reanudar exactamente donde quedó** tras un
  reinicio, **replay determinista**, **exactamente una vez** en el cobro. n8n puede esperar con un nodo Wait,
  pero no garantiza durabilidad de estado ni replay. Un script con cron tampoco. Es justo lo que durable
  execution (7.3) resuelve.
- **#4 híbrido.** La trampa es elegir dicotomía. La orquestación (recibir → decidir ruta → disparar) es simple
  y conviene visible para ops → n8n delgado. Pero la extracción con IA necesita evals y lógica testeable →
  un servicio en código que n8n invoca. Lo mejor de ambos: visibilidad + testabilidad del core.

## ADR esperado (ideas, no literal)

Para el escenario que el alumno gradúe (típicamente #2 o #3). Debe incluir:
- **Contexto:** qué hace el flujo y qué síntoma muestra que n8n ya no rinde (lógica ingobernable / falta de
  durabilidad).
- **Decisión:** a qué gradúa y la restricción que lo exige.
- **Alternativas:** quedarse en n8n (por qué no), y al menos otra opción descartada.
- **Trade-off honesto:** qué PIERDE — menos visibilidad para operaciones, más infraestructura que operar,
  curva de aprendizaje (sobre todo si gradúa a Temporal). Si el ADR solo lista ventajas, está incompleto.

## Notas para el corrector

- Una elección distinta a la tabla es válida **si la restricción la sostiene**. Ej.: alguien podría defender
  #4 como "todo n8n con un nodo de IA" si argumenta bien la simplicidad de la extracción — pero debe
  reconocer que pierde testabilidad/evals serios. Pídele que defienda el trade-off.
- Lo inaceptable: #3 en n8n "con un Wait" sin reconocer la falta de durabilidad/replay; o "código siempre
  mejor" sin nombrar al mantenedor no-dev de #1.
- Premia que el alumno mencione el **patrón híbrido** y que graduar **cuesta** (no es gratis). Esa honestidad
  es la marca del criterio maduro.
