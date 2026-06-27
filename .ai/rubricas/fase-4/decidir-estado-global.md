---
ejercicio_id: fase-4/decidir-estado-global
fase: fase-4
sub_unidad: "4.8"
version: 1
---

# Rúbrica — ¿Dónde vive cada pieza de estado?

> Rúbrica analítica para un ejercicio de **razonamiento/diseño** (sin tests). El corrector evalúa
> el `decision-estado.md` del alumno: la clasificación de las 8 piezas, la calidad de las
> justificaciones, y las dos respuestas trampa. No es la etiqueta lo que importa, sino **el porqué**.

## Objetivos evaluados
- **O1** — Clasificar cada pieza en local / server state / URL state / global de cliente, y justificar.
- **O2** — Explicar por qué meter server state en un store global es un antipatrón (dos fuentes de verdad).
- **O3** — Decidir desde la seguridad dónde NO persistir un token (XSS + `localStorage`).

> Clasificación esperada (el corrector la sabe; NO se la entrega): 1=local · 2=server · 3=URL · 4=global cliente · 5=local levantado (o store pequeño, con trade-off) · 6=global cliente + persist · 7=server · 8=secreto, fuera del store/persist (cookie httpOnly).

## Criterios y niveles

### C1 — Clasificación correcta de las 8 piezas (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan piezas, o mete server state (2, 7) en Zustand, o pone el id de conversación (3) en un store en vez de la URL. |
| **en-progreso** | La mayoría bien, pero confunde 1–2 piezas (típico: el modelo (4) como local, o el tema (6) sin notar el `persist`). |
| **competente** | Las 8 clasificadas correctamente: 2 y 7 como server state, 3 como URL state, 4 y 6 como global de cliente, 1 como local. |
| **excelente** | Además distingue que 6 necesita `persist` y 4 no, y trata la 5 como ambigua con criterio (no la fuerza a global). |

### C2 — Calidad de las justificaciones (comprensión demostrada) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Justificaciones ausentes o circulares ("es global porque es global"). |
| **en-progreso** | Justifica con la etiqueta pero sin el criterio (no apela a "vino de una API", "lo comparten muchos lejanos", "debe ser compartible por link"). |
| **competente** | Cada justificación apela al criterio de la escalera de decisión; se entiende por qué ahí y no en otro cubo. |
| **excelente** | Conecta con consecuencias concretas (refetch, staleness, re-render, deep-linking) y nombra la herramienta exacta por cubo. |

### C3 — Trampa del server state (T1) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No ve el problema, o cree que sí conviene ponerla en el store. |
| **en-progreso** | Intuye que "está raro" pero no nombra el problema concreto. |
| **competente** | Nombra las **dos fuentes de verdad** y/o que tendría que reimplementar a mano cache/refetch/invalidación que TanStack Query ya da. |
| **excelente** | Añade el síntoma observable (datos viejos, ¿cuál copia está fresca?) y por qué el store no sabe de staleness. |

### C4 — Seguridad del token (T2) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Diría que sí, o no menciona seguridad. |
| **en-progreso** | Dice "no" por instinto pero sin el porqué (no menciona XSS ni `localStorage` legible por scripts). |
| **competente** | Explica que `localStorage` es legible por cualquier script (riesgo XSS) y que un token jamás se persiste ahí; propone alternativa (cookie httpOnly). |
| **excelente** | Distingue secreto de estado de UI, menciona que el token no es "estado global" en el sentido de UI, y conecta con OWASP / manejo de sesión del backend. |

## Errores típicos a marcar
- Meter la lista de conversaciones (2) o los mensajes (7) en Zustand "para tenerlos a mano" (el antipatrón central de la lección).
- Poner el id de conversación (3) en un store en vez de la URL (rompe deep-linking, refresh y compartir por link).
- Clasificar el texto del input (1) como global (es local del componente del input).
- Decir que el token (8) "es global, va en el store con persist" (falla de seguridad grave).
- Forzar la barra lateral (5) a global sin reconocer que local-levantado suele bastar (sobre-engineering).
- Confundir Context con un gestor de estado (mencionarlo como equivalente a Zustand sin matiz de re-render).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tabla perfecta con vocabulario impecable pero justificaciones genéricas que no apelan a la app concreta (ChatLab) ni a consecuencias observables.
- Respuestas T1/T2 que suenan a copy-paste de un blog (mencionan herramientas que la lección no usó) sin poder defenderlas.
- **Verificación sugerida:** pídele que mueva una pieza de cubo (p. ej. "¿y si pongo los mensajes en Zustand? ¿qué se rompe primero?") y prediga la consecuencia. Si entiende, responde con el síntoma concreto; si copió, da una respuesta vaga.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia.
- **Pista (nivel 1):** "Para cada pieza, hazte la primera pregunta de la escalera: ¿este dato vino de una API? Si sí, ya tienes el cubo."
- **Pregunta socrática (nivel 2):** "Si guardas los mensajes (7) en Zustand y también los tiene TanStack Query, ¿cuál de las dos copias muestras cuando llega uno nuevo? ¿Cómo sabe el store que la del servidor cambió?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa las piezas 2 y 7: ambas vienen de un `GET`. Reclasifícalas como server state y explica en una frase qué le pides a TanStack Query que haga. Para la 8, cambia el eje de la respuesta de 'dónde es cómodo' a 'qué pasa si me roban lo que hay en localStorage'."

## Conexión con el proyecto / capstone
- Esta clasificación es el **plano de estado** del [Capstone F4](/fase-4-frontend/proyecto/): define qué va en `useUiStore`, qué en TanStack Query y qué en la URL. Hacerlo bien aquí evita pelear con datos viejos cuando montes el chat.
