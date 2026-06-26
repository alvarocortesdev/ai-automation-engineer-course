# ejercicios/ — Tu workspace

Aquí **trabajas y dejas tus soluciones**. Es tu mesa de trabajo, al lado de VSCode, mientras estudias
la lección en el sitio. Cada ejercicio aplica la regla **Primero-Sin-IA**: lo intentas solo, a mano,
con timebox; consultas docs oficiales; y solo al final usas IA para revisar y explicar.

## Cómo funciona

```text
ejercicios/
├─ README.md                 ← este archivo
├─ plantilla-ejercicio/      ← la estructura base que replican todas las lecciones
└─ fase-N/<slug>/            ← un directorio por ejercicio
   ├─ README.md              ← enunciado: objetivo, criterios de "hecho", timebox, pista
   ├─ solucion.<ext>         ← starter que completas TÚ (no lo borres: los tests dependen de él)
   └─ test_solucion.<ext>    ← tests de ejemplo (extiéndelos con tus propios casos)
```

- Cada lección del sitio apunta a su scaffold aquí, en `ejercicios/fase-N/<slug>/`.
- El `slug` es descriptivo y en kebab-case (p. ej. `fase-1/cli-despensa/`).
- **Tu solución vive aquí.** Edita el starter, escribe tu código, corre los tests. Esto es tuyo;
  commitéalo si quieres llevar tu historial de avance.

## El ciclo de un ejercicio

1. Lee el **enunciado** (`README.md` del ejercicio) y arranca el cronómetro (25–45 min).
2. Resuélvelo **sin IA**, completando el starter. Corre los tests hasta que pasen.
3. ¿Atascado más allá del timebox? Abre la **pista** del enunciado y revisa la documentación oficial.
4. Cuando termines, **pide la corrección a una IA** (ver abajo).
5. Al día siguiente, **reescribe la solución de memoria**. Si no puedes, vuelve a la lección.

## Relación con `.ai/` (corrección por IA)

La carpeta `.ai/` en la raíz del repo contiene el framework de corrección:

- `.ai/INSTRUCCIONES-CORRECTOR.md` — el prompt maestro del corrector.
- `.ai/rubricas/fase-N/<slug>.md` — qué evaluar, criterios, niveles y errores típicos del ejercicio.
- `.ai/soluciones/fase-N/<slug>/` — solución de referencia (es para el corrector, **no la mires antes
  de intentarlo**: es un spoiler).

Para que una IA te corrija, dale tres cosas:

1. Tu entrega (el contenido de tu `ejercicios/fase-N/<slug>/`).
2. La rúbrica correspondiente de `.ai/rubricas/fase-N/<slug>.md`.
3. Las instrucciones del corrector (`.ai/INSTRUCCIONES-CORRECTOR.md`).

El corrector evalúa **corrección, calidad de ingeniería, seguridad y comprensión demostrada**, y te
devuelve *feedback pedagógico*: el misconception concreto, a qué sección de la lección volver y el
siguiente paso de práctica. No es solo una nota. Corrige el trabajo, no a la persona.

> En este repo existe la skill `.claude/skills/corregir-ejercicio/`, que automatiza ese flujo si usas
> un asistente compatible.

## Reglas de la casa

- **No borres** la firma de las funciones del starter: los tests dependen de ella.
- **Honestidad:** intenta de verdad antes de pedir ayuda. El valor del Primero-Sin-IA está en el
  intento, no en el resultado bonito.
- Usa **pnpm** para ejercicios JS/TS y **uv** para los de Python (o `pytest` directo).
