---
ejercicio_id: fase-3/disenar-puertos-cobranza
fase: fase-3
sub_unidad: "3.9"
version: 1
---

# Rúbrica — Diseña los puertos de una feature (y decide dónde NO ponerlos)

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio **a-mano**: no hay test que pase. Evalúa
> `diseno.md` + `diagrama.md`. La clave no es "puso muchos puertos" sino **criterio**: puertos donde
> pagan, y un "PUERTO NO" bien defendido donde sería sobre-ingeniería. Mide el juicio, no la cantidad.

## Objetivos evaluados
- **O1** — Clasificar piezas en dominio puro vs adaptadores y proponer los puertos justos con sus métodos.
- **O2** — Decidir, por escenario, PUERTO SÍ / NO con un trade-off defendible (testabilidad / cambio real vs sobre-ingeniería).
- **O3** — Dibujar la dirección de las dependencias correctamente (todo hacia el dominio).

## Criterios y niveles

### C1 — Clasificación dominio vs adaptador · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Mete la regla de negocio entre los adaptadores, o llama "dominio" a la persistencia/email. |
| **en-progreso** | Clasifica bien la mayoría pero confunde una pieza (p. ej. trata el formateo como dominio "de negocio"). |
| **competente** | La regla del paso 1 = dominio puro; DB/email/webhook = adaptadores de salida; HTTP = adaptador de entrada. |
| **excelente** | Lo anterior + nombra la entrada (HTTP) como adaptador *driving* y los externos como *driven*, con la terminología correcta. |

### C2 — Puertos propuestos y sus métodos · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin puertos, o puertos sin métodos/firmas. |
| **en-progreso** | Propone puertos pero con métodos vagos o que filtran detalles de infra (p. ej. `enviar_smtp(...)` en vez de `enviar_recibo(...)`). |
| **competente** | `RepositorioPagos`, `EnviadorDeEmail`, `NotificadorWebhook` con métodos expresados en lenguaje de dominio. |
| **excelente** | Los nombres de método describen la **intención** (qué necesita el dominio), no la tecnología; firmas limpias y mínimas. |

### C3 — Criterio "light": las tres micro-decisiones · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "PUERTO SÍ" a las tres (incluido el formateo) sin justificar: no detectó la sobre-ingeniería. |
| **en-progreso** | Acierta D1/D3 (email/webhook = SÍ) pero también pone puerto al formateo, o no defiende las decisiones. |
| **competente** | D1=SÍ, D3=SÍ, D2=NO, cada una con trade-off defendible (testabilidad / cambio real vs función pura ya testeable). |
| **excelente** | Razona el criterio general ("introduce el puerto cuando el dolor ya es visible, no por si acaso") y menciona el riesgo de pattern-itis. |

### C4 — Diagrama: dirección de dependencias · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Flechas del dominio hacia adaptadores concretos (DB, email): dependencia invertida mal. |
| **en-progreso** | Estructura razonable pero alguna flecha sale del dominio hacia la infra, o faltan los puertos. |
| **competente** | HTTP→dominio→puertos; adaptadores de salida implementan los puertos; ninguna flecha sale del dominio hacia un concreto. |
| **excelente** | Distingue visualmente entrada/salida y muestra los puertos como el límite; coherente con la clasificación de C1. |

### C5 — Testabilidad y seguridad · mapea: O2 (transversal testing + seguridad)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica cómo testear sin infra, ni menciona el riesgo del webhook. |
| **en-progreso** | Menciona dobles vagamente, o la seguridad sin nombrar el vector. |
| **competente** | Explica inyectar dobles por los puertos (sin email/webhook/DB reales) **y** nombra el riesgo SSRF del POST saliente. |
| **excelente** | Conecta los dobles con la taxonomía (fake/spy/mock) y propone una mitigación concreta (allowlist de URLs, validar destino). |

## Errores típicos a marcar
- **Puerto al formateo de monto:** función pura ya testeable; un puerto ahí es ceremonia. Es la trampa del ejercicio.
- **Regla de negocio clasificada como adaptador** o, al revés, el email tratado como "dominio".
- **Métodos del puerto que filtran tecnología** (`enviar_via_smtp`, `insert_sql`) en vez de intención (`enviar_recibo`, `guardar`).
- **Flecha del dominio hacia un adaptador concreto** en el diagrama (dependencia mal dirigida).
- **Decisiones sin defensa** ("PUERTO SÍ porque es buena práctica"): el ejercicio mide el trade-off, no el dogma.
- **Olvidar SSRF** en el POST saliente a una URL configurable.
- (transversal) "puertos a todo" = pattern-itis; tan grave como el acoplamiento.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño con 5+ puertos, "capa de aplicación", DTOs y mappers para todo: sofisticación impropia del enunciado (un CRUD con 3 efectos externos), señal de plantilla pegada.
- Justificaciones que repiten "clean architecture / SOLID / desacoplar" sin aterrizar en testabilidad o cambio concreto de ESTA feature.
- Pone "PUERTO SÍ" al formateo y no sabe por qué una función pura no lo necesita.
- **Verificación sugerida:** pídele que defienda, sin notas, por qué el formateo de monto NO merece un puerto pero el envío de email SÍ; y que diga qué piezas del diseño cambiarían si mañana migrara de SendGrid a Resend (solo el adaptador de email, no el dominio).

## Feedback sugerido (graduado)
> Es un ejercicio de criterio; guía con preguntas, no des el diseño.
- **Pista (nivel 1):** "Para cada pieza pregúntate: ¿toca el mundo exterior (DB, red, archivos) o es lógica pura? Lo que no lo toca rara vez necesita puerto."
- **Pregunta socrática (nivel 2):** "¿Qué ganas poniéndole un puerto al formateo de monto? ¿Lo vas a mockear en un test? ¿Va a cambiar de proveedor? Si la respuesta a ambas es no, ¿qué te da el puerto que no tengas ya?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El dominio = la regla del paso 1. Puertos = `RepositorioPagos`, `EnviadorDeEmail`, `NotificadorWebhook` (lentos/con efectos/intercambiables). El formateo = función pura, sin puerto. En el diagrama, el `ServicioPagos` apunta a los **puertos**, y los adaptadores concretos los **implementan**. Repasa 4.2 y 4.9."

## Conexión con el proyecto / capstone
- Es el criterio que aplicarás en cada feature del capstone que toque sistemas externos: dónde trazar un puerto (testabilidad/cambio) y dónde no (sobre-ingeniería). La decisión va documentada en un ADR, y el riesgo SSRF del webhook reaparece en `3.13` (OWASP) y en los agentes que hacen fetch de la Fase 6/7.
