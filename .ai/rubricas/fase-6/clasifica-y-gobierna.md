---
ejercicio_id: fase-6/clasifica-y-gobierna
fase: fase-6
sub_unidad: "6.15"
version: 1
---

# Rúbrica — Clasifica y gobierna: 5 sistemas de IA

> Rúbrica **analítica** atada a los `objetivos` del contrato. Los **tiers tienen veredicto
> correcto** (no es opinión: rankear CVs es alto riesgo, el social scoring está prohibido);
> los **artefactos y matices** se evalúan por la calidad de la justificación. El corrector
> evalúa que el alumno **derive** del orden de preguntas y resuelva el alcance, no que copie
> una tabla.

## Objetivos evaluados

- **O1** — Clasificar cada sistema en el tier correcto, derivándolo del orden de preguntas.
- **O2** — Resolver el alcance extraterritorial (¿la salida llega a la UE?).
- **O3** — Derivar obligaciones (Art. 50, logging, supervisión humana, sesgo) y artefactos de gobernanza.

## Criterios y niveles

### C1 — Tier correcto, derivado del criterio · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Pone el mismo tier a varios, o clasifica el social scoring (Caso 5) como "alto riesgo" en vez de prohibido, o el screening de CVs (Caso 1) como "limitado/mínimo". |
| **en-progreso** | Acierta 2–3 tiers pero no los deriva del orden de preguntas (los justifica "porque sí"), o confunde "decide sobre personas" con "interactúa". |
| **competente** | Caso 1 → alto; Caso 2 → limitado; Caso 3 → limitado; Caso 4 → mínimo; Caso 5 → inaceptable. Cada uno justificado por la pregunta que lo decide. |
| **excelente** | Nombra explícitamente la pregunta del orden que zanja cada caso ("decide sobre empleo → Annex III → alto"; "interactúa, no decide → Art. 50") y distingue el Caso 3 (genera contenido → Art. 50) del Caso 1 (decide → alto). |

### C2 — Alcance extraterritorial bien resuelto · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Afirma "estoy en Chile, no me aplica" en algún caso; o no menciona el alcance. |
| **en-progreso** | Resuelve el alcance solo en algunos casos, o lo confunde con "dónde está el servidor". |
| **competente** | En cada caso decide el alcance por **a dónde llega la salida**; reconoce que el Caso 4 (spam interno, sin usuarios UE) NO le aplica el Act. |
| **excelente** | Articula el principio (efecto Bruselas: "no es dónde corre el servidor, es a dónde llega la salida") y nota que aunque el Act no aplique (Caso 4), los principios de Responsible AI siguen siendo buena ingeniería. |

### C3 — Obligaciones y artefactos derivados · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra obligaciones concretas, o las inventa; no propone artefactos. |
| **en-progreso** | Nombra "model card / audit log" genéricamente sin atarlos al caso. |
| **competente** | Para el Caso 1 (alto): supervisión humana + audit log + medir sesgo + model/data card. Para 2 y 3 (limitado): aviso Art. 50 (badge de IA / etiqueta de contenido sintético). Para 4 (mínimo): nada obligatorio. |
| **excelente** | Distingue la transparencia del Caso 2 (avisar que es IA) de la del Caso 3 (marcar/etiquetar contenido sintético); para el Caso 1 enfatiza "sugiere, no decide" (humano en el loop) como mitigación de fondo, y conecta el sesgo con métricas desagregadas (6.0/6.9). |

## Errores típicos a marcar

- Clasificar el **social scoring** (Caso 5) como alto riesgo en vez de **prohibido**.
- Clasificar el **screening de CVs** (Caso 1) como limitado/mínimo (es alto riesgo, Annex III).
- Tratar **interactuar/generar** (Casos 2, 3) como "alto riesgo" — no deciden sobre personas.
- "Estoy en Chile → no aplica": ignorar el alcance extraterritorial cuando la salida llega a la UE.
- No identificar que el **Caso 4** (spam interno) es a la vez mínimo **y** fuera del alcance.
- Confundir el aviso "es una IA" (Art. 50.1, Caso 2) con el marcado de contenido sintético (Art. 50.2, Caso 3).
- (transversal) artefactos genéricos sin atarlos al caso; ningún trade-off ni consecuencia concreta de clasificar mal.

## Señales de dependencia-IA

- Cinco casos con prosa pulida e idéntica estructura pero **sin** comprometerse a un tier
  ("podría ser alto o limitado según el contexto") cuando el caso tiene veredicto claro.
- Cita artículos o números inventados (un "Annex VII", una multa que no existe) que no
  salieron en la lección.
- **Verificación sugerida:** pídele que explique, sin notas, por qué el screening de CVs es
  alto riesgo y el chatbot no. Si lo razonó, distingue "decide sobre empleo" de "solo
  interactúa"; si lo copió, repite "es alto riesgo" sin el mecanismo.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir la clasificación por el alumno.**

- **Pista (nivel 1):** "Para cada caso, recorre el orden: ¿prohibido? ¿decide algo serio
  sobre personas? ¿interactúa o genera contenido? ¿nada? La primera que dé 'sí' fija el tier."
- **Pregunta socrática (nivel 2):** "En el Caso 1, ¿qué pasa en la vida de una persona si tu
  sistema la rankea última? ¿Y en el Caso 2, qué decide el chatbot sobre alguien? Esa
  diferencia es la que separa alto de limitado."
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu Caso 5 es el prohibido
  (asignar puntaje para dar/negar servicios = social scoring). Tu Caso 4 es el único fuera del
  alcance (spam interno, sin salida a la UE). Y para el alcance del resto, fíjate en si hay
  usuarios o clientes en la UE recibiendo la salida — el servidor en Santiago no cambia nada."

## Conexión con el proyecto / capstone

- Esta clasificación es **literalmente** la sección de gobernanza del
  [Capstone F6 (Plataforma RAG)](/fase-6-ai-engineering/proyecto/): en qué tier cae tu RAG
  (típicamente limitado → Art. 50), si te alcanza el alcance, y qué avisas/logueas. Conecta con
  el segundo ejercicio (model card + audit log) y con
  [6.9 · evals](/fase-6-ai-engineering/6-9-eval-driven-development/) para el sesgo medido.
