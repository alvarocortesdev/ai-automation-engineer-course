---
ejercicio_id: fase-0/capstone-cli-sin-ia
fase: fase-0
sub_unidad: "0.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Capstone Fase 0: CLI sin IA

## Aviso de uso para el corrector

Este capstone **no tiene una única respuesta correcta**: el alumno elige su propio
problema, su diseño y su herramienta. Lo de abajo es **un** proyecto ejemplar que
alcanza el nivel `excelente` —una **vara de medir**, no la solución a copiar—.
**No exijas que el alumno haya hecho *este* proyecto.** Evalúa su entrega contra la
rúbrica (`.ai/rubricas/fase-0/capstone-cli-sin-ia.md`) usando este ejemplo solo
para calibrar qué se ve como "disciplina completa": spec antes del código, ADR,
exit codes honestos, README con demo y Conventional Commits.

> Lo esencial a verificar no es el problema elegido, sino: **¿la spec llegó antes
> del código? ¿hay un ADR real? ¿los exit codes y los flujos stdout/stderr son
> honestos? ¿el historial es Conventional Commits por pasos? ¿puede explicarlo todo
> sin notas?** Un proyecto distinto que cumpla todo eso es igual de `excelente`.

---

## Proyecto ejemplar: `bitacora` (bitácora de estudio)

Una herramienta que el alumno usaría de verdad: registra sesiones de estudio y las
resume por semana. Resoluble 100% con lo de la Fase 0 (funciones, `dict`/`list`,
validación, `argparse`, JSON, terminal).

### 1. `SPEC.md` (escrita ANTES de codear)

```text
# SPEC — bitacora

Propósito: registrar sesiones de estudio y resumir minutos por semana, desde la terminal.

Comandos:
  bitacora add "<tema>" --min <n>   registra una sesión (tema + minutos)
  bitacora resumen                  suma minutos por semana ISO

Entrada:
  tema:  texto no vacío (argv)
  --min: entero positivo (argv)
  almacenamiento: JSON en $BITACORA_FILE (default ~/.bitacora.json)

Salida:
  stdout: confirmación al registrar; el resumen "AAAA-Sxx: N min" por semana
  stderr: errores de validación y de datos
  exit:   0 éxito · 2 uso incorrecto · 1 error de ejecución

Casos borde:
  - tema vacío / solo espacios   -> error a stderr, exit 2
  - --min <= 0                    -> error a stderr, exit 2
  - --min faltante                -> argparse: uso a stderr, exit 2
  - archivo de datos no existe    -> NO es error: se trata como vacío / se crea
  - resumen sin sesiones          -> mensaje informativo, exit 0
  - archivo JSON corrupto         -> error claro a stderr, exit 1
```

### 2. `docs/ADR-0001-almacenamiento-json.md`

```text
# ADR-0001 — Almacenamiento en un archivo JSON local

- Estado: aceptada
- Fecha: 2026-06-25

## Contexto
Necesito persistir las sesiones entre ejecuciones. Es una herramienta personal,
single-user, de pocos cientos de registros, y estoy en la Fase 0 (objetivo:
entender, cero dependencias externas).

## Decisión
Guardo las sesiones en un único archivo JSON, cuya ruta sale de la variable de
entorno BITACORA_FILE (default ~/.bitacora.json).

## Alternativas consideradas
- SQLite — robusto, pero overkill para este volumen y suma complejidad de esquema
  que no necesito aún. Lo reconsideraré si el archivo crece o quiero consultas.
- CSV — simple, pero modela peor datos anidados y es más frágil al editarlo a mano.

## Consecuencias
- (+) Cero dependencias; el archivo es legible y editable por un humano.
- (+) La env var permite tests y múltiples bitácoras sin tocar código (12-factor en miniatura).
- (−) No escala a concurrencia ni a millones de filas; lo acepto: no es el caso de uso.
```

### 3. El código (`bitacora.py`) — verificado, corre

```python
#!/usr/bin/env python3
"""bitacora — registra y resume tus sesiones de estudio desde la terminal."""
import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

EXIT_OK, EXIT_ERROR, EXIT_USO = 0, 1, 2


def ruta_datos() -> Path:
    return Path(os.environ.get("BITACORA_FILE", Path.home() / ".bitacora.json"))


def cargar(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []  # archivo nuevo: no es error
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"bitacora corrupta en {ruta}: {e}") from e


def guardar(ruta: Path, sesiones: list[dict]) -> None:
    ruta.write_text(json.dumps(sesiones, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_add(args: argparse.Namespace) -> int:
    tema = args.tema.strip()
    if not tema:
        print("error: el tema no puede estar vacio", file=sys.stderr)
        return EXIT_USO
    if args.min <= 0:
        print("error: --min debe ser un entero positivo", file=sys.stderr)
        return EXIT_USO
    ruta = ruta_datos()
    sesiones = cargar(ruta)
    sesiones.append({"fecha": date.today().isoformat(), "tema": tema, "min": args.min})
    guardar(ruta, sesiones)
    print(f"registrado: {tema} ({args.min} min)")
    return EXIT_OK


def cmd_resumen(args: argparse.Namespace) -> int:
    sesiones = cargar(ruta_datos())
    if not sesiones:
        print('sin sesiones aun: registra una con  bitacora add "tema" --min 40')
        return EXIT_OK
    por_semana: dict[str, int] = defaultdict(int)
    for s in sesiones:
        anio, semana, _ = date.fromisoformat(s["fecha"]).isocalendar()
        por_semana[f"{anio}-S{semana:02d}"] += s["min"]
    for clave in sorted(por_semana):
        print(f"{clave}: {por_semana[clave]} min")
    return EXIT_OK


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bitacora", description="bitacora de estudio")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("add", help="registra una sesion de estudio")
    p_add.add_argument("tema", help="que estudiaste")
    p_add.add_argument("--min", type=int, required=True, help="minutos (entero positivo)")
    p_add.set_defaults(func=cmd_add)

    p_res = sub.add_parser("resumen", help="suma minutos por semana ISO")
    p_res.set_defaults(func=cmd_resumen)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        return args.func(args)
    except ValueError as e:  # p. ej. bitácora corrupta
        print(f"error: {e}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
```

