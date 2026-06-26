---
ejercicio_id: fase-2/unit-test-vs-eval-frontera
fase: fase-2
sub_unidad: "2.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — La frontera: unit test, eval o ninguno

## Sección 1 — Clasificación de las 8 afirmaciones

| # | Afirmación | Veredicto | Por qué (una frase) |
|---|---|---|---|
| 1 | El correo está en el prompt enviado | **unit test** | Determinista; un spy (`Mock`) sobre `generar` afirma `correo in call_args.args[0]`. |
| 2 | Parsea un JSON válido al objeto correcto | **unit test** | Con un fake que devuelve un string JSON fijo, el assert verifica tu parser. |
| 3 | Reintenta una vez ante JSON malformado y luego lanza | **unit test** | Un fake que devuelve basura las veces que quieras prueba el bucle de reintento y el error final (idealmente dos tests: "reintenta una vez" y "tras dos fallos lanza"). |
| 4 | El modelo asigna la **categoría correcta** | **eval** | "¿El modelo acierta?" se mide con un dataset etiquetado (correo → categoría) y una métrica (accuracy / F1), no con un assert. |
| 5 | El **resumen** es fiel y no inventa | **eval** | Calidad/fidelidad de texto generado: LLM-as-judge o métrica de faithfulness (Fase 6), no comparación exacta. |
| 6 | Trunca el correo a 8000 caracteres | **unit test** | Lógica pura del código; afirma `len(prompt) <= límite` con una entrada larga, sin tocar el modelo. |
| 7 | Misma `prioridad` exacta en dos llamadas seguidas | **ninguno** | La salida del modelo es no determinista; afirmar igualdad byte a byte es flaky por diseño y no prueba nada útil. |
| 8 | No revela el system prompt ante una inyección | **eval (seguridad)** | Robustez frente a prompt injection (OWASP LLM): se evalúa con muestreo repetido / red-team sobre muchas variantes, no con un solo assert. |

**Resumen de la línea:** 1/2/3/6 empiezan con "¿mi código…?" → **unit test** (tu pegamento, determinista, con fake). 4/5/8 empiezan con "¿el modelo…?" → **eval** (la calidad/robustez del modelo, con dataset y métrica). 7 pide una garantía que el sistema no da → **no se testea**.

## Sección 2 — Diseño de la frontera

**Qué se inyecta y mockea:** la única frontera es `generar(prompt) -> str` (la llamada al LLM: red, costo, no determinismo). En los unit tests se reemplaza por un doble:
- un **stub** (función que devuelve un string fijo) para los casos de parseo, validación y error;
- un **spy** (`Mock(return_value=...)`) cuando hay que afirmar el prompt (afirmación 1) o **contar reintentos** (afirmación 3: `Mock(side_effect=["basura", "basura"])` para dos fallos, o `["basura", '{"...":...}']` para "reintenta una vez y se recupera").

**Qué corre real (NO se mockea):** `json.loads`, la validación de campos, el **truncado** a 8000 chars y el **bucle de reintento**. Son lógica pura del código y es justo lo que se quiere cubrir; mockearlos sería sobre-mockeo y vaciaría los tests de sentido.

**Cómo se ve un eval (afirmación 4):**
- **Entrada:** un dataset etiquetado —decenas/cientos de correos reales con su categoría correcta anotada a mano.
- **Proceso:** correr `triage` (o solo el modelo) sobre cada correo, llamando al **modelo real**.
- **Salida:** un **número** (accuracy, o F1 por categoría) comparado contra un umbral (p. ej. ≥ 0.90).
- **Dónde corre:** **no** en cada commit (es lento y quema tokens), sino como **gate** del pipeline de IA, ocasionalmente. Es "el unit test de la IA": misma función (red de seguridad contra regresiones) pero mide calidad estadística, no corrección puntual. En la Fase 6 lo construyes con herramientas como promptfoo/DeepEval (en CI como gate) y LLM-as-judge para la fidelidad del resumen (afirmación 5).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Afirmación 6 (truncado)** mal clasificada como eval: es código determinista del alumno → unit test claro.
2. **Afirmación 4** "convertida" en unit test mockeando el modelo: el mock devuelve la categoría que el alumno escribió; no prueba que el modelo acierte. Si el alumno cae aquí, es el error conceptual central a corregir.
3. **Afirmación 7**: aceptar "ninguno" o "no testeable de forma útil"; rechazar que se proponga un assert de igualdad. Matiz válido: *sí* podrías afirmar que la prioridad **pertenece al conjunto** {alta, media, baja} (eso es validación de dominio, unit test sobre tu código) — pero **no** que sea idéntica entre dos llamadas.
4. **Afirmación 8**: aceptar "eval" o "eval de seguridad"; lo importante es que reconozca que un solo caso no basta (muestreo repetido / red-team).
5. **Frontera**: penalizar cualquier propuesta de mockear el parser/validación/truncado, o de llamar al modelo real en la suite unitaria.

## Rango de soluciones aceptables
- **Afirmación 3 como uno o dos unit tests**: ambas válidas; dos (reintento + fallo final) es más fino → "excelente".
- **Afirmación 8 como "eval" sin el matiz "seguridad"**: aceptable para "competente"; el matiz OWASP LLM sube a "excelente".
- **Métricas nombradas distintas pero correctas** (accuracy, F1, precision/recall para 4; faithfulness/groundedness/LLM-as-judge para 5): válidas.
- **Sección 2 que además mencione** prompt caching o batching para abaratar el eval: bienvenido, no exigido.
