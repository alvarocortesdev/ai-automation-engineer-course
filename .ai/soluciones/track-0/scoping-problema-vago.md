---
ejercicio_id: track-0/scoping-problema-vago
fase: track-0
sub_unidad: "T0.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **diseño/razonamiento**: el spec de cada alumno será distinto. Lo que se mide es el **criterio de
> discovery** (separar solución imaginada del problema, preguntas pertinentes, MVP acotado), no que el
> spec coincida palabra por palabra.

# Solución de referencia — Discovery de la clínica SonrIA

## 0. Solución imaginada vs. problema (referencia)

- **Solución imaginada del cliente:** "un asistente con IA que hable con los pacientes por WhatsApp".
- **Por qué no construirla aún:** "WhatsApp" y "asistente conversacional" es **cómo** Rodrigo imaginó la
  solución, no su problema. El problema, leyendo el mensaje, son los **no-shows** (citas que no asisten =
  pérdida de plata) y las **horas de recepción gastadas confirmando por teléfono**.
- **Problema en una frase:** *"La clínica pierde ingresos por citas a las que el paciente no asiste, y el
  equipo gasta tiempo confirmando manualmente."* (Admite varias soluciones: recordatorios automáticos,
  overbooking inteligente, confirmación por el canal que el paciente ya use —WhatsApp es una opción, no
  el objetivo.)

## 1. Banco de 7 preguntas (referencia)

| # | Dimensión | Pregunta de referencia | Supuesto razonable |
|---|---|---|---|
| 1 | Outcome | "Si esto funcionara, ¿cuánto bajaría el % de no-shows y cuántas horas de confirmación ahorrarían?" | Hoy ~25-30% de no-shows; 2 recepcionistas, ~2 h/día c/u confirmando. |
| 2 | Usuario | "¿Quién interactúa: el paciente, la recepcionista, ambos?" | El sistema lo opera recepción; el paciente solo recibe el recordatorio y confirma. |
| 3 | Proceso actual | "Cuéntame cómo confirman una cita hoy, paso a paso." | Llaman uno por uno la víspera; muchos no contestan. |
| 4 | Costo de error | "¿Qué pasa si el sistema le recuerda mal la hora a un paciente?" | Grave (paciente llega a destiempo) → el mensaje debe leer la hora correcta del sistema, no inventarla. |
| 5 | Datos | "Las citas y los teléfonos, ¿están limpios y al día en Dentalink? ¿Hay API?" | Datos existen pero hay teléfonos desactualizados; validar si Dentalink expone API/export. |
| 6 | Restricciones | "Datos de salud (sensibles), antes de temporada alta (¿fin de año?), ¿presupuesto?" | Privacidad (datos de pacientes), plazo Q4, presupuesto acotado de pyme. |
| 7 | Rebanada mínima | "Si solo pudieran atacar UNA cosa primero, ¿no-shows o las horas de recepción?" | Reducir no-shows pesa más (impacto directo en ingresos). |

## 2. Mini-spec de referencia

```text
PROBLEM STATEMENT
La clinica pierde ingresos por citas no asistidas (~25-30% no-shows) y el equipo de
recepcion gasta ~4 h/dia confirmando citas a mano por telefono.

SUCCESS METRIC
- Reducir no-shows desde ~28% (linea base a medir) a un objetivo (ej. <15%) en 6 semanas.
- Reducir horas de confirmacion manual (linea base ~4 h/dia).

EN-SCOPE (MVP)
Recordatorio automatico de cita por el canal que el paciente ya usa (WhatsApp/SMS),
leyendo fecha/hora directo del sistema, con confirmacion de un toque (Si/Reagendar);
las respuestas "reagendar" caen en una bandeja para que recepcion las gestione.

FUERA-DE-SCOPE (fase 2+)
Asistente conversacional que "hable" con el paciente; reprogramacion automatica;
manejo de pagos; cualquier respuesta generada por IA libre.

RESTRICCIONES
Datos de salud (privacidad/consentimiento); integracion con Dentalink (validar API);
entregable antes de temporada alta (Q4); presupuesto de pyme.

REBANADA MINIMA DE VALOR
Recordatorio + confirmacion de un toque para UNA sucursal, midiendo no-shows antes/
despues. Si baja, se expande a las 3 sucursales y a la fase 2.

SUPUESTOS Y PREGUNTAS ABIERTAS
- Asumo que Dentalink permite leer/exportar citas (VALIDAR: es la incognita #1).
- Pendiente: % real de no-shows actual; cuantos telefonos estan al dia.
- Pendiente: consentimiento de los pacientes para mensajeria.
```

> Clave: el MVP **no es un chatbot**. Es un recordatorio con confirmación —mucho más simple, entregable
> en el plazo, y que ataca el dolor #1 (no-shows). "WhatsApp" aparece como **canal de implementación**, no
> como el objetivo. Eso es haber separado la solución imaginada del problema.

## 3. Pregunta de mayor riesgo (referencia)

**El acceso a los datos de Dentalink (pregunta 5).** Todo el MVP asume que se puede leer fecha/hora y
teléfono del sistema de forma confiable. Si Dentalink **no** expone API ni export usable, el diseño
cambia por completo (carga manual, otro proveedor, o reevaluar el proyecto). Es la incógnita que más
mueve la aguja, por encima del % exacto de no-shows.

## Puntos donde el corrector debe mirar
1. **¿El spec codea la solución imaginada?** Si el problem statement o el en-scope dicen "chatbot/
   asistente conversacional" como objetivo, el alumno no separó solución de problema. Error central.
2. **¿El MVP acota de verdad?** Un "MVP" que incluye conversación + reprogramación + pagos no es mínimo.
3. **¿El costo de error generó una decisión?** La hora correcta debe salir del sistema (no inventada): es
   una decisión técnica que nace de una pregunta de negocio.
4. **¿Distingue supuesto de hecho?** Las respuestas son supuestos por validar, no datos confirmados.

## Rango de soluciones aceptables
- Atacar primero **las horas de recepción** en vez de los no-shows es válido **si se justifica** (p. ej.
  el cliente valora más liberar al equipo). Lo no válido es no priorizar y meter todo al MVP.
- Elegir SMS, email o WhatsApp como canal es indistinto: lo que importa es que el canal sea una decisión
  de implementación, no el objetivo del spec.
- Marcar el acceso a datos **o** el consentimiento de pacientes como riesgo #1 son ambos defendibles.
- Cualquier métrica con número y línea base cuenta; "que funcione mejor" no.
- Entregar en inglés suma el bonus del hilo; en español es aceptable.
