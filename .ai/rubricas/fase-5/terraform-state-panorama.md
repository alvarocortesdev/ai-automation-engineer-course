---
ejercicio_id: fase-5/terraform-state-panorama
fase: fase-5
sub_unidad: "5.11"
version: 1
---

# Rúbrica — Diseña el state y el panorama IaC de tu proyecto

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: el `diseno.md`
> se corrige por la **calidad del criterio** (entiende el problema, distingue declarativo/imperativo,
> diseña el state bien, elige Terraform/OpenTofu con justificación), no por una redacción única.

## Objetivos evaluados

- O1: Explicar el problema que IaC resuelve (no-reproducibilidad + config drift) con un ejemplo concreto.
- O2: Distinguir declarativo (estado deseado, idempotente) de imperativo (los pasos).
- O3: Diseñar el state remoto compartido (backend S3 + `use_lockfile`) y por qué el state no va a Git.
- O4: Decidir Terraform (BSL) vs OpenTofu (MPL) con trade-off defendible.

## Criterios y niveles

### C1 — El problema y el modelo declarativo · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | "Terraform es para crear infra" sin nombrar reproducibilidad ni drift; confunde declarativo con un script. |
| **en-progreso** | Nombra reproducibilidad o drift pero en abstracto (sin ejemplo); explica declarativo a medias. |
| **competente** | Da un **ejemplo concreto** de drift/no-reproducibilidad y explica declarativo+idempotencia con el caso de "apply dos veces". |
| **excelente** | Además contrasta con un script de bash imperativo (con `if exists`) y nombra que Terraform calcula el diff mínimo. |

### C2 — Diseño del state (seguridad) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Propone commitear el state a Git, o no menciona dónde vive; o usa `dynamodb_table` como si fuera la única opción sin saber que está deprecado. |
| **en-progreso** | Dice "backend remoto" pero el bloque está incompleto/incorrecto, o da menos de 3 razones de por qué no va a Git. |
| **competente** | Bloque `backend "s3"` correcto con `encrypt` y **`use_lockfile`**; 3 razones sólidas (secretos en texto plano, colisión/locking, no auditable en Git). |
| **excelente** | Además explica el `.gitignore` del state, que el `.terraform.lock.hcl` SÍ va a Git, y por qué `use_lockfile` reemplazó a DynamoDB. |

### C3 — Terraform vs OpenTofu (criterio de mercado) · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige, o "el más popular/el que sea" sin razón. |
| **en-progreso** | Elige pero la justificación es superficial ("OpenTofu es open source y ya"). |
| **competente** | Justifica con el trade-off real: licencia BSL vs MPL, **a quién afecta** (al usuario que corre `apply` casi nada; al SaaS que revende, mucho), compatibilidad de comandos. |
| **excelente** | Menciona contexto 2026 (Linux Foundation/CNCF, IBM compró HashiCorp, diferenciadores como state encryption nativo en OpenTofu) sin sobrevender. |

### C4 — Comunicación / ADR · mapea: O1–O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Texto suelto sin estructura; falta la regla de oro. |
| **en-progreso** | Cubre las secciones pero sin tono de decisión defendida. |
| **competente** | Las 5 secciones presentes; la regla de oro ("una vez de Terraform, se cambia solo por Terraform") está. |
| **excelente** | Se lee como un ADR real: contexto → decisión → consecuencia, defendible ante un equipo. |

## Errores típicos a marcar

- Tratar a Terraform como lenguaje imperativo ("primero crea, luego un if").
- Proponer commitear el state a Git, o creer que es un caché regenerable.
- Usar `dynamodb_table` sin saber que el locking nativo (`use_lockfile`) lo reemplazó en 1.11.
- Creer que la BSL le afecta al que solo corre `apply` contra su propia infra (no es así).
- Olvidar la regla de oro sobre cambios manuales (drift).
- (transversal) ningún trade-off defendible: elige OpenTofu o Terraform "porque sí".

## Señales de dependencia-IA

- Explicación impecable de la BSL/OpenTofu pero sin poder responder "¿y a ti, que corres apply contra tu infra, te afecta?".
- Bloque `backend` perfecto que el alumno no puede defender ("¿por qué `encrypt = true`?" sin respuesta).
- Menciona conceptos avanzados (state encryption, workspaces, `import`) impropios del nivel sin justificar por qué encajan.
- Problema descrito en abstracto/genérico, sin el ejemplo concreto que solo da quien lo vivió.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu diseño del backend está bien, pero ¿das 3 razones reales de por qué el state no va a Git? Una es 'tiene secretos'; ¿cuál es la del trabajo en equipo?"
- **Pregunta socrática (nivel 2):** "Si borras el `terraform.tfstate`, ¿se borran los recursos reales? ¿Qué pasa en el próximo `apply`? Eso te dice qué ES el state."
- **Dirección concreta (nivel 3, sólo tras intento real):** "Cierra C2: el state va en backend remoto cifrado con `use_lockfile` (no DynamoDB) y en `.gitignore`; las 3 razones son secretos en texto plano, falta de locking (colisión de equipo) y no-auditable. Para C3, ancla tu decisión en 'a quién afecta la BSL'. Revisa secciones 4.6 y 5 de la lección."

## Conexión con el proyecto / capstone

- Este `diseno.md` **es** el ADR de IaC del Capstone F5 si decides provisionar con Terraform: justifica el modelo, el state y la herramienta antes de escribir una línea de HCL. La otra mitad (escribir la config y testearla) la cubre `terraform-bucket-modulo`.
