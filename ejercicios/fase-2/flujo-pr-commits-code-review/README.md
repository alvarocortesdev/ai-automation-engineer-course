# Ejercicio 2.13 — Reescribe el historial: Conventional Commits + PR + code review

> **Modalidad: razonamiento/comunicación (sin IA primero).** No se corrige con tests verdes: se corrige
> con la **calidad de tu comunicación de ingeniería** — commits legibles, una descripción de PR que le
> ahorra trabajo al revisor, y un code review que mejora el código sin atacar a la persona.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.13` Colaboración, spec-driven dev y ADRs
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Convertir el material crudo de un PR (un historial de commits horrible y el diff de un compañero) en
trabajo profesional: **Conventional Commits** correctos (incluido marcar lo que rompe compatibilidad),
una **descripción de PR** con por qué/cómo probarlo, y un **code review** etiquetado por intención que
separe lo que bloquea de lo que es preferencia e identifique el bug plantado en el diff.

## 📋 Contexto

En un equipo, tu historial de commits es documentación, tu descripción de PR es respeto por el tiempo
del revisor, y tu code review es donde se transfiere criterio. Hacer las tres bien es lo que te vuelve
alguien en quien se confía un repo. Este ejercicio te da material realista y te pide profesionalizarlo.

Material de entrada en esta carpeta (no lo edites, es el input):
- `historial-malo.md` — los 5 mensajes de commit a reescribir.
- `diff-a-revisar.md` — el cambio de un compañero que vas a revisar (tiene un bug plantado y algo bien hecho).

## 📏 Primero-Sin-IA

1. Hazlo **solo**, a mano, dentro del timebox. Decide tú los tipos, redacta tú los comentarios.
2. Solo entonces relee las secciones 4.4–4.6 de la lección (commits, PR, review) y los recursos oficiales.
3. **Solo al final**, usa IA para *cuestionar* tu review —no para escribirlo.
4. Mañana, reescribe los 5 commits **de memoria**. Si no te sale cuál es `BREAKING CHANGE`, repasa.

## 🛠️ Instrucciones

1. **`commits.md`** — reescribe los 5 mensajes de `historial-malo.md` como Conventional Commits válidos
   (`tipo(scope): descripción en imperativo, minúscula, sin punto`). **Marca el que rompe
   compatibilidad** con `!` o footer `BREAKING CHANGE:`. Si un mensaje mezcla dos cosas, dilo.
2. **`pr.md`** — escribe la descripción del PR con secciones **Qué / Por qué / Cómo probarlo /
   Trade-offs**, enlazando un issue ficticio con `Closes #42`.
3. **`review.md`** — da el code review sobre `diff-a-revisar.md`: **3-4 comentarios**, cada uno
   etiquetado (`praise` / `issue` / `suggestion` / `question`) y marcando si **bloquea** o no.
   - Al menos **un `issue` bloqueante real** (hay un bug plantado en el diff: encuéntralo).
   - Al menos **un `praise` concreto** (hay algo bien hecho: nómbralo, no "buen trabajo" genérico).

> 💡 Comenta el **código**, no a la persona ("esto lanza X cuando Y", no "no pensaste en Y").
> Etiqueta la intención y separa lo que **debe** arreglarse de lo que es opinión.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 5 commits tienen **tipo válido** + descripción en **imperativo**; el que cambia el contrato del cupón lleva `!`/`BREAKING CHANGE`.
- [ ] `pr.md` explica el **por qué** (no solo el qué) y dice **cómo probarlo**.
- [ ] Los comentarios del review **comentan el código, no a la persona**, y están **etiquetados** por intención.
- [ ] Separas lo que **bloquea** de lo que es preferencia, e **identificaste el bug plantado**.
- [ ] Hay al menos un `praise` **concreto**.
- [ ] Puedes explicar **sin notas** por qué un PR pequeño se revisa mejor que uno grande.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `commits.md` — los 5 commits reescritos.
- `pr.md` — la descripción del PR.
- `review.md` — tu code review (3-4 comentarios etiquetados).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para los commits, pregúntate por cada uno: ¿agrega funcionalidad (`feat`), arregla un bug (`fix`), o es
mantenimiento (`chore`/`build`)? El que dice "cupón inválido ahora tira error en vez de aplicar 0"
**cambia el comportamiento observable para quien llama** → es breaking (`!` o `BREAKING CHANGE:`). El de
"subo deps y arreglo lint" mezcla dos cosas: idealmente dos commits. Para el review, recorre el diff
buscando un cálculo sospechoso: ¿el descuento usa el porcentaje en la escala correcta? ¿qué pasa con un
total que se vuelve negativo? El `praise` está en el test (mira qué cubre). Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tus `commits.md`, `pr.md` y `review.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/flujo-pr-commits-code-review.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/flujo-pr-commits-code-review.md` — no la
mires antes de intentarlo de verdad.
