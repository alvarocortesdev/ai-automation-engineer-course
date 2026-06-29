---
ejercicio_id: track-0/evidencia-ai-augmented
fase: track-0
sub_unidad: "T0.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **diseño/razonamiento**: el reframe de cada alumno será distinto. Lo que se mide es el **criterio**
> (framing honesto + evidencia abrible), no la redacción exacta.

# Solución de referencia — Reframe + mapa de evidencia

## 1. Diagnóstico del framing (referencia)

La autodescripción cae de lleno en el cuadro **vibe-coder**: todo el peso está en **velocidad** ("5x o
10x", "rapidísimo") y en **delegación total** ("ya casi no escribo código a mano", "la IA lo hace mejor
que yo"), sin una sola mención al **criterio** con que verifica el output. Eso resta en una entrevista
2026 por tres motivos: (a) suena a alguien **gobernado por** la herramienta, no a alguien que la gobierna;
(b) es **indefendible** —si le piden explicar una línea con la IA apagada, no tiene cómo respaldar su
"ventaja"; y (c) ya tuvo el costo real (el bug de zonas horarias que pegó sin revisar) que confirma la
debilidad. Lo más irónico: el candidato **tiene** material de criterio de sobra (sabe programar, resolvió
a mano antes, escribió la lógica de pagos sin IA a propósito) pero lo **esconde** porque cree que admitir
un "aquí no usé IA" lo hace ver mal. Es exactamente al revés: ahí está su mejor evidencia.

## 2. Narrativa reescrita (referencia, framing AI-augmented honesto)

> *"Trabajo AI-augmented, pero la idea clave es que **dirijo** la IA y respondo por cada línea, no que la
> IA programe por mí. En mis proyectos escribo el spec y los tests yo —defino qué significa 'funciona'
> antes de delegar—, dejo que el agente proponga la implementación, y la reviso contra esos tests; cuando
> sugiere algo que no convence, lo rechazo y lo dejo anotado. Para las partes con IA no me fío de que 'se
> vea bien': mido la salida con un set de casos. Y sé cuándo NO usarla: la lógica de cobro de un sistema de
> pagos la escribí a mano a propósito, porque ahí el costo de un error supera lo que ahorro delegando. La
> uso para multiplicar, no para pensar por mí —por eso puedo defender mi código contigo sin la IA al
> lado."*

Por qué funciona: el eje es **criterio**, no velocidad (no aparece "10x"); cada afirmación es
**verificable** en un repo; reincorpora el dato escondido (pagos sin IA) **como fortaleza**, no como
confesión; y cierra conectando con **Primero-Sin-IA**. No sobrevende ni oculta.

## 3. Mapa de evidencia (referencia)

| Músculo | Artefacto concreto y abrible | ¿Existe / a crear? |
|---|---|---|
| Spec-driven | un `spec.md` o mini-spec commiteado **antes** del primer commit de implementación (se ve en el historial: el spec precede al código). | a crear: adoptar el hábito en el próximo capstone |
| Agentic + review | un PR donde el historial muestra spec → tests rojos → implementación, con comentarios de review propios; un ADR titulado p. ej. *"rechazo cachear el token en memoria del proceso (rompe con varios workers)"*. | a crear: el ADR de rechazo es el más demostrativo |
| Evals | un directorio `evals/` con `dataset.jsonl` (casos etiquetados) + un número (p. ej. faithfulness) + el **gate** en el workflow de CI que falla si baja del umbral. | a crear en el capstone de IA (F6/F7) |
| Cuándo-NO | un ADR titulado *"la lógica de cobro se implementa sin asistente de IA: el costo de un error en pagos supera el ahorro"* —documenta la decisión de **no** delegar. | **ya vivido** (la lógica de pagos a mano): falta solo escribir el ADR |
| (meta) | el propio repo del curso: commits Primero-Sin-IA + write-ups honestos que dicen dónde usó IA y dónde no. | ya existe (es el repo de estudio) |

## 4. Músculo más débil (referencia)

El más débil suele ser **evals**: el candidato "se daba cuenta si estaba mal mirando", nunca midió una
salida de LLM con un set de casos. Plan accionable: en el próximo proyecto con IA, armar un `dataset.jsonl`
de 30–60 casos etiquetados, calcular un número y agregar el gate en CI. Hasta que ese artefacto exista,
**no** vender el músculo de evals en la entrevista —vender solo lo que puede abrir.

## Puntos donde el corrector debe mirar
1. **Eje del reframe.** Si sigue siendo velocidad/productividad ("muy rápido", "muy productivo") en vez de
   criterio, el alumno no captó el punto.
2. **Ocultar vs. vender el cuándo-NO.** Si el reframe esconde el "no usé IA en pagos" o no recupera ese
   dato, perdió su mejor evidencia.
3. **Abribilidad del mapa.** Cualquier celda con una cualidad abstracta ("código limpio") en vez de un
   archivo/commit/ADR concreto = no entendió "evidencia verificable".
4. **Honestidad del músculo débil.** Debe ser coherente con el mapa y traer un plan, no un "ninguno, soy
   fuerte en todos" (señal de Dunning-Kruger).

## Rango de soluciones aceptables
- Cualquier reframe es válido mientras el eje sea **criterio** (no velocidad), sea verificable, y no
  sobrevenda ni oculte. La redacción exacta es libre.
- El mapa puede listar artefactos distintos a los de referencia siempre que sean **abribles y específicos**
  y cubran los **4 músculos**. "A crear" es aceptable si dice dónde.
- El músculo débil puede ser otro (spec-driven, cuándo-NO…) según el perfil real del alumno; lo no válido
  es "ninguno".
- Conectar con Primero-Sin-IA y enlazar un artefacto que ya exista son bonus de Excelente, no obligatorios
  para Competente.
- Entregar en inglés suma el bonus del hilo; en español es aceptable.
