---
ejercicio_id: fase-3/auditoria-owasp-config
fase: fase-3
sub_unidad: "3.13"
version: 1
---

# Rúbrica — Audita una configuración insegura (mapéala a OWASP)

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio **a-mano**: no hay tests; la
> entrega es `auditoria.md`. El corrector evalúa la **cobertura** (cuántas fallas reales
> detectó), la **clasificación** correcta a OWASP, y la **calidad del fix** — no la prosa.

## Objetivos evaluados
- **O1** — Detectar las fallas y clasificarlas en su categoría OWASP Top 10 (2021).
- **O2** — Proponer un fix concreto por hallazgo, distinguiendo autenticación de autorización.
- **O3** — Secrets management: detectar con gitleaks y saber que un secreto filtrado se rota, no solo se borra.

## Criterios y niveles

### C1 — Cobertura y detección · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 4 hallazgos, o se pierde los críticos (inyección, CORS, secreto, fuga de `password_hash`). |
| **en-progreso** | 4–5 hallazgos; detecta los obvios pero omite el IDOR sin auth, el handler que filtra el error o la ausencia de rate limit. |
| **competente** | **≥ 6** hallazgos distintos, incluidos CORS comodín+credenciales, f-string en SQL, secreto hardcodeado y fuga de `password_hash`. |
| **excelente** | Detecta los 8 marcados + nota que SSRF (A10) está **ausente** aquí pero sería el riesgo si se agregara un fetch saliente (pensamiento de superficie de ataque). |

### C2 — Clasificación OWASP y fix · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Clasifica mal la mayoría (p. ej. llama "injection" al CORS) o los fixes son vagos ("hacerlo más seguro"). |
| **en-progreso** | Clasificación correcta en lo grueso; algún fix genérico sin detalle accionable. |
| **competente** | Cada hallazgo con su categoría correcta (A01/A02/A03/A05…) y un fix concreto de 1–2 líneas. |
| **excelente** | Severidad bien razonada (prioriza por impacto×explotabilidad) y fixes que citan el mecanismo exacto (parametrizar, lista explícita de orígenes, env vars, response_model). |

### C3 — Autorización vs autenticación + secrets · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue auth de autorización; la sección de secrets falta o solo dice "sacar el secreto". |
| **en-progreso** | Señala el IDOR pero no lo nombra como problema de autorización; menciona gitleaks sin la rotación. |
| **competente** | Marca `GET /usuarios/{id}` como falla de **autorización** (falta auth/dueño); nombra `gitleaks git .` y dice que el secreto filtrado se **rota**. |
| **excelente** | Explica por qué borrar el secreto en un commit nuevo no basta (sigue en el historial) y propone `.env` + `.gitignore` + `.env.example` + scanner en CI. |

## Errores típicos a marcar
- **Clasificar el CORS comodín como "injection"** u otra categoría: es Security Misconfiguration (A05).
- **No notar que `*` + `allow_credentials=True`** es peor que cualquiera por separado (y que la spec lo prohíbe).
- **Confundir el IDOR/sin-auth con un problema de autenticación**: aquí ni siquiera hay auth en `GET /usuarios/{id}` — es control de acceso (A01).
- **Olvidar la fuga de `password_hash`** en la fila cruda: devolver el modelo de DB directo es fuga de datos.
- **Decir "borra el secreto del código" como fix completo**: hay que **rotarlo** porque ya está en el historial.
- **No mencionar el handler `Exception` que devuelve `str(exc)`**: filtra detalles internos (A05) — debería loguear el detalle y responder genérico.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Auditoría que lista 12 hallazgos genéricos copiados del Top 10 sin atarlos a **líneas concretas** del archivo (no leyó el código, recitó la lista).
- Categorías OWASP perfectas pero fixes que no calzan con FastAPI/SQLAlchemy (genéricos de otro stack).
- No puede decir cuál es el peor ni por qué (sin criterio de severidad propio).
- **Verificación sugerida:** pídele que señale la línea exacta de la inyección y reescriba el fix parametrizado; y que explique con sus palabras por qué `*`+credenciales es el combo tóxico.

## Feedback sugerido (graduado)
> Es un ejercicio de criterio; guía sin entregar la tabla completa.
- **Pista (nivel 1):** "Numeré 8 problemas con comentarios en el archivo. ¿Encontraste los 8? Empieza por la query del login: ¿cómo se construye?"
- **Pregunta socrática (nivel 2):** "¿`GET /usuarios/{id}` es un problema de saber quién llama, o de si quien llama puede ver ese usuario? ¿Y qué pasa con `password_hash` en la respuesta?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Asegúrate de cubrir: CORS (A05), f-string SQL (A03), secreto hardcodeado (A02/A05), debug+handler que filtra (A05), fuga de password_hash (A01/A02), IDOR sin auth (A01), sin rate limit (A05/A07). Cierra con `gitleaks git .` + rotar. Repasa 4.2–4.8."

## Conexión con el proyecto / capstone
- Esta auditoría es el checklist que aplicarás a tu propio capstone antes de entregarlo: el Definition of Done exige seguridad aplicada + secret-scanning en CI. Saber auditar código ajeno es saber revisar el tuyo.
