---
ejercicio_id: fase-2/disenar-dobles-y-contrato
fase: fase-2
sub_unidad: "2.8"
version: 1
---

# Rúbrica — Diseña la estrategia de dobles y decide dónde va un contrato

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio de **diseño**: no hay
> tests que corran, hay un documento (`plan-de-tests.md`) que el corrector evalúa por la **calidad del
> razonamiento**. Lo central es que el alumno elija el double por *naturaleza del colaborador* (no "mock
> para todo") y reconozca que la frontera HTTP entre servicios pide un **contrato**, no un mock.

## Objetivos evaluados
- **O1** — Elegir y justificar el test double correcto para cada uno de los cuatro colaboradores.
- **O2** — Distinguir verificación de estado de interacción y escribir casos en Given-When-Then.
- **O3** — Decidir qué frontera merece contract testing y explicar el modo de falla del mock, consumer vs provider.

## Criterios y niveles

### C1 — Elección de dobles (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan colaboradores, o asigna "mock" a todos sin distinguir naturaleza. |
| **en-progreso** | Asigna dobles razonables pero sin justificar, o confunde stub con mock (los trata como sinónimos). |
| **competente** | Los cuatro tienen double justificado: `Reloj`→stub, `Repo`→fake, `EnviadorDeEmail`→mock/spy, `PasarelaDePago`→stub/mock; explica por qué. |
| **excelente** | Además distingue cuándo la `PasarelaDePago` necesita un mock (verificar `assert_not_called` en el caso de rechazo) vs. un stub (camino feliz), y menciona el `dummy` como categoría aunque aquí no aplique. |

### C2 — Estado vs. interacción + Given-When-Then · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue estado de interacción, o los casos no están en GWT. |
| **en-progreso** | Casos en GWT pero no clasifica la verificación, o clasifica mal (llama "estado" a un `assert_called`). |
| **competente** | Dos casos en GWT legible (feliz + borde); clasifica correctamente estado (repo) vs. interacción (email/pasarela) con el porqué. |
| **excelente** | El caso de borde usa una **interacción negativa** (`assert_not_called` sobre la pasarela cuando el reembolso se rechaza) y lo razona; los GWT podrían leerse como criterios de aceptación de producto. |

### C3 — Contract testing (la decisión clave) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica ninguna frontera para contrato, o propone contract testing para el repo/reloj (internos). |
| **en-progreso** | Señala la `PasarelaDePago` pero no explica el modo de falla del mock, o confunde contract test con test de integración. |
| **competente** | Identifica la `PasarelaDePago`; explica que un mock codifica *su suposición* del otro lado y que si el provider cambia el JSON el mock sigue verde; nombra consumer (su servicio) y provider (el equipo de la pasarela). |
| **excelente** | Además explica que el pact se **genera en el CI del consumer** y se **verifica en el CI del provider**, y por qué eso escala mejor que integración end-to-end; menciona que `match` afirma la *forma*, no el valor. |

## Errores típicos a marcar
- **"Mock para todo":** el error central. No distinguir que el reloj solo necesita un valor (stub) y que el repo se prueba mejor con un fake + estado.
- **Contract testing para colaboradores internos:** proponer Pact para el `Repo` o el `Reloj`. El contrato es para fronteras entre **servicios desplegados por separado** (otro equipo), no para dependencias internas del mismo proceso.
- **Confundir contract test con test de integración:** decir que el contract test "levanta los dos servicios y los prueba juntos". Es lo contrario: cada lado se verifica por separado contra el contrato.
- **Caso de borde mal verificado:** afirmar el resultado (excepción) pero olvidar que la pasarela **no debe llamarse** cuando el reembolso se rechaza por regla de negocio (`assert_not_called`).
- (transversales, seguridad) no notar que validar el monto *antes* de llamar a la pasarela (no reembolsar más de lo cobrado) es una verificación de negocio que merece su propio test de borde.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Vocabulario perfecto ("consumer-driven contract", "provider verification") pero no puede explicar con sus palabras *por qué* un mock "miente" (no conecta el concepto con el caso concreto de la pasarela).
- Asigna los cinco doubles con definiciones de libro pero no los mapea a *estos* cuatro colaboradores, o fuerza un `dummy` donde no hay ninguno.
- Clasifica estado/interacción correctamente en la teoría pero al revés en sus propios casos.
- **Verificación sugerida:** pedir que explique, en una frase, qué pasaría en producción si el equipo de la pasarela renombrara `id_transaccion` a `transaction_id` y solo hubiera un mock. Quien entendió dice "mis tests siguen verdes y mi cliente revienta en runtime"; quien dependió de la IA da una definición genérica.

## Feedback sugerido (graduado)
> Nunca dar la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada colaborador, pregúntate solo una cosa: ¿necesito que *devuelva* algo, que *registre* que lo llamé, o que *funcione de verdad pero liviano*? Esa pregunta ya te da el double."
- **Pregunta socrática (nivel 2):** "El email no deja rastro consultable y el repo sí. ¿Cómo afirmas 'se envió el comprobante' si no puedes leer ningún estado? ¿Y cómo afirmas 'quedó guardado' sin mockear el repo? Una de las dos respuestas es 'verifico interacción' y la otra 'verifico estado' — ¿cuál es cuál?"
- **Dirección concreta (nivel 3, solo tras intento real):** "La frontera con la `PasarelaDePago` es entre tu servicio y otro equipo: un mock ahí solo prueba *tu suposición* de su respuesta. El contrato (Pact) vuelve esa suposición un artefacto que el otro equipo verifica en su CI. Tú eres el consumer; ellos el provider. Eso es lo que un test de integración end-to-end no te da sin levantar todo el stack."

## Conexión con el proyecto / capstone
- Esta estrategia de dobles es la que aplicarás al testear el backend del **Capstone F2** sin acoplarte a la implementación. Y la decisión de "esto cruza a otro servicio → contrato" es la **semilla directa de la Fase 7**: cuando un agente de automatización integre con sistemas externos, el pact es lo que evita que un cambio ajeno te rompa en producción (modo de falla #1 de la integración).
