---
ejercicio_id: track-0/readme-tecnico-en-ingles
fase: track-0
sub_unidad: "T0.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de
> medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio
> es de **producción en inglés sobre un proyecto propio**: no hay una única respuesta
> correcta; esta es una **referencia ejemplar** + el criterio para juzgar otras.

# Solución de referencia — Escribe un README técnico en inglés

## Respuesta canónica (ejemplo de entrega "excelente")

Proyecto de ejemplo: un script que cuenta frecuencias de palabras en un archivo de texto.

### `MI-README.md`

```markdown
# wordcount

A small CLI tool that counts word frequencies in a text file.

## Requirements

- Python 3.11+

## Usage

Run the script with the path to a text file:

    python wordcount.py path/to/file.txt

It prints each word and its frequency to stdout, sorted by count (highest first).

## Example

    $ python wordcount.py article.txt
    the    42
    data   18
    model  11
```

### `glosario.md` (ejemplo)

| # | Español | Inglés técnico idiomático |
|---|---------|---------------------------|
| 1 | ejecutar el script | run the script |
| 2 | lanza una excepción | raises an exception |
| 3 | por defecto | by default |
| 4 | devuelve / retorna | returns |
| 5 | imprime en pantalla | prints to stdout |
| 6 | recibe un JSON | accepts a JSON payload |
| 7 | ordenado por frecuencia | sorted by frequency |
| 8 | si el archivo no existe | if the file does not exist |

> **Clave de corrección:** el proyecto y el contenido exacto **dependen del alumno**.
> Cualquier proyecto vale. Lo que se mide es el inglés técnico y las convenciones, no el
> tema. No penalizar un proyecto trivial si el README es claro y correcto.

## Razonamiento paso a paso (lo que debe entender el alumno)

1. **La estructura va antes que la prosa.** Encabezados estándar (título+descripción,
   Requirements, Usage, Example) en orden lógico del lector: qué es → qué necesito → cómo
   se usa → muéstrame.
2. **El inglés técnico es idiomático, no traducido.** Los patrones de alto rendimiento:
   - 3ª persona del singular con "s": *it counts*, *the function returns*.
   - Propósito con "to + verbo": *to install*, *to run* (no "for install").
   - Verbos técnicos: *run / build / install / returns / raises / accepts*, no calcos
     ("execute" coloquial, "give back", "show in the screen").
   - Negación correcta: *if the file does not exist* (no "if the file not exists").
3. **Un ejemplo ejecutable vale más que tres párrafos.** Comando + salida real.
4. **El glosario captura la lucha real.** Los términos que al alumno le costaron son los
   que internaliza; copiar genéricos no enseña.

## Puntos resbalosos (donde el corrector debe mirar)
- **Conjugación de 3ª persona** (lo más común): "the function return", "it count".
- **"for + verbo"** para propósito en vez de "to + verbo".
- **Verbos no técnicos:** "give back" por "returns", "show in the screen" por
  "prints to stdout"/"displays on screen".
- **Orden de secciones:** Usage antes que Requirements.
- **Ejemplo ausente o decorativo** (sin comando + salida real).
- **Glosario copiado del starter** sin añadir los 4 términos propios (faltan filas 5–8).

## Rango de soluciones aceptables
- Cualquier proyecto (script, repo de estudio, plan de CLI) y cualquier lenguaje.
- Secciones adicionales (Installation, License, Contributing) son bienvenidas, no
  requeridas; lo mínimo son las 4 pedidas.
- El comando de uso puede ser de Python, Node, bash, lo que sea — siempre que sea **exacto**
  y vaya con imperativo directo.
- Inglés B1–B2 sólido es suficiente para "excelente" si los patrones técnicos están bien;
  NO se exige prosa avanzada. Penalizar lo retorcido, no lo simple.
- El glosario puede tener términos distintos a los del ejemplo; lo que importa es que sean
  **reales del proyecto del alumno** y la columna inglesa sea idiomática.
