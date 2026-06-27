---
ejercicio_id: fase-5/auditar-supply-chain
fase: fase-5
sub_unidad: "5.4"
version: 1
---

# Rúbrica — Auditoría de supply chain de un workflow real

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: **el `hallazgos.md` es el corazón** y se corrige por la calidad, completitud y priorización de la auditoría —no por una redacción única. Una clasificación OWASP CICD-SEC distinta pero defendible es válida.

## Objetivos evaluados

- O1: Identificar al menos 6 fallas de cadena de suministro distintas en el workflow.
- O2: Clasificar cada falla por gate/concepto y categoría OWASP CICD-SEC, con severidad justificada.
- O3: Priorizar los arreglos por impacto real, reconociendo el PPE como el más grave.

## Las fallas que el workflow contiene (checklist del corrector)

> El alumno debería cubrir la mayoría. Hay 7; el DoD pide ≥6.

1. `pull_request_target` + checkout del `head.ref` del PR + acceso a secrets → **Poisoned Pipeline Execution (PPE)**, CICD-SEC-04. **Severidad: crítica/alta** (RCE con tus secrets desde un fork ajeno).
2. `permissions: write-all` → **privilegio excesivo** del `GITHUB_TOKEN` (CICD-SEC-05/Insufficient PBAC). Media-alta.
3. `actions/checkout@main` → action **sin pinear** a SHA, ref mutable (CICD-SEC-03 *Dependency Chain Abuse*). Media-alta.
4. `randomdev/super-deploy-action@v1` → action de **tercero no confiable** y además sin pinear (CICD-SEC-03 / uso no gobernado de 3ros). Alta.
5. `${{ github.event.pull_request.title }}` dentro de un `run:` → **script/expression injection** (el título lo controla el atacante; CICD-SEC-04). Alta.
6. `curl -sSL ... | sudo bash` → **ejecución de código remoto sin verificar** (versión no fijada, puede cambiar; CICD-SEC-04). Alta.
7. `PROD_API_KEY: "prod-key-..."` → **secreto en texto plano** en el YAML (filtración; debe ser `${{ secrets.X }}` y rotarse). Alta.

## Criterios y niveles

### C1 — Cobertura (¿encontró las fallas?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 4 fallas, o varias son la misma con otro nombre. Se le pasó el PPE. |
| **en-progreso** | 4–5 fallas reales, pero mezcla dos en una o se le escapa una alta (PPE, injection o el 3ro no confiable). |
| **competente** | ≥6 fallas distintas, incluido el PPE y el secreto en claro. |
| **excelente** | Las 7, incluida la **expression injection** del título del PR (la más sutil), con cada una bien delimitada. |

### C2 — Clasificación y severidad · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin clasificar, o todo "alto" sin justificar; no usa los conceptos de la lección. |
| **en-progreso** | Clasifica por gate (secret/pin/permisos) pero no mapea a OWASP CICD-SEC, o la severidad es arbitraria. |
| **competente** | Cada falla con su gate/concepto + una categoría CICD-SEC razonable + severidad justificada en una frase. |
| **excelente** | Distingue con precisión secreto-en-claro (filtración) de action-sin-pinear (supply chain) de PPE (ejecución); mapeo CICD-SEC correcto y defendible. |

### C3 — Priorización (criterio de ingeniero) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No prioriza, o prioriza por orden de aparición en el archivo. |
| **en-progreso** | Prioriza pero por criterio débil ("el secreto porque es obvio") sin pesar impacto/explotabilidad. |
| **competente** | Pone el **PPE** (o el combo secrets+código no confiable) primero, porque combina mayor impacto y explotabilidad por un externo. |
| **excelente** | Razona impacto × probabilidad, agrupa arreglos rápidos de alto retorno (pin + permisos + rotar secreto) y justifica el orden. |

## Errores típicos a marcar

- Pasar por alto el **PPE**: es el más grave y el menos obvio; si no está, el feedback debe apuntar ahí sin resolverlo.
- Tratar `actions/checkout@main` y el secreto en claro como "lo mismo" (son superficies distintas: build chain vs. credenciales).
- No notar la **expression injection** del `${{ ... }}` en `run:` (input controlado por atacante → comando).
- Decir "quitar `curl | bash`" sin explicar el riesgo (código remoto no versionado ni verificado).
- Priorizar por orden de aparición en vez de por impacto.
- Olvidar que el secreto filtrado, además de moverse a `secrets`, hay que **rotarlo**.

## Señales de dependencia-IA

- Lista exhaustiva y perfectamente formateada pero **sin priorización propia** o con priorización genérica (señal de copy-paste).
- Usa nombres exactos de CICD-SEC para las 7 pero no puede explicar **por qué** el PPE es peor que el secreto en claro.
- Hallazgos redactados como documentación (definiciones abstractas) en vez de referidos a **líneas concretas** del archivo.
- "Severidad alta" en todo, sin diferenciar, pero con prosa pulida.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Recorre el YAML con una pregunta por línea (ver pista del README). ¿Cuántas fallas distintas llevas? Te falta(n) la(s) más sutil(es): mira el `on:` y el `${{ ... }}` dentro de un `run:`."
- **Pregunta socrática (nivel 2):** "Si yo abro un PR desde mi fork y cambio lo que corre, ¿qué de este workflow me deja ejecutar mi código con TUS secrets? ¿Por qué `pull_request` no haría eso y `pull_request_target` sí?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El hallazgo crítico es el **PPE**: `pull_request_target` corre con tus secrets incluso para forks, y al hacer checkout del código del PR ejecutas código ajeno con ellos. El título del PR en un `run:` es **expression injection**. Prioriza por impacto×explotabilidad, no por orden. Revisa la sección 6.1 de la lección."

## Conexión con el proyecto / capstone

- Auditar antes de construir: el alumno aprende a mirar un pipeline y ver el riesgo, de modo que el suyo (Capstone F5) no repita ninguna de estas 7 fallas. Es la otra cara del ejercicio `gates-de-seguridad-ci` (construir) — aquí evalúa (auditar).
