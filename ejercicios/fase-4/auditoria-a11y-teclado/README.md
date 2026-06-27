# Ejercicio 4.4 — Auditoría de accesibilidad: traza el foco y nombra el SC violado

> **Modalidad: a-mano (razonamiento/diagnóstico).** No hay test ni código que escribir: entregas un
> `auditoria.md`. Resuélvelo **Primero-Sin-IA**: el músculo que entrena es *ver el problema y nombrarlo con
> el vocabulario del estándar*, justo lo que hace un buen revisor en code review.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.4` Accesibilidad WCAG 2.2
**Ruta:** crítica · **Timebox:** 30–35 min

## 🎯 Objetivo

- **O1** — Trazar el **orden de foco** de la pantalla a mano e identificar elementos **inalcanzables** y
  **trampas de foco**.
- **O2** — Diagnosticar cada problema nombrando el **Success Criterion concreto de WCAG 2.2** que viola.
- **O3** — Distinguir **ARIA mal usada** de HTML semántico correcto y **priorizar** los arreglos por impacto.

## 📋 Contexto

Lee `pantalla-a-auditar.md`: es la descripción de un "Panel de revisión de documentos con IA" que funciona
con mouse pero está plagado de problemas de accesibilidad (orden de foco roto, trampa de foco en un modal,
ARIA que miente, contraste, alt, error no anunciado, foco invisible, target size, foco tapado por header).
Tu trabajo es **auditarlo por escrito**, no arreglarlo en código.

## 📏 Primero-Sin-IA

1. Audítalo **solo**, a mano (timebox arriba). Documentación oficial permitida (lista de SC de WCAG 2.2).
2. Recorre la pantalla con una **checklist de SC**, una por una, en vez de mirar "en general".
3. **Solo al final**, usa IA para *revisar* tu auditoría — no para *generarla*.
4. Mañana, intenta **nombrar los SC de memoria** sobre la misma pantalla. Si no te salen los números, no
   los internalizaste: vuelve a la sección 4 de la lección.

## 🛠️ Instrucciones

Crea un `auditoria.md` con tres partes:

1. **Orden de foco trazado.** Lista, en orden, qué elemento recibe foco al pulsar `Tab` repetidamente
   (considera el efecto de los `tabindex` positivos). Marca qué elementos son **inalcanzables** con teclado
   y dónde hay una **trampa de foco**.
2. **Problemas diagnosticados.** Para cada problema (al menos **cinco** distintos): `problema · SC violado
   (con número) · corrección accionable`. Si la corrección correcta es "usar HTML nativo en vez de ARIA",
   dilo explícitamente.
3. **Top-3 priorizado.** Si solo pudieras arreglar tres, ¿cuáles y por qué? Justifica por **impacto**
   (¿bloquea por completo a alguien, o solo molesta?), no por orden de aparición.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Trazaste el **orden de foco** completo y marcaste inalcanzables + la trampa de foco.
- [ ] Diagnosticaste **≥ 5 problemas**, cada uno con su **SC de WCAG 2.2 (número correcto)** y una
      corrección accionable.
- [ ] Identificaste al menos un caso de **ARIA mal usada** (rol que miente o ARIA redundante) y explicaste
      por qué empeora las cosas.
- [ ] El **top-3** está justificado por impacto (bloquea vs. molesta), no por orden.
- [ ] Puedes **defender tu auditoría sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Pasa esta checklist de SC por la pantalla, uno por uno: teclado operable (2.1.1), sin trampa de foco
(2.1.2), foco visible (2.4.7), foco no tapado (2.4.11), nombre/rol/valor (4.1.2), mensajes de estado
anunciados (4.1.3), info y relaciones / label (1.3.1), contraste de texto (1.4.3), uso del color (1.4.1),
texto alternativo (1.1.1), target size (2.5.8). Para el orden de foco: sigue el DOM, **salvo** que haya
`tabindex` positivos, que se tabulan primero en orden numérico (1, 2, ...) y luego el resto en orden de
DOM — eso ya es de por sí un problema. Para priorizar: lo que **impide usar** una función (trampa de foco,
control inalcanzable, contraste ilegible) pesa más que lo que solo molesta. Esto es una pista, no la
solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `auditoria.md`,
- la **rúbrica**: `.ai/rubricas/fase-4/auditoria-a11y-teclado.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-4/auditoria-a11y-teclado.md` — no la mires antes
de intentarlo de verdad.
