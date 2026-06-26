# 2.9 — Qué NO testear + tu política de umbral honesta

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.9` Coverage vs mutation/behavior
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** razonamiento (sin código)

## 🎯 Objetivo

Tomar decisiones de ingeniería que un entrevistador evalúa de verdad: **qué código
vale la pena testear y cuál no**, y **qué política de calidad** propondrías a un equipo
sin caer en el antipatrón de "coverage ≥ 80% como meta". El producto es tu juicio
escrito y defendible, no un número.

## 📋 Contexto

"Apuntamos a 80% de coverage" suena responsable y es, casi siempre, una mentira
cómoda: premia tests que ejecutan sin verificar y castiga a quien decide —con razón—
no testear un getter. Este ejercicio te obliga a tomar partido y argumentarlo, que es
exactamente lo que harás al documentar el gate de calidad de tu **Capstone F2**.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Decide y justifica con tu cabeza.
2. Solo entonces, consulta la lección y la documentación oficial (mutmut, coverage.py).
3. **Solo al final**, usa IA para *revisar y cuestionar* tus argumentos — no para escribirlos.
4. Mañana, **defiende tu política de memoria** ante la pregunta "¿por qué no me pides 90% de coverage y ya?".

## 🛠️ Instrucciones

### Parte 1 — Qué testear y qué no

Abre `casos.md`: tiene 8 artefactos (A–H) de un backend real. En `decisiones.md`,
para **cada uno**, completa una tabla:

| Caso | Decisión | Justificación (1 frase) |
|---|---|---|
| A | `testear-unitario` / `no-testear` / `testear-en-integración` | … |

La justificación debe anclarse en dos preguntas:
- **¿Puede fallar de una forma interesante?** (¿hay lógica, ramas, bordes, parsing?)
- **¿El test se rompería al refactorizar sin atrapar ningún bug real?** (señal de test de bajo valor)

### Parte 2 — Tu política de calidad

Escribe `politica-cobertura.md` (máx. 1 página): la política que le propondrías a tu
equipo. Tiene que responder, **con argumentos** (no opiniones sueltas):

1. ¿Usamos coverage como **gate** de CI? Si sí, ¿con qué número y por qué ese número
   **no** es una mentira? Si no, ¿cómo usamos coverage entonces?
2. ¿Dónde entra el **mutation testing**? ¿Sobre qué código (todo / solo la lógica crítica)?
3. ¿Con qué **cadencia** corre el mutation testing, dado que es **caro**? (cada PR /
   sobre el diff / nightly). Justifica con el costo.
4. ¿Qué **excluimos** de la medición (código generado, infra) y por qué eso no es trampa?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 8 casos tienen decisión **y** justificación ligada a valor/costo (no "porque sí").
- [ ] La función de IVA (caso C) y el parser (caso F) están marcados como el centro del esfuerzo unitario.
- [ ] El endpoint orquestador (caso H) está marcado como **integración**, no unitario con todo mockeado.
- [ ] Tu política **no** propone "coverage ≥ X" como objetivo ciego; explica Goodhart y qué medir en su lugar.
- [ ] Tu política reconoce el **costo** del mutation testing y propone una cadencia realista.
- [ ] Puedes defender **sin notas** por qué excluir código generado de la métrica no es hacer trampa.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `decisiones.md` — la tabla de los 8 casos con justificación.
- `politica-cobertura.md` — tu política de calidad (máx. 1 página).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Heurística para clasificar: testea unitariamente lo que tiene **lógica que puede
equivocarse y es tuya** (C: tramos de IVA; F: parsing con bordes y errores). No
testees unitariamente lo (a) trivial sin lógica (A getter, E DTO generado), (b)
responsabilidad de otra librería ya probada (B wrapper de `requests`: testearlo prueba
`requests`, no tu código), o (c) infraestructura (D logging, G `__main__`). El
orquestador (H) se prueba en **integración**: mockear los tres servicios y verificar
"que se llamaron" solo prueba tus mocks, no que el flujo funcione.

Para la política, ancla en la lección: coverage como **diagnóstico de mínimos** (mira
el 0%, no celebres el 90%), mutation score como medida de **fuerza** sobre la lógica
crítica, y costo → **nightly o sobre el diff**, no en cada push. Excluir código
generado no es trampa porque no es *tu* lógica: medirlo infla el número sin medir
calidad real. Pista, no solución: el argumento tienes que construirlo tú.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `decisiones.md` + `politica-cobertura.md`),
- la **rúbrica**: `.ai/rubricas/fase-2/que-no-testear-y-umbral.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/que-no-testear-y-umbral.md`
— no la mires antes de intentarlo de verdad.
