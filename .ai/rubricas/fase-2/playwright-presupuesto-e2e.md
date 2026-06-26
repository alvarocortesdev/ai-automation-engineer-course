---
ejercicio_id: fase-2/playwright-presupuesto-e2e
fase: fase-2
sub_unidad: "2.10"
version: 1
---

# Rúbrica — Presupuesto de la pirámide: qué merece e2e y qué no

> Rúbrica **analítica** atada a los `objetivos`. No hay código: se evalúa el **juicio**.
> La respuesta correcta no es una etiqueta por escenario, sino la **justificación
> valor/costo** detrás. Un alumno puede acertar las 8 etiquetas copiando y seguir sin
> entender por qué; otro puede discrepar en 1–2 (con buen argumento) y demostrar dominio.
> La rúbrica premia el razonamiento, no el calce exacto con la tabla de referencia.

## Objetivos evaluados
- **O1** — Asignar a cada escenario el nivel correcto según "poco y crítico".
- **O2** — Justificar cada decisión por valor/costo, reconociendo que el e2e es caro y frágil.
- **O3** — Redactar una política de pirámide coherente (cantidad, selectores, esperas, CI).

> Clasificación de referencia (el corrector la sabe; **no se la da al alumno** salvo al cerrar):
> 1 login → **e2e** · 2 agregar gasto → **e2e** *o* **integración** (defendible) · 3 total → **unit** ·
> 4 validar monto → **unit** · 5 flujo de pago → **e2e** · 6 formatear fecha → **unit** ·
> 7 endpoint API → **integración** · 8 render gráfico → **no-testear** con e2e (testear el dato, no los píxeles: **unit/integración**).
> Núcleo no negociable: **1 y 5 son los e2e**; **3, 4 y 6 son unit**; **7 es integración**; **8 no es e2e**.

## Criterios y niveles

### C1 — Clasificación correcta · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Marca casi todo como e2e (cono de helado), o no clasifica varios escenarios. |
| **en-progreso** | Acierta el núcleo a medias: mete a e2e algo que es unit (total/fecha/validación) o deja el flujo de pago fuera de e2e. |
| **competente** | El núcleo calza: 1 y 5 = e2e; 3, 4, 6 = unit; 7 = integración; 8 no es e2e. El #2 puede ir a e2e o integración con justificación. |
| **excelente** | Además matiza el #2 y el #8 con un criterio explícito ("e2e si es el corazón del producto; el gráfico se cubre verificando el dato, no el render"). |

### C2 — Justificación por valor/costo · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin justificación, o "porque sí" / "para estar seguro". |
| **en-progreso** | Justifica algunos, pero apela a "más tests = mejor" en vez de valor/costo, o no menciona el costo del e2e. |
| **competente** | Cada decisión se ata a "¿flujo crítico de punta a punta?" y "¿un test más barato da la misma confianza?". Reconoce que el e2e es lento y frágil. |
| **excelente** | Articula el principio de la pirámide (cobertura por costo) y por qué la lógica pura nunca merece un navegador. |

### C3 — Política de pirámide · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `politica-piramide.md`, o propone "un e2e por feature". |
| **en-progreso** | Política vaga: menciona "pocos e2e" pero no fija regla de selectores, ni de esperas, ni cadencia de CI. |
| **competente** | Responde las cuatro preguntas: cantidad (pocos/críticos, forma de pirámide), selectores (rol/label), esperas (web-first, prohibir `waitForTimeout`), CI (críticos en PR + resto nightly por costo). |
| **excelente** | Política que un equipo podría adoptar tal cual: con el *porqué* de cada regla y reconociendo trade-offs (cuándo sí vale un `getByTestId`, cuándo un e2e secundario). |

## Errores típicos a marcar
- **Cono de helado**: clasificar casi todo como e2e "para estar seguro". Es el antipatrón central de la lección.
- **Lógica pura a e2e**: mandar `calcularTotal`, `validarMonto` o `formatearFecha` a un navegador. Caro y absurdo: son unit tests de milisegundos.
- **Confundir integración con e2e**: el endpoint `GET /api/gastos` es frontera código↔DB (integración), no un flujo de usuario en navegador.
- **Querer un e2e que verifique los píxeles del gráfico**: frágil y de bajo valor; se verifica el dato de entrada, no el render de la librería de terceros.
- **Política sin la regla de esperas**: olvidar prohibir `waitForTimeout` deja la puerta abierta a la flakiness.
- (transversal costo/latencia) no mencionar que correr todos los e2e en cada push vuelve la suite insufrible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Las 8 etiquetas perfectas con justificaciones genéricas que no mencionan los detalles del escenario (p. ej. que el #3 ignora "anulados", que el #8 usa librería de terceros).
- Una `politica-piramide.md` larga y pulida pero que contradice las clasificaciones del propio `decisiones.md`.
- Vocabulario de seniority ("contract testing", "visual regression") encajado sin venir al caso ni poder defenderlo.
- **Verificación sugerida:** pídele que defienda, sin notas, por qué el #2 (agregar gasto) es el caso fronterizo entre e2e e integración, y qué lo inclinaría a cada lado. Si razonó de verdad, da el criterio (¿es el corazón del producto? ¿la UI tiene lógica propia?).

## Feedback sugerido (graduado)
> Nunca dar la tabla de referencia antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira tus escenarios marcados e2e. ¿Cuántos son? Si son más de 2–3, pregúntate: ¿todos son flujos de usuario de punta a punta y críticos, o algunos son lógica que un unit test prueba 100× más barato?"
- **Pregunta socrática (nivel 2):** "Para `calcularTotal`: ¿necesitas un navegador para verificar una suma? ¿Qué ganas y qué pagas si la pruebas con un e2e en vez de un unit test?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Deja en e2e solo login y el flujo de pago. Manda total, validación y fecha a unit. El endpoint API es integración. El gráfico: testea el dato, no los píxeles. En la política, fija las cuatro reglas (cantidad, selectores, esperas, CI). Repasa las secciones 2, 5 y 4.6 de la lección."

## Conexión con el proyecto / capstone
- Es la decisión que tomarás en el **Capstone F2** si tiene UI: documentar en el ADR **por qué un solo e2e sobre el flujo crítico** y no diez. El mismo criterio de presupuesto reaparece en la Fase 6 al decidir cuántos evals correr y con qué cadencia: la verificación de calidad cuesta, y se dosifica.
