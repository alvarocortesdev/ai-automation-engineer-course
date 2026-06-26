# `.ai/` — Framework de corrección por IA

> El alumno elige **cualquier** IA con acceso al repo (Claude Code, Cursor, ChatGPT con el repo cargado, etc.) y le pide que **corrija un ejercicio usando esta carpeta**. La IA no resuelve por el alumno: evalúa lo que el alumno ya intentó, detecta dónde se equivoca, y devuelve **feedback pedagógico** que lo empuja a aprender.

Esta carpeta es el contrato y el material que hace que esa corrección sea **consistente, honesta y sin spoilers**, sin importar qué modelo se use.

---

## Filosofía: Primero-Sin-IA (innegociable)

El curso existe porque la dependencia de la IA **para pensar** atrofia la autonomía de ingeniería. La corrección con IA no puede contradecir eso. Por tanto, el corrector:

- **EXPLICA y GUÍA. Nunca entrega la solución antes de que el alumno la haya intentado.** Si no hay intento del alumno, el corrector pide que primero lo intente (timebox 25–45 min) y se detiene.
- Da **feedback graduado**: primero pistas, luego preguntas socráticas, y **sólo al final** —si el alumno sigue trabado tras intentarlo de verdad— dirección concreta. Nunca el código completo de la solución de referencia.
- Distingue **corregir el trabajo** de **corregir a la persona**. El tono es el de un mentor exigente, no el de un juez.
- Detecta cuando el alumno usó IA **para pensar en vez de aprender** (explicación que no calza con el código, conceptos que "entiende sin notas" pero no puede defender) y lo nombra sin acusar.

> Regla rectora del repo: *"No se trata de no usar IA. Se trata de no necesitarla para pensar."*

El andamiaje **escala por novedad** (ver rúbricas):
- **Concepto nuevo:** worked example → ejercicio de completar (faded) → Primero-Sin-IA.
- **Repaso/consolidación:** Primero-Sin-IA de entrada.

---

## Cómo se usa (alumno)

1. El alumno trabaja el ejercicio en `ejercicios/<fase>/<slug>/`. Deja ahí su intento (código, tabla de traza, notas, `write-up`, lo que pida el enunciado). **Primero a mano, sin IA.**
2. Cuando quiere feedback, le pide a su IA:
   > "Corrige mi ejercicio `ejercicios/fase-0/trazado-a-mano-bucle/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."
3. La IA localiza el ejercicio, lee su contrato (`ejercicio.yml`), carga la rúbrica y la solución de referencia, evalúa, y devuelve feedback + veredicto **sin filtrar la solución**.
4. El alumno corrige, vuelve a intentar, y al día siguiente reescribe de memoria (spaced retrieval).

## Cómo se usa (autor del curso / quien escribe lecciones)

Cada sub-unidad que genere ejercicios debe producir, por ejercicio, **los cuatro artefactos del contrato** (abajo). Copia `ejercicios/fase-0/trazado-a-mano-bucle/` y `.ai/rubricas/_PLANTILLA.md` como referencias de calidad.

---

## Contrato de metadata por ejercicio (v1)

Cada ejercicio enlaza cuatro artefactos —**enunciado ↔ rúbrica ↔ solución ↔ tests**— para que el corrector navegue solo sin adivinar rutas. El enlace vive en un archivo **`ejercicio.yml`** dentro de la carpeta del ejercicio.

### Convención de rutas (por defecto, no hace falta declararla)

Dado `id: <fase>/<slug>` (clave única), el corrector resuelve por convención:

| Artefacto | Ruta (relativa a la raíz del repo) |
|---|---|
| **Enunciado** | `ejercicios/<fase>/<slug>/README.md` |
| **Solución del alumno** | `ejercicios/<fase>/<slug>/` (todo lo demás que dejó el alumno) |
| **Rúbrica** | `.ai/rubricas/<fase>/<slug>.md` |
| **Solución de referencia** | `.ai/soluciones/<fase>/<slug>.md` |
| **Tests** | `ejercicios/<fase>/<slug>/tests/` (si existe; muchos ejercicios `a-mano` no tienen) |

Sólo se declara una ruta en `paths:` cuando **difiere** de la convención (p. ej. un ejercicio sin solución de referencia: `paths: { solucion_referencia: null }`).

### Esquema de `ejercicio.yml`

```yaml
# .ai contract v1 — un ejercicio
id: fase-0/trazado-a-mano-bucle      # = <fase>/<slug>, clave única y estable
titulo: "Trazado a mano de un bucle anidado"
fase: fase-0
sub_unidad: "0.3"                    # id de la build-list / ROADMAP que lo origina
ruta_critica: true                   # true = ruta-crítica · false = opcional/profundización
modalidad: a-mano                    # a-mano | codigo | mixto
objetivos:                           # objetivos observables (verbos de Bloom); el corrector evalúa contra estos
  - "Predecir la salida de un bucle anidado línea a línea, sin ejecutar"
  - "Construir una tabla de traza (variable × iteración) que justifique la predicción"
hilos_transversales: []              # [testing, evals, seguridad, observabilidad, spec-driven, costo-latencia, ingles]
primero_sin_ia:
  novedad: nuevo                     # nuevo (worked example → faded → solo) | repaso (solo de entrada)
  timebox_min: 30                    # presupuesto sugerido de intento sin IA
definition_of_done: []               # IDs de los puntos del DoD único (§B) que aplican; [] en ejercicios atómicos sin capstone
paths: {}                            # overrides opcionales; sólo si una ruta difiere de la convención
```

### Reglas del contrato

- `id` es **estable**: no se renombra aunque cambie el título (las rúbricas/soluciones lo referencian).
- `objetivos` es la **fuente de verdad** de qué evaluar. Si el enunciado pide algo que no está en `objetivos`, falta un objetivo.
- `hilos_transversales` declara qué hilos (testing, evals, seguridad, observabilidad, spec-driven, costo/latencia, inglés) deben aparecer en una entrega **Excelente** aunque el enunciado no los pida —es ahí donde se mide si el alumno los interiorizó como hábito.
- `primero_sin_ia.novedad` le dice al corrector cuánto andamiaje esperar y cuán pronto puede dar dirección concreta.
- Para **capstones**, `definition_of_done` enumera los puntos del **Definition of Done único** (§B de `CURRICULUM-REVIEW.md`) que el corrector debe verificar como entregables de primera clase.

---

## Estructura de la carpeta

```
.ai/
├── README.md                      ← este archivo (qué es, cómo se usa, contrato)
├── INSTRUCCIONES-CORRECTOR.md     ← system/prompt MAESTRO del corrector IA
├── rubricas/
│   ├── _PLANTILLA.md              ← formato estándar de rúbrica
│   ├── fase-0/<slug>.md           ← una rúbrica por ejercicio
│   ├── fase-1..fase-8/            ← idem por fase
│   └── track-0/
└── soluciones/
    ├── README.md                  ← política de soluciones de referencia (spoiler)
    ├── fase-0/<slug>.md           ← solución de referencia, marcada spoiler
    └── fase-1..fase-8/, track-0/
```

## Ejemplo de referencia (calidad esperada)

El loop completo está instanciado para un ejercicio de Fase 0; cópialo como molde:

- Enunciado + contrato: `ejercicios/fase-0/trazado-a-mano-bucle/`
- Rúbrica: `.ai/rubricas/fase-0/trazado-a-mano-bucle.md`
- Solución de referencia: `.ai/soluciones/fase-0/trazado-a-mano-bucle.md`
