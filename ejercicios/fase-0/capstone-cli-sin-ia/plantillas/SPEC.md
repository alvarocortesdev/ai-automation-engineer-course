# SPEC — <nombre-de-tu-herramienta>

> **Mini-spec. Escríbela ANTES de codear.** Tres partes: entradas, salidas, casos
> borde. Cada fila de "casos borde" es, más tarde, una rama de validación de tu
> código (y, en la Fase 2, un test). No la escribas después: el valor está en
> pensar los bordes cuando todavía son baratos —en papel, no en producción.

## Propósito

<Una frase: qué problema **tuyo** resuelve esta herramienta. Si no la usarías esta
semana, elige otro problema.>

## Comandos

| Comando | Qué hace |
|---|---|
| `mi-cli <verbo> <args>` | … |
| `mi-cli <verbo> <args>` | … |

## Entradas

- `<argumento>`: `<tipo>` — `<formato / de dónde viene: argv, stdin, archivo, env var>`

## Salidas

- **stdout** (el dato útil, componible con pipes): `<qué imprime>`
- **stderr** (diagnósticos y errores): `<qué avisa>`
- **exit codes**:
  - `0` = éxito
  - `2` = uso incorrecto (argumento faltante / inválido)
  - `1` = error durante la ejecución
  - *(ajústalos a tu caso; lo importante es que cuenten una historia honesta de qué pasó)*

## Configuración (opcional)

- Variable de entorno `MI_CLI_<...>`: `<qué controla>`

## Casos borde (la mitad del trabajo)

| Caso | Qué debe pasar | exit |
|---|---|---|
| argumento faltante | mensaje de uso a `stderr` | 2 |
| entrada inválida (`<...>`) | error claro a `stderr` | 2 |
| caso "vacío" (`<...>`) | **no es error**: mensaje informativo a `stdout` | 0 |
| `<tu caso borde propio>` | … | … |
