---
ejercicio_id: track-0/historia-falla-produccion
fase: track-0
sub_unidad: "T0.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio es de **instrumentación + escritura**: no hay una única respuesta "correcta", hay **un patrón de calidad**. No penalices un incidente distinto al del ejemplar si cumple el patrón. Lo único innegociable: el incidente debe ser **real** (no de juguete).

# Solución de referencia — Historia de falla en producción

## Respuesta canónica (patrón de una entrega excelente)

No existe "la" respuesta. Una entrega excelente exhibe **cuatro patrones**:

1. **Incidente real con usuarios reales.** Aunque sean 3 (la pareja, un amigo). Hay impacto **humano** concreto, no un gráfico abstracto, y hay rastro (una línea de log real, un timeline con horas). La prueba: ¿podría el alumno mostrar la línea de log que correlaciona el fallo? Si los números son redondos y no hay rastro, sospecha fabricación.

2. **Causa raíz blameless y sistémica.** Los 5 whys terminan en algo que se puede cambiar en el sistema (un test que faltaba, una alerta inexistente, un deploy sin _graceful shutdown_, un review ausente), **nunca** en "una persona se equivocó" ni "el usuario hizo algo raro".

3. **Loop cerrado con una señal nueva.** La sección _Detection_ admite el hueco (qué debió alertar y no lo hizo) y los action items agregan una **métrica/alerta/SLO** concreta + un **test de regresión**. No termina en "ya lo arreglé".

4. **STAR en inglés derivada del mismo incidente**, con _Result_ apuntando a la señal nueva, mapeada a ≥3 preguntas.

### Ejemplar de incidente (vara de medir, NO para mostrar)

> **HomeHub — pérdida silenciosa de datos en la lista de compras (2 usuarios reales: la persona y su pareja).** Un deploy mató el contenedor a mitad de un POST de escritura; dos productos se perdieron sin que nada alertara; la usuaria se enteró en el supermercado, no por una señal.
>
> **5 whys (resumen):** el POST devolvió 500 → el contenedor se reinició por un deploy en curso → el deploy no drena requests en vuelo (sin _graceful shutdown_) → no había alerta sobre el camino de escritura → el frontend hizo _optimistic update_ y nunca confirmó contra el servidor, así que el dato se perdió en silencio.
>
> **Cierre del loop:** alerta sobre 5xx del camino de escritura + test de regresión que reproduce la escritura perdida durante reinicio + SLO "99.5% de escrituras exitosas en 30 días" con alerta de quema de error budget. La próxima vez, el sistema avisa en minutos.

Nota cómo el "bug" (un 500 puntual) es el **trigger**, pero la causa raíz es **sistémica** (deploy sin red de seguridad + frontend que miente sobre el estado + cero alertas del camino crítico). Ninguna es "una persona falló". Eso es nivel `excelente` en C2 y C3.

## Razonamiento paso a paso (qué hace buena cada parte)

- **Impact antes que causa.** El post-mortem humaniza primero (cuántos usuarios reales, qué perdieron, impacto en la confianza) y recién después diagnostica. Un impacto sin número o sin usuario es débil.
- **Detection como hueco, no como adorno.** La pregunta clave es "¿qué alertó?". Si la respuesta honesta es "nada, me avisó la usuaria", esa admisión **es** el hallazgo más valioso y justifica el action item de la alerta nueva. Castiga la ausencia de esta sección, no la honestidad.
- **5 whys hasta lo sistémico.** Cada "por qué" se aleja del síntoma. Parar en "había un bug" no enseñó nada; llegar a "ningún test cubría la escritura bajo reinicio" produce un action item que previene una familia de fallos.
- **Remediación ≠ prevención.** Arreglar el bug es remediar; agregar la alerta/SLO + el test de regresión es prevenir. El cierre obligatorio es la **señal nueva**.
- **Testing como reflejo.** Al menos un action item es un test de regresión que reproduce el fallo: es el hábito TDD del curso aplicado a un incidente.
- **Inglés.** Post-mortem y STAR en inglés porque ambos son artefactos públicos / de entrevista (T0.1). Traducir después no entrena el músculo.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Incidente de juguete.** Usuarios inventados, "100k usuarios", números redondos, sin línea de log ni timeline real ⇒ falla C1. Pide la evidencia (la línea de log).
2. **Causa con nombre propio.** "Fui descuidado" / "el dev no testeó" / "el usuario hizo algo raro" ⇒ no es blameless; reconduce a lo sistémico vía un "por qué" más.
3. **Parar en el trigger.** "Había un typo / un bug en la línea X" sin preguntar por qué llegó a producción sin ser detectado.
4. **Sin sección Detection** o que no admite que "me avisó el usuario" es un hueco.
5. **Termina en 'ya lo arreglé'.** Sin métrica/alerta/SLO nueva ni test de regresión ⇒ no cerró el loop (falla C3/C4).
6. **Action items sin dueño/fecha.** Es un diario, no ingeniería.
7. **STAR en español** o que no deriva del mismo incidente / no mapea a ≥3 preguntas ⇒ falla C5.
8. **Gray failure ignorado.** Si el incidente fue "respondía 200 pero entregaba mal", verificar que el alumno entendió que "está arriba" no es "está sano".

## Rango de soluciones aceptables

- El incidente puede venir de la app del alumno con usuarios reales **o** de un incidente real de su pasado (un cliente/compañero/usuario de un proyecto previo) — ambos son reales. Lo prohibido es inventar.
- Es válido que la instrumentación sea modesta (un log JSON + una alerta) o incluso un **plan honesto del "todavía no"**, siempre que no finja tenerla.
- La severidad puede ser baja: un fallo pequeño y verdadero gana a uno grande e inventado.
- La métrica/alerta/SLO nueva puede expresarse de varias formas (alerta de tasa de error, SLO de disponibilidad/latencia, health-check real); lo que importa es que **cerraría el loop** y sea defendible.
- El formato del post-mortem puede variar mientras estén las **7 secciones** y la causa raíz sea blameless.
- La historia STAR puede salir de este incidente o de otro real del alumno, mientras derive de un fallo en producción real y cumpla S/T/A/R + número + ≥3 preguntas.
