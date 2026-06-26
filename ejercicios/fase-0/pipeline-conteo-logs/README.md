# Ejercicio 0.5 — Top 3 de IPs en un log

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.5` Terminal y Linux
**Ruta:** crítica · **Modalidad:** mixto (pipeline + script) · **Timebox:** 35 min

## 🎯 Objetivo

Componer un pipeline de shell que **agregue y rankee** datos de texto, y envolverlo en un script
bash que valide su argumento y use códigos de salida honestos. Al terminar sabrás responder, en
segundos y desde la terminal, "¿quién hizo más peticiones?" sobre cualquier log.

## 📋 Contexto

Leer logs es pan de cada día en backend, DevOps y soporte de producción. "Top 3 IPs por peticiones"
es el ejemplo resuelto de la lección; aquí lo conviertes en una herramienta reutilizable. Es también
exactamente el tipo de pregunta que cae en una entrevista técnica de live coding.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Prueba el pipeline pieza por pieza en la terminal
   antes de pegarlo en el script.
2. Solo entonces consulta **documentación oficial** (`man awk`, `man sort`, `man uniq`).
3. **Solo al final**, usa IA para que te *revise y explique* — nunca para que lo *genere*.
4. Mañana, **reescríbelo de memoria**. Si no te sale, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Mira el archivo de ejemplo `acceso.log` (formato de log web; la IP es la **primera columna**).
2. Abre `resolver.sh` y completa el script para que, dado el log por argumento (`$1`), imprima las
   **3 IPs con más peticiones**, una por línea, en formato `CONTEO IP`, de mayor a menor.
3. Pruébalo:

   ```bash
   bash resolver.sh acceso.log
   ```

4. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `bash resolver.sh acceso.log` imprime exactamente las 3 líneas esperadas (lo verifican los tests).
- [ ] El script empieza con `#!/usr/bin/env bash` y `set -euo pipefail`.
- [ ] **Sin argumento**, el script termina con código de salida distinto de 0 (no se cuelga ni explota feo).
- [ ] Puedes **explicar en voz alta** qué entra y qué sale de cada etapa del pipeline (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Es el ejemplo resuelto de la lección: aísla la primera columna (`awk '{print $1}'`), **ordena**
(`sort`) para juntar iguales, **cuenta** (`uniq -c`), **ordena por conteo descendente** (`sort -rn`)
y **corta** (`head -3`). Lo único nuevo es leer la ruta desde `$1` y validar que venga. Repasa el
esqueleto de script con `set -euo pipefail` y la forma `"${1:?mensaje}"`. Si la salida de `uniq -c`
trae espacios de más adelante, un `awk '{print $1, $2}'` final la normaliza.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-0/pipeline-conteo-logs.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-0/pipeline-conteo-logs.md` — no la mires
antes de intentarlo de verdad.
