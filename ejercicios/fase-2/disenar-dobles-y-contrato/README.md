# Ejercicio 2.8 — Diseña la estrategia de dobles y decide dónde va un contrato

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.8` Diseño de tests
**Ruta:** crítica · **Timebox:** 30–45 min · **Modalidad:** diseño (documento, no código ejecutable)

> **Primero-Sin-IA.** Razona el diseño **a mano, sin IA**. La IA solo revisa tu razonamiento al final.
> Este ejercicio no se "corre": se piensa. El entregable es un documento de diseño de tests.

## 🎯 Objetivo

Elegir y **justificar** el test double correcto para cada colaborador de un servicio, distinguir
verificación de **estado** vs. **interacción**, y decidir cuál frontera merece **contract testing**
(no un mock) explicando el modo de falla que un mock oculta.

## 📋 Contexto

En `sistema_bajo_prueba.py` (solo lectura, **no lo ejecutas**) tienes un `ServicioDeReembolsos` que
depende de cuatro colaboradores:

| Colaborador | Qué es | Naturaleza |
|---|---|---|
| `PasarelaDePago` | API HTTP de **otro equipo** que ejecuta el reembolso | red, frontera entre servicios |
| `Reloj` | da la fecha/hora actual | no determinista |
| `EnviadorDeEmail` | manda el comprobante por SMTP externo | efecto sin estado inspeccionable |
| `RepositorioDeReembolsos` | persiste el reembolso (base de datos) | estado consultable |

Diseñar bien qué pones en lugar de cada uno es exactamente la habilidad de la sección 4.3–4.4 de la
lección. Y decidir dónde va un **contrato** es la semilla de la integración de la **Fase 7**.

## 📏 Primero-Sin-IA

1. Lee `sistema_bajo_prueba.py` y entiende qué hace `reembolsar` con cada colaborador.
2. Resuelve el diseño **solo**, a mano. Consulta la lección (secciones 4.3–4.6) y la documentación
   oficial de Pact y `unittest.mock` si lo necesitas — pero **no** generes el documento con IA.
3. **Solo al final**, usa IA para *revisar y cuestionar* tus elecciones.
4. Mañana, reconstruye de memoria la tabla "colaborador → double → por qué".

## 🛠️ Instrucciones — entrega `plan-de-tests.md` con cuatro secciones

1. **Tabla de dobles.** Para **cada** colaborador, decide el double (dummy / stub / spy / mock / fake) y
   justifica en una frase. Al menos uno debe ser **fake** y al menos uno debe verificarse por
   **interacción** (mock/spy); explica por qué *ese* y no otro.
2. **Dos casos en Given-When-Then** (texto, no código): uno de camino feliz y uno de borde (p. ej. un
   reembolso mayor que el cobro original → debe rechazarse y **no** llamar a la pasarela).
3. **Estado vs. interacción.** Para cada uno de tus dos casos, di si la verificación final es de estado o
   de interacción, y por qué.
4. **El contrato.** Identifica **cuál** colaborador merece además un **contract test con Pact** (no un
   mock) y explica en 3–4 frases: qué falla un mock aquí que un contrato sí previene, quién es el
   *consumer* y quién el *provider*, y en qué pipeline corre cada verificación.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los **cuatro** colaboradores tienen double asignado **y justificado** (no "mock para todo").
- [ ] Hay al menos un **fake** y al menos una verificación de **interacción**, ambos justificados.
- [ ] Distingues explícitamente un caso de verificación de **estado** de uno de **interacción**, con el porqué.
- [ ] Tus dos casos están en **Given-When-Then** legible (un product manager los entendería).
- [ ] Señalaste la **`PasarelaDePago`** como candidata a contract testing y explicaste el modo de falla
      que un mock oculta (tu suposición ≠ la realidad del otro lado), consumer/provider y pipelines.
- [ ] Puedes explicar **sin notas** la diferencia entre un contract test y un test de integración end-to-end.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Mapeo guía (no la solución completa): el `Reloj` casi siempre es **stub** (hora fija → determinismo). El
`RepositorioDeReembolsos` es un buen **fake** en memoria y verificas **estado** (el reembolso quedó
guardado). El `EnviadorDeEmail` no tiene estado inspeccionable desde el test → **mock/spy** y verificas
**interacción** (se llamó una vez con el comprobante). La `PasarelaDePago` es la frontera entre **tu**
servicio (consumer) y el de otro equipo (provider): un mock codifica *tu suposición* de su respuesta; si
ellos cambian el JSON, tu mock sigue verde y producción cae — por eso va **contract testing**. Para el
caso de borde, recuerda que "rechaza el reembolso" implica que la pasarela **no** debe llamarse: esa es
una verificación de interacción negativa (`assert_not_called`). Revisa las secciones 4.4 y 4.6 de la
lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `plan-de-tests.md`),
- la **rúbrica**: `.ai/rubricas/fase-2/disenar-dobles-y-contrato.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/disenar-dobles-y-contrato.md` — no la mires
antes de intentarlo de verdad.
