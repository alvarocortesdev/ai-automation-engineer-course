---
ejercicio_id: fase-0/git-modelo-mental
fase: fase-0
sub_unidad: "0.6"
version: 1
---

# Rúbrica — Predice las referencias (modelo mental de Git)

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **modelo mental** (a qué apunta cada referencia y por qué), no si copió la salida de `git log`. Un alumno puede acertar el grafo de pura intuición y no saber justificar el merge; otro puede equivocar una etiqueta pero razonar el rebase perfecto. La rúbrica los distingue.

## Objetivos evaluados
- **O1** — Predecir a qué apunta cada referencia (`main`, `feature`, `HEAD`) tras la secuencia.
- **O2** — Justificar fast-forward vs merge de 3 vías y dibujar el grafo resultante.
- **O3** — Explicar qué reescribe el rebase y enunciar la regla de oro.

> Resultado correcto (el corrector lo sabe; **no se lo adelanta al alumno** salvo al cerrar): `main`→C4, `feature`→C3, `HEAD`→`feature` *antes* del último `git switch main`; tras la secuencia completa `HEAD`→`main`→C4. El merge es de **3 vías** (ambas ramas avanzaron desde C2). El rebase produce **C3'** (hash nuevo) sobre C4.

## Criterios y niveles

### C1 — Grafo y etiquetado de referencias · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay grafo, o no distingue commits de ramas; trata la rama como una carpeta/copia. |
| **en-progreso** | Dibuja la cadena pero coloca mal una referencia (típico: cree que `main` "siguió" a C3, o que `HEAD` apunta a un commit y no a la rama). |
| **competente** | Grafo correcto con la bifurcación en C2; `main`→C4, `feature`→C3, `HEAD`→`main` al final, con flechas commit→padre. |
| **excelente** | Además expresa `HEAD` de forma simbólica (`ref: refs/heads/...`) y nota que el único post-it que se mueve en cada commit es el de la rama activa. |

### C2 — Justificación del merge (3 vías vs fast-forward) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No clasifica el merge, o dice fast-forward sin razón. |
| **en-progreso** | Acierta "3 vías" pero la justificación es circular ("porque sí") o no menciona la divergencia. |
| **competente** | Dice 3 vías **porque ambas ramas avanzaron desde el ancestro común (C2)**, así que no hay fast-forward; dibuja el commit de fusión con dos padres. |
| **excelente** | Contrasta explícitamente: el fast-forward solo aplicaría si `main` **no** hubiera avanzado (solo se movería el puntero, sin commit nuevo). |

### C3 — Comprensión del rebase + regla de oro · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No dibuja el grafo del rebase o cree que "pierde" C3. |
| **en-progreso** | Grafo lineal correcto pero no explica el cambio de hash, o la "regla" es vaga. |
| **competente** | Grafo lineal con C3' sobre C4; explica que C3' tiene **mismo cambio, padre y hash distintos**; enuncia la regla de oro. |
| **excelente** | Liga el cambio de hash a la naturaleza content-addressed de Git y da un criterio operativo (rebasear local antes de compartir; merge para lo ya público). |

### C4 — Metacognición (verificación honesta) · mapea: O1–O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No ejecutó para verificar, o no hay `verificacion.md`. |
| **en-progreso** | Verificó pero la nota es superficial ("me equivoqué") sin nombrar la idea de fondo. |
| **competente** | Compara predicción vs realidad y nombra con precisión cualquier idea equivocada (o por qué acertó). |
| **excelente** | Convierte el error en una regla reutilizable ("cuando dudo de dónde quedó una rama, miro qué post-it tenía `HEAD` al commitear"). |

## Errores típicos a marcar
- **`main` "sigue" a la rama nueva:** creer que tras `git switch -c feature` y commitear, `main` también avanza. Solo se mueve la rama activa.
- **`HEAD` apunta a un commit, no a una rama:** confundir el caso normal (HEAD→rama) con *detached HEAD*.
- **Llamar fast-forward a un merge de ramas divergidas:** olvidar que ambas avanzaron desde C2.
- **Creer que rebase borra/pierde C3:** no distingue "reescribir" (copia con otro hash) de "perder".
- **Ejecutar antes de predecir:** invalida O1 aunque el resto esté impecable (resultado sin proceso).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `grafo.md` con el resultado correcto pero sin razonamiento de qué post-it se mueve (resultado copiado de `git log --graph`).
- Vocabulario muy por encima del nivel F0 (ej. "DAG content-addressed") sin poder explicar la bifurcación concreta.
- Explicación del rebase impecable pero `verificacion.md` que no menciona ningún hash real ni el grafo ejecutado.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, dónde quedaría `HEAD` si tras la secuencia hace `git switch feature && git merge main`. Si trazó de verdad, lo resuelve; si dependió de IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el grafo final ni la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Revisa qué referencia se mueve en C3 y en C4. ¿`HEAD` apuntaba a la misma rama en ambos?"
- **Pregunta socrática (nivel 2):** "Para que un merge sea fast-forward, ¿qué tendría que ser cierto sobre `main` desde que `feature` divergió? ¿Se cumple aquí?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El punto a corregir es el modelo de la rama como **puntero móvil**: solo avanza la rama a la que apunta `HEAD` al commitear. Re-etiqueta el grafo bajo esa regla y vuelve a predecir el tipo de merge antes de ejecutar."

## Conexión con el proyecto / capstone
- Este músculo —saber dónde está cada rama sin ejecutar— sostiene el **Capstone F0 — CLI sin IA**: trabajarás en ramas y resolverás algún conflicto sin pánico. Es también justo lo que se evalúa cuando un entrevistador pregunta "¿qué hace este `rebase`?" (T0.3).
