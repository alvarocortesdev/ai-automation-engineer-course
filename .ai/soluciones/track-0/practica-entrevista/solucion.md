---
ejercicio_id: track-0/practica-entrevista
fase: track-0
sub_unidad: "T0.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio es de **diseño + autoevaluación**: no hay una única respuesta "correcta", hay **un patrón de calidad**. No penalices contenido distinto al del ejemplar si cumple el patrón.

# Solución de referencia — Cadencia + banco STAR + autoevaluación de mock

## Respuesta canónica (patrón de una entrega excelente)

No existe "la" respuesta. Una entrega excelente exhibe **tres patrones**:

1. **Cadencia ejecutable, no aspiracional.** Día y hora fijos para los 3 formatos, herramientas nombradas, y la regla inglés/grabado/autoevaluado-el-mismo-día. La prueba: ¿podría un tercero ejecutar este plan tal cual está escrito? Si dice "cuando pueda", falla.

2. **Historias STAR estructuradas, con número, reutilizables.** S breve, A dominante, R con métrica, y cada historia mapeada a ≥3 preguntas.

3. **Autoevaluación que evidencia haberse escuchado**, con una mejora accionable atada a un criterio observable.

### Ejemplar de una historia STAR (vara de medir, NO para mostrar)

> **S** — "An n8n workflow that enrolled new clients was failing silently a few times a week; no alert fired, so we found out days later with duplicated records downstream."
> **T** — "I owned making it reliable, not just stopping the crash."
> **A** — "I reproduced the failure first instead of guessing, read the execution logs, and found a retry step that wasn't idempotent — every retry re-inserted the record. I added an idempotency key on the external call, a dead-letter path for the cases that still failed, and a failure alert to Slack."
> **R** — "Failures went from ~3/week to 0 over two months, and we stopped losing ~4 hours/week reconciling duplicates by hand."
>
> _Cubre:_ "difficult bug", "improved a process", "took ownership", "production failure", "worked with unreliable data".

Nota cómo **demuestra** idempotencia + observabilidad + manejo de errores sin que el candidato diga "soy bueno en eso". Eso es nivel `excelente` en C2.

## Razonamiento paso a paso (qué hace buena cada parte)

- **Proporción STAR.** El contexto (S) en 1-2 frases; la Action ~60%; el Result siempre con número. El error más común es la S inflada que se come el tiempo. Una buena Action narra **método** (medir/diagnosticar/decidir), no una lista de tareas.
- **Reutilización.** El sentido del banco de 8-10 es que **una** historia cubre varias preguntas. Si el alumno escribió una historia por pregunta, no entendió el mecanismo (apunta a C2 en-progreso).
- **Número en el Result.** "Quedó mejor" no es resultado; "bajó de 6 s a 1,8 s" sí. Sin número, la historia no demuestra impacto.
- **Grabación = observabilidad.** La autoevaluación honesta nace de **escucharse**: muletillas, silencios sin narrar, no clarificar. La mejora debe ser un comportamiento concreto y medible la próxima semana, no "hablar mejor".
- **Inglés.** Las historias y el mock van en inglés porque el gate de mercado es hablar bajo presión en inglés (T0.1). Traducir después no entrena ese músculo.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Cadencia aspiracional.** "Practicaré 3 veces por semana" sin día/hora ⇒ no es cadencia. Exige concreción.
2. **Result sin número** en una o más historias ⇒ el feedback debe pedir la métrica, no reescribir la historia.
3. **Una historia = una pregunta.** Señal de que no captó la reutilización.
4. **Autoevaluación genérica** que no cita nada del audio real ⇒ probable que no se grabó; pedir verificación (que cuente una historia en voz alta).
5. **Historias en español.** Falla C4; el gate es el inglés hablado.
6. **Mejora no accionable** ("estar menos nervioso") ⇒ reconducir a un comportamiento observable.

## Rango de soluciones aceptables

- Cualquier estructura de cadencia (tabla, lista, calendario) cuenta si los bloques son concretos y cubren los 3 formatos.
- Las historias pueden venir de trabajo, proyectos personales o el HomeHub/capstones; lo que importa es S/T/A/R + número + mapeo, no que sean "épicas".
- Es válido que el alumno entregue solo 3 historias (la semilla) con un backlog hacia 8-10; no exijas las 10 en esta entrega.
- La grabación puede ser solo-audio o pantalla+audio; ambas valen mientras la autoevaluación evidencie que se escuchó.
- El formato del mock grabado puede ser cualquiera de los 3; no exijas uno específico.
