# Ejercicio 1.10 — Tu primer LLM en una mini-CLI (testeable, con la key a salvo)

> **Modalidad: código.** Tu primera victoria de IA real, hecha como ingeniero: la API key fuera
> del código, el input validado antes de gastar una llamada, los fallos del SDK mapeados a errores
> claros, y todo **testeable sin red ni tokens** gracias al seam de inyección de 1.5.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.10` Primer llamado a un LLM + mini-CLI
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Construir una mini-CLI: `python solucion.py "¿qué es un embedding?"` le manda la pregunta a un LLM
y te imprime la respuesta. Pero con los hábitos que separan un script de juguete de código que
aguanta: secreto en variable de entorno, validación previa, errores de dominio, y un seam que deja
los tests corriendo offline.

## 📋 Contexto

Esta es la primitiva sobre la que se construye todo el curso de IA (agentes, RAG, automatización):
un programa que arma un mensaje, lo manda a un modelo por API, recibe texto y decide qué hacer. El
seam de inyección que practicas aquí es el mismo que hará testeable tu capstone, y el reflejo de
"secretos en el entorno" se aplica a cualquier credencial.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** (Anthropic Get Started, sección 9 de la lección).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa las cuatro funciones (no cambies sus firmas):
   - `leer_api_key(entorno)` — lee `ANTHROPIC_API_KEY` del mapping; lanza `FaltaApiKey` si falta o
     está vacía. **Nunca imprime la key.**
   - `responder(prompt, preguntar_al_modelo)` — valida el prompt (vacío/solo espacios → `PromptVacio`,
     **antes** de llamar) y delega en el modelo inyectado; devuelve el texto sin espacios sobrantes.
   - `preguntar_a_claude(prompt)` — la llamada **real** con el SDK `anthropic` (importado **dentro**
     de la función): cliente, `messages.create` (modelo, `max_tokens`, mensaje), devuelve
     `content[0].text`. Mapea `anthropic.AuthenticationError → FaltaApiKey` y
     `anthropic.APIError → ModeloInalcanzable`.
   - `main(argv, entorno, preguntar=...)` — arma el prompt desde `argv`; sin prompt → `stderr` + `2`;
     falta key → `3`; `ModeloInalcanzable` → `4`; éxito → imprime y `0`.
2. Corre los tests (no necesitas red, ni key, ni el paquete `anthropic` instalado):

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_solucion.py` (un caso borde que se te ocurra).

### Victoria real (opcional — necesita una API key)

Para ver el modelo responder de verdad:

```bash
pip install anthropic            # o: uv add anthropic
export ANTHROPIC_API_KEY="sk-ant-..."   # tu key de console.anthropic.com — NO la commitees
python solucion.py "explícame qué es un embedding en una frase"
```

El costo es de **centavos** con `claude-haiku-4-5`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La API key se lee del entorno; **no** aparece hardcodeada ni se imprime nunca.
- [ ] Prompt vacío → `PromptVacio` y el modelo **no** se llama (no gastas una llamada en input inválido).
- [ ] `leer_api_key` lanza `FaltaApiKey` cuando la variable falta o está vacía.
- [ ] Los fallos del SDK se mapean a errores de dominio; `main` los traduce a códigos de salida distintos (2/3/4).
- [ ] Todos los tests pasan **sin red ni key real** y agregaste al menos uno propio.
- [ ] Puedes **explicar sin notas** por qué inyectar el modelo hace el código testeable y por qué la key va en el entorno.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa el **contrato** primero (spec-first, de 0.8): qué entra, qué sale, qué errores.
`leer_api_key` es `entorno.get("ANTHROPIC_API_KEY", "").strip()` y, si queda vacío, `raise FaltaApiKey(...)`.
`responder` valida con `if not prompt or not prompt.strip(): raise PromptVacio` **antes** de
`return preguntar_al_modelo(prompt).strip()`. `preguntar_a_claude` envuelve `messages.create` en
`try/except anthropic.AuthenticationError / anthropic.APIError` (importa `anthropic` **dentro** de la
función). `main` ordena las guardas: prompt vacío → `2`; `leer_api_key` (FaltaApiKey) → `3`;
`responder` con `except ModeloInalcanzable` → `4`; éxito → imprime y `0`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/primer-llm-mini-cli.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/primer-llm-mini-cli.md` — no la mires
antes de intentarlo de verdad.
