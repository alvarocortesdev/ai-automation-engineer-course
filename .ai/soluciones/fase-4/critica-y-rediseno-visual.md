---
ejercicio_id: fase-4/critica-y-rediseno-visual
fase: fase-4
sub_unidad: "4.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ejercicio de **razonamiento**: no
> existe una única redacción correcta. Esta es una **referencia ejemplar** + el criterio para juzgar
> otras. El alumno puede nombrar problemas distintos y estar `excelente` si la heurística es correcta y la
> corrección es defendible.

# Solución de referencia — Crítica de diseño

## Diagnóstico canónico (ejemplo de entrega "excelente")

> Cada entrada: problema · palanca · heurística violada · corrección.

1. **Todo el texto (encabezado, intro, títulos de sección, etiquetas) está en 18px bold.**
   · Palanca: **jerarquía/tipografía** · Heurística: sin contraste de tamaño/peso, nada destaca (la
   jerarquía es contraste relativo). · Corrección: escala tipográfica de 3 niveles (p. ej. título de
   página 24–28px bold; títulos de sección 20px bold; etiquetas 16px regular; ayuda 14px). Solo lo
   importante en bold.

2. **El párrafo de intro ocupa todo el ancho (≈180 caracteres por línea) con `line-height: 1.0`.**
   · Palanca: **tipografía** · Heurística: longitud de línea fuera del rango legible (45–75 caracteres) e
   interlineado insuficiente. · Corrección: `max-width` ~60–70ch al contenedor y `line-height: 1.5` al
   texto de cuerpo.

3. **Las etiquetas están centradas; los campos, a la izquierda; el botón, a la derecha.**
   · Palanca: **layout/alineación** · Heurística: múltiples ejes de alineación → el ojo lee desorden.
   · Corrección: alinear etiquetas, campos y acciones a un único borde izquierdo (o un grid de formulario
   consistente).

4. **La etiqueta "Selecciona el modelo" está a 5px del título de sección de arriba y a 22px de su propio
   campo de abajo.** · Palanca: **espaciado** · Heurística: **ley de proximidad** invertida (lo
   relacionado debe estar más cerca que lo no relacionado). · Corrección: invertir los espacios: la
   etiqueta pegada a su campo (p. ej. 4–8px) y más separación (24–32px) entre secciones. Usar una escala
   base-4/8 en vez de 5/13/22/30px sueltos.

5. **El texto de ayuda es `#c4c4c4` sobre blanco.** · Palanca: **color** · Heurística: contraste por
   debajo de WCAG AA (≈1.9:1, exige 4.5:1). · Corrección: oscurecer a ≥ 4.5:1 (p. ej. `#595959`).

6. **El error solo se comunica con el borde del input en rojo (sin ícono ni texto).** · Palanca: **color**
   · Heurística: "no usar el color como único medio para transmitir información" (WCAG SC 1.4.1). ·
   Corrección: añadir ícono + mensaje de texto describiendo el error, además del color.

7. **Cuatro colores de acento (azul/verde/naranja/morado) compitiendo.** · Palanca: **color** ·
   Heurística: paleta sin disciplina (regla 60-30-10: un acento dominante). · Corrección: una base neutra
   + **un** acento para la acción primaria; los semánticos (éxito/error) reservados a su función.

8. **El botón primario "Guardar" usa `#dcdcdc`/`#9a9a9a` — se ve deshabilitado.** · Palanca:
   **jerarquía (de acciones)/color** · Heurística: la acción primaria debe ser la más prominente; aquí es
   la menos visible y además su texto no pasa contraste. · Corrección: "Guardar" con el color de acento
   sólido y texto que pase 4.5:1; "Restablecer" como acción secundaria (texto/borde, menos peso).

## Top-3 priorizado (ejemplo)
1. **#5 (texto de ayuda `#c4c4c4`) y #8 (botón primario ilegible)** — fallan **ambos ejes**: rompen
   accesibilidad (contraste) *y* legibilidad/jerarquía de acciones. Inarreglable a ojo: hay que medirlo.
2. **#1 (sin jerarquía tipográfica)** — rompe lo más básico: el usuario no sabe qué leer ni qué es cada
   cosa. Alto impacto en toda la pantalla.
3. **#4 (proximidad invertida)** — confunde qué etiqueta va con qué campo; error funcional, no estético.

> El criterio de priorización es ponderar dos ejes: **legibilidad/jerarquía** (¿sé qué leer y hacer?) y
> **accesibilidad** (¿pasa contraste? ¿depende solo del color?). Lo que falla ambos va primero.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **Diagnosticar = nombrar la causa, no el síntoma.** "El texto se pierde" es síntoma; "longitud de línea
   sin `max-width` + `line-height: 1.0`" es la causa nombrable.
2. **Las cinco palancas son una checklist, no intuición.** Recorrer una por una encuentra lo que la mirada
   "general" salta.
3. **Accesibilidad y diseño visual se tocan en el color.** Contraste e "información solo por color" son
   ambas cosas: estética y a11y a la vez.
4. **Priorizar es ingeniería, no gusto.** Se justifica por impacto medible en dos ejes.

## Puntos resbalosos (donde el corrector debe mirar)
- Que el alumno **detecte ambos** problemas de contraste (texto de ayuda **y** botón primario), no solo uno.
- Que marque la falla de **"información solo por color"** (#6): es la más fácil de pasar por alto y la más
  reveladora de criterio de accesibilidad.
- Que la priorización use los **dos ejes**, no "el que más le molesta".
- Que las correcciones tengan **valores/reglas** (umbral 4.5:1, escala base-4, rango 45–75 ch), no "más
  contraste" a secas.

## Rango de soluciones aceptables
- El alumno puede agrupar o separar problemas distinto (p. ej. tratar todos los de color como uno con
  sub-puntos) y seguir siendo `excelente` si la heurística es correcta en cada caso.
- Valores de corrección distintos a los del ejemplo cuentan si respetan los umbrales (contraste ≥ 4.5:1
  para texto, escala consistente, longitud de línea en rango).
- El top-3 puede diferir mientras la **justificación por impacto** sea sólida; no hay un único orden
  correcto, pero los dos problemas de contraste/legibilidad casi siempre deberían entrar.
