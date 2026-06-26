---
ejercicio_id: fase-0/commit-msg-hook
fase: fase-0
sub_unidad: "0.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Prohibido pegar o parafrasear de forma reconstruible el script. Úsala solo para detectar el error, nombrar la misconception y calibrar las pistas (ver `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Construye el hook commit-msg

## Respuesta canónica (hook completo)

```bash
#!/usr/bin/env bash
set -euo pipefail

msg_file="$1"

# Cabecera: primera línea no vacía que no empiece con '#'.
header="$(awk 'NF==0 {next} /^#/ {next} {print; exit}' "$msg_file")"

# 1) Deja pasar los mensajes autogenerados por Git (merge/revert).
if printf '%s' "$header" | grep -qE '^(Merge|Revert) '; then
  exit 0
fi

# 2) Conventional Commits: <type>[(scope)][!]: <descripción>
pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9._/-]+\))?(!)?: .+$'

if printf '%s' "$header" | grep -qE "$pattern"; then
  exit 0
fi

# 3) Inválido: ayuda a stderr y abortar.
cat >&2 <<'EOF'
✖ Mensaje de commit inválido (Conventional Commits).

  Formato:  <type>[(scope)][!]: <descripción>
  Ejemplos: feat(auth): añade login con OAuth2
            fix: corrige off-by-one en el paginador
            docs!: reescribe el README (breaking change)

  Tipos válidos: feat fix docs style refactor perf test build ci chore revert
EOF
exit 1
```

Instalación compartible (versionada):

```bash
mkdir -p .githooks && cp commit-msg .githooks/ && chmod +x .githooks/commit-msg
git config core.hooksPath .githooks
```

## Razonamiento (por qué cada pieza)

- **`$1` es una ruta, no el texto.** Git pasa el archivo del mensaje (`.git/COMMIT_EDITMSG`). Hay que leerlo.
- **`awk` para la cabecera:** lee el archivo directo, salta líneas vacías y comentarios (`#`, que Git añade en el editor) y devuelve la primera línea real. Evita el patrón frágil `grep … | head -1`, que con cuerpos multilínea y `set -o pipefail` puede morir por SIGPIPE.
- **Guard de `Merge`/`Revert` primero:** esos mensajes los genera Git y no siguen Conventional Commits; bloquearlos rompería `git merge`/`git revert`.
- **La regex, anclada `^…$`:**
  - `(feat|fix|...)` — alternancia de tipos válidos.
  - `(\([a-z0-9._/-]+\))?` — scope **opcional**; los paréntesis literales van escapados `\(` `\)` porque en ERE (`grep -E`) `(` es agrupación.
  - `(!)?` — breaking change opcional.
  - `: .+$` — exige `:`, un espacio y **al menos un carácter** de descripción.
- **Salida:** `exit 0` acepta; `exit 1` (≠0) hace que Git aborte. La ayuda va a **stderr** (`>&2`), no a stdout.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Regex sin anclar** (`^…$`): sin anclas, "feat" haría match dentro de cualquier palabra. Error #1.
2. **Paréntesis del scope sin escapar:** `(parser)` con `(` sin `\(` cambia el significado del patrón.
3. **No exigir descripción:** olvidar `.+` tras `: ` deja pasar `feat:` y `feat: ` vacíos.
4. **Ayuda a stdout:** debe ir a stderr; un test lo verifica.
5. **Olvidar el guard de merge/revert:** dos tests fallan y, peor, rompe merges reales.
6. **"Arreglar" editando los tests** en vez del hook: anti-patrón a marcar de inmediato.

## Rango de soluciones aceptables

- **Otro lenguaje:** el hook puede estar en Python/Node en vez de Bash, siempre que lea `$1` (la ruta), valide y use el código de salida. Cuenta como `competente`/`excelente` si está limpio.
- **Límite de longitud:** acotar la descripción (`.{1,72}$` en vez de `.+$`) es una mejora válida y defendible; no es obligatorio porque los tests no lo exigen. Si lo añade, debe seguir aceptando los mensajes válidos del contrato.
- **Extracción de la cabecera:** `sed -n '/^[^#]/{p;q}'` o equivalentes son aceptables si manejan bien comentarios y líneas vacías sin romperse con cuerpos multilínea.
- **Caso de scope vacío** (`feat(): x`): el patrón de referencia lo **rechaza** (`+` exige ≥1 char dentro del scope). Aceptarlo o rechazarlo es defendible si el alumno lo prueba y justifica.
- **Conciencia de `--no-verify` + CI:** mencionar que el hook se puede saltar y que la validación debe repetirse en CI es señal de nivel `excelente` (no exigido para `competente`).
