---
ejercicio_id: fase-6/clasifica-y-gobierna
fase: fase-6
sub_unidad: "6.15"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Los **tiers** tienen
> veredicto correcto (úsalos como vara firme); los **artefactos y matices** admiten varias
> respuestas defendibles. Juzga la **calidad de la justificación** y que el alumno derive del
> orden de preguntas, no la coincidencia literal.

# Solución de referencia — Clasifica y gobierna: 5 sistemas de IA

## Caso 1 — Screening de CVs

- **Tier de riesgo:** **alto**. Pregunta que lo decide: "¿decide algo serio sobre personas?"
  → sí, **empleo**. El Annex III lista los sistemas de contratación/selección como alto riesgo.
- **¿Le aplica el EU AI Act?** **Sí.** Clientes en España usan la salida (el ranking) → la
  salida llega a la UE. El servidor en Santiago es irrelevante.
- **Obligaciones principales:** gestión de riesgo, data governance, documentación técnica,
  **logging automático** (Art. 12), **supervisión humana**, robustez, evaluación de
  conformidad. En la práctica: el sistema **sugiere**, RRHH **decide** (nunca rechazo
  automático).
- **Artefactos:** **audit log** de cada ranking (qué CV, score, versión de modelo, quién lo
  usó), **model card** (uso previsto + out-of-scope "no decide, sugiere" + evaluación de
  sesgo), **data card** del dataset (sesgos conocidos), y medición de desempeño
  **desagregada por grupo** (fairness).
- **Riesgo si lo clasificaras mal:** tratarlo como mínimo → discriminación no detectada +
  multa (hasta 15M EUR o 3%) + un sistema indefendible frente a un candidato rechazado.

## Caso 2 — Chatbot de soporte

- **Tier de riesgo:** **limitado**. No decide nada serio sobre personas: **interactúa** y, si
  no sabe, deriva a un humano. Pregunta que lo decide: "¿interactúa con personas?" → sí.
- **¿Le aplica el EU AI Act?** **Sí** (usuarios en la UE reciben la salida).
- **Obligaciones principales:** **transparencia (Art. 50.1)** — informar que se está hablando
  con una IA (un badge "Asistente de IA"), salvo que sea obvio.
- **Artefactos:** la etiqueta de transparencia en la UI; opcionalmente una model card ligera y
  audit log básico (buena práctica, no obligatorio en este tier).
- **Riesgo si lo clasificaras mal:** tratarlo como alto riesgo → sobre-ingeniería costosa para
  algo que solo necesita un aviso. Tratarlo como "sin nada" → incumplir el Art. 50 (multa
  posible).

## Caso 3 — Generador de avatares "deepfake" para marketing

- **Tier de riesgo:** **limitado**. Genera **contenido sintético** (video de un presentador
  que no grabó eso). No decide sobre personas. Pregunta que lo decide: "¿genera contenido?"
  → sí.
- **¿Le aplica el EU AI Act?** **Sí** (campañas en mercados que incluyen la UE).
- **Obligaciones principales:** **transparencia (Art. 50.2 / deepfakes)** — el proveedor del
  generador marca la salida como artificial en **formato detectable por máquina** (marca de
  agua/metadatos) y el deployer **etiqueta** visiblemente que el video fue generado/manipulado.
- **Artefactos:** marca de agua + etiqueta visible; model card del generador con out-of-scope
  (p. ej. "no usar para suplantar a personas reales sin consentimiento").
- **Riesgo si lo clasificaras mal:** no etiquetar → engaño al público + incumplimiento Art. 50.
  Además, si el deepfake fuera **no consentido** de una persona real, podría caer en la nueva
  **prohibición** (Art. 5, imágenes íntimas no consentidas / contenido ilícito) → inaceptable.

## Caso 4 — Filtro de spam

- **Tier de riesgo:** **mínimo**. No decide algo serio sobre personas externas, no interactúa
  con el público, no genera contenido. Todas las preguntas dan "no".
- **¿Le aplica el EU AI Act?** **No** (uso interno, la salida no llega a usuarios en la UE).
  Aun así, los principios de Responsible AI (no perder correos legítimos, etc.) siguen siendo
  buena ingeniería.
- **Obligaciones principales:** **ninguna obligatoria.**
- **Artefactos:** voluntarios; quizá una nota de evaluación (precision/recall del clasificador).
- **Riesgo si lo clasificaras mal:** sobre-ingenierizarlo (model card formal, conformidad)
  = quemar tiempo por nada.

## Caso 5 — "Puntaje de confianza ciudadana"

- **Tier de riesgo:** **inaceptable — prohibido.** Asignar a ciudadanos un puntaje de
  confiabilidad agregando comportamiento para **darles o negarles servicios** es **social
  scoring**: la primera pregunta del orden ("¿es un uso prohibido?") da "sí" y te detienes.
- **¿Le aplica el EU AI Act?** Si toca la UE, sí — y la respuesta es que **no se construye**.
- **Obligaciones principales:** N/A — está **prohibido** (tope de multa: 35M EUR o 7%).
- **Artefactos:** N/A. La decisión de ingeniería correcta es **no hacerlo** y decir por qué.
- **Riesgo si lo clasificaras mal:** intentar "gobernarlo" con model cards y audit logs como
  si fuera alto riesgo → estás documentando algo que la ley **prohíbe**. El error es no
  reconocer la línea roja.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Caso 5 como "alto riesgo"** en vez de prohibido: el error conceptual más grave; el social
   scoring estatal es línea roja, no "alto riesgo con muchas obligaciones".
2. **Caso 1 como limitado/mínimo:** subestimar que decidir sobre empleo es Annex III.
3. **Casos 2 y 3 como alto riesgo:** confundir "interactúa/genera" con "decide sobre personas".
4. **Caso 4 dentro del alcance:** no notar que es interno y sin salida a la UE.
5. **Distinción Art. 50.1 vs 50.2:** avisar "es una IA" (Caso 2) no es lo mismo que marcar/
   etiquetar contenido sintético (Caso 3).
6. "Estoy en Chile → no aplica" en cualquier caso donde la salida sí llega a la UE.

## Rango de soluciones aceptables

- En el Caso 3, es defendible mencionar la nueva prohibición (deepfakes no consentidos) como
  el límite donde "limitado" se vuelve "inaceptable"; no es obligatorio, es señal de dominio.
- En el Caso 2, añadir audit log/model card como buena práctica es válido aunque no sea
  obligatorio en riesgo limitado — siempre que el alumno aclare que es voluntario.
- En el Caso 1, cualquier conjunto razonable de obligaciones de alto riesgo cuenta; lo
  innegociable es **supervisión humana + sesgo medido + logging**.
- Para el alcance, aceptar "no aplica" solo donde la salida realmente no toca la UE (Caso 4).
  En 1, 2, 3 la respuesta correcta es "sí aplica".
- Mencionar que los principios de Responsible AI aplican aunque el Act no (Caso 4) es señal de
  madurez, no requisito.
