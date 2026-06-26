# Ejercicio 0.5 — Consulta JSON con jq

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.5` Terminal y Linux
**Ruta:** crítica · **Modalidad:** código (pipeline jq) · **Timebox:** 30 min

## 🎯 Objetivo

Filtrar y transformar JSON desde la terminal con `jq`. JSON es el idioma de las APIs y de casi toda
respuesta de un LLM; saber recortarlo en una línea —sin escribir un programa— es un superpoder diario.

## 📋 Contexto

Cuando llames a una API (Fase 1) o a un modelo de IA (Fase 6), te devuelven JSON. `curl ... | jq ...`
es el reflejo que separa al que improvisa del que extrae justo el dato que necesita. Aquí trabajas
sobre un archivo fijo para que el resultado sea **reproducible**; en la vida real ese JSON vendría de
`curl https://api.ejemplo.com/usuarios | ./consulta.sh /dev/stdin`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano. Construye el filtro `jq` por partes en la terminal antes de pegarlo.
2. Solo entonces consulta el **manual oficial** de jq: <https://jqlang.github.io/jq/manual/>.
3. **Solo al final**, usa IA para *revisar*, no para *generar*.
4. Mañana, **reescríbelo de memoria**.

## 🛠️ Instrucciones

Tienes `usuarios.json`: una lista de objetos con campos `nombre`, `activo` (bool), `rol` y `logins`.

Completa `consulta.sh <archivo.json>` para que imprima los **nombres de los usuarios activos con más
de 5 logins**, ordenados alfabéticamente, **uno por línea** y **en crudo** (sin comillas JSON).

Instala `jq` si no lo tienes:

```bash
brew install jq      # macOS
sudo apt install jq  # Debian/Ubuntu
```

Pruébalo y corre los tests:

```bash
bash consulta.sh usuarios.json
uv run pytest        # o:  pytest
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `bash consulta.sh usuarios.json` imprime exactamente `Ana` y `Carla`, en ese orden, uno por línea.
- [ ] La salida es **en crudo** (pista: `jq -r`), apta para encadenar en otro pipeline.
- [ ] Filtras por **dos condiciones a la vez** (activo Y más de 5 logins) y ordenas por nombre.
- [ ] Puedes **explicar sin notas** qué hace `select(...)` y por qué `jq -r` y no `jq` a secas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`jq` tiene `map(select(condición))` para quedarte con los elementos que cumplen, `and` para combinar
condiciones (`.activo and .logins > 5`), `sort_by(.campo)` para ordenar, y `.[].campo` para extraer un
campo de cada elemento. La bandera `-r` (raw) quita las comillas de los strings. Lee la ruta del
archivo desde `$1`.

</details>

## 🤖 Cómo pedir la corrección

Entrega a tu IA: tu solución (este directorio), la **rúbrica** `.ai/rubricas/fase-0/json-con-jq.md` y
`.ai/INSTRUCCIONES-CORRECTOR.md`. La **solución de referencia**
(`.ai/soluciones/fase-0/json-con-jq.md`) no se mira antes de intentarlo de verdad.
