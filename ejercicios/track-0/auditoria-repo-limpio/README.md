# Ejercicio T0.6 — Audita y limpia un repo de portafolio

> **Modalidad: diagnóstico/diseño (sin código que ejecutar, sin IA primero).** Este ejercicio entrena
> el ojo que un reclutador técnico usa en segundos: detectar lo que **descalifica** un repo de
> portafolio (un secreto filtrado, un historial ilegible, la falta de README o licencia) y proponer el
> fix correcto —en el orden correcto.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.6` GitHub profesional
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O1** — Auditar un repositorio y detectar problemas de seguridad, legales y de señal.
- **O2** — Proponer el fix concreto de cada problema, con el **orden de pasos** correcto en el caso del
  secreto filtrado.
- **O3** — Reescribir mensajes de commit ruido a **Conventional Commits** bien formados.

## Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 40 min). Lee `repo-a-auditar.md` y diagnostica con tu criterio.
2. Solo entonces consulta la doc oficial (Conventional Commits, Choose a License, gitleaks).
3. **Solo al final**, usa IA para *revisar tu auditoría* —no para *generarla*.
4. Mañana, reescribe de memoria el orden de pasos al descubrir una API key commiteada.

## Tu tarea (en este orden)

Lee `repo-a-auditar.md` (la foto del repo: su `git log`, su árbol y fragmentos). Produce `auditoria.md`:

1. **Lista de problemas** — apunta a **al menos 5**, cada uno clasificado por gravedad:
   - 🔴 **crítico** (riesgo de seguridad o legal),
   - 🟡 **importante** (daña la señal del repo),
   - ⚪ **menor**.
2. **Fix concreto por problema** — el comando o la acción, no una vaguedad. Para el **secreto
   filtrado**, el fix debe incluir el **orden correcto de pasos**: ¿qué es lo PRIMERO que haces?
3. **Reescribe 3 mensajes de commit** del log a **Conventional Commits** (`tipo(scope): descripción`),
   explicando en una frase qué tipo elegiste y por qué.
4. **Veredicto** — en una frase: ¿este repo está listo para pinear en un perfil, o no, y qué falta como
   mínimo?

## Qué entregar (deja este archivo en esta carpeta)

- `auditoria.md` — las 4 secciones completas.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **≥5 problemas** detectados y clasificados por gravedad.
- [ ] El **secreto filtrado** está marcado 🔴 **crítico** y su fix **empieza por rotar la key** (no por
  "borrar el archivo").
- [ ] La **ausencia de `LICENSE`** está identificada con su consecuencia legal (all rights reserved).
- [ ] **3 commits reescritos** como Conventional Commits válidos, con su tipo justificado.
- [ ] Un **veredicto** claro al final.
- [ ] Puedes **explicar la auditoría sin notas** (check de dominio).
- [ ] (Bonus Excelente) mencionas que un escáner de secretos (gitleaks/trufflehog) en CI lo habría
  atrapado antes (conecta con los gates de seguridad de la Fase 5).

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Recorre el repo como lo haría un atacante y luego como un reclutador. Como atacante: ¿hay algo que
**nunca** debería estar en un repo público? (mira el árbol y el log con atención). Como reclutador:
si abres el README, ¿entiendes qué hace el proyecto? ¿El historial cuenta una historia o es ruido?
Para el secreto: recuerda que Git guarda **todo el historial** —borrar el archivo hoy no quita el
secreto de los commits viejos. Por eso el primer paso no es del repo, es de la **key**. Revisa la
sección "Non-examples y misconceptions" de la lección antes de mirar la solución de referencia.

</details>

## Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/auditoria-repo-limpio.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/auditoria-repo-limpio.md` — no la mires
antes de intentarlo de verdad. El corrector evaluará tu **criterio** (que priorices el secreto, que el
fix tenga el orden correcto, que distingas gravedades), no que tu lista coincida palabra por palabra.