**Notas de diseño que el corrector debe reconocer como señales de comprensión:**
- **Decidir vs. actuar separados:** `cargar`/`guardar` (E/S) están aisladas de la
  lógica de cada comando. Es el mismo patrón del worked example de la lección y el
  que reaparece hasta en agentes de IA.
- **stdout = dato útil, stderr = diagnósticos.** El resumen y las confirmaciones van
  a `stdout`; todo error va a `stderr`. Esto hace el CLI componible con pipes.
- **Exit codes honestos y distintos:** `2` para uso incorrecto, `1` para error de
  ejecución (archivo corrupto), `0` para éxito —incluido el "resumen vacío", que
  **no** es un error.
- **Archivo inexistente ≠ error:** se trata como bitácora vacía; el archivo se crea
  al primer `add`. Confundir "no existe" con "error" es un fallo típico.

### 4. Demo que corre (pegada en el README)

```console
$ export BITACORA_FILE=./bitacora.json
$ bitacora resumen
sin sesiones aun: registra una con  bitacora add "tema" --min 40
$ bitacora add "algebra lineal" --min 40
registrado: algebra lineal (40 min)
$ bitacora add "python: argparse" --min 25
registrado: python: argparse (25 min)
$ bitacora resumen
2026-S26: 65 min
$ bitacora add "" --min 30
error: el tema no puede estar vacio
$ echo $?
2
```

### 5. Historial de Git (Conventional Commits, por pasos)

```text
chore: inicializa repo + hook commit-msg (core.hooksPath)
docs: agrega SPEC inicial de bitacora
docs: agrega ADR-0001 (almacenamiento json)
feat: registra sesiones con add (tema + minutos)
feat: resume minutos por semana ISO
fix: valida tema vacio y --min no positivo (exit 2)
fix: trata json corrupto como error de ejecucion (exit 1)
docs: agrega README con instalacion, uso y demo
```

El historial se lee como un resumen del proyecto: la spec y el ADR **antes** que la
primera `feat`, pasos pequeños que corren, y los bordes como `fix:` propios.

### 6. Write-up de trade-offs (cierre)

> Elegí JSON sobre SQLite por simplicidad y cero dependencias (lo dejé en el ADR);
> el costo es que no escala a concurrencia, que no me importa para una herramienta
> personal. Lo más difícil fue decidir que "archivo inexistente" y "resumen vacío"
> **no** son errores: mi instinto era lanzar excepción, pero la spec me obligó a
> pensarlo y terminó siendo exit 0. Dejé fuera editar/borrar sesiones a propósito:
> `add` + `resumen` es lo que uso de verdad esta semana.

---

## Mapeo al Definition of Done (lo que el corrector verifica)

| Punto del DoD (§B) | Evidencia en el ejemplar | Aplica en F0 |
|---|---|---|
| **1. Spec + ADRs** | `SPEC.md` commiteada antes de la 1ª `feat` + ADR-0001 | ✅ Obligatorio |
| **8. Demo que corre + README + write-up** | sesión de consola pegada + README usable + 5 líneas de trade-offs | ✅ Obligatorio |
| **9. Conventional Commits** | todo el historial valida contra el hook | ✅ Obligatorio |
| **Gate F0 — 100% sin IA** | puede explicar cada línea/commit y el porqué de cada exit code | ✅ Obligatorio |
| 2. Tests verdes en CI | — la "demo que corre" es la versión manual; los tests llegan en F1–F2 | 🌱 semilla |
| 3. Seguridad (OWASP) | — semilla: valida la entrada, no confía en datos a ciegas | 🌱 semilla |
| 4. Observabilidad | — semilla: stderr + exit codes honestos | 🌱 semilla |

## Rango de soluciones aceptables (para no penalizar lo correcto)

- **Cualquier problema** sirve si es útil para el alumno y resoluble con la Fase 0:
  organizador de archivos, divisor de gastos, gestor de notas, renombrador por
  lotes, conversor, etc. No exigir `bitacora`.
- **Un solo archivo** de código es perfecto; no pedir estructura de paquete ni
  empaquetado con `pyproject.toml` (es profundización opcional).
- `argparse` (stdlib) es la elección esperada, pero `click`/`typer` o incluso parseo
  de `sys.argv` a mano son aceptables **si el ADR lo justifica**.
- La persistencia puede ser JSON, CSV, SQLite, o ninguna (herramientas sin estado
  como un organizador de archivos) —lo que importa es la coherencia con la spec.
- **Otro lenguaje** (un CLI en Bash o Node) es válido si cumple el mismo DoD: spec,
  ADR, exit codes honestos, README con demo, Conventional Commits.
- Para el gate sin-IA: lo decisivo es que **defienda su diseño sin notas**, no la
  elegancia del código. Un CLI feo pero entendido y honesto supera a uno pulido que
  no puede explicar.
