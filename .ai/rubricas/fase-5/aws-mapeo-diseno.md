---
ejercicio_id: fase-5/aws-mapeo-diseno
fase: fase-5
sub_unidad: "5.7"
version: 1
---

# Rúbrica — AWS para tu capstone: mapeo y diseño con least privilege

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: el `diseno.md`
> se corrige por la **calidad del criterio** (mapeo correcto, trade-off defendible, IAM least
> privilege, conciencia de costo), no por una redacción única. Servicios alternativos bien
> justificados (p. ej. ECS/Fargate en vez de App Runner) son válidos: lo que se evalúa es el porqué.

## Objetivos evaluados

- O1: Mapear EC2/S3/IAM/Lambda/RDS a los primitivos de cloud (5.5) + equivalente Azure.
- O2: Diseñar acceso con least privilege (role, no access keys; policy acotada por acción y ARN).
- O3: Estimar costo/riesgo (free tier 2026 + medida de control el día 1).
- O4: Elegir compute justificando el trade-off según el patrón de carga.

## Mapeo de referencia (checklist del corrector)

| Necesidad | Primitivo | AWS | Azure |
|---|---|---|---|
| Correr la API | compute | EC2 / ECS-Fargate / App Runner | VMs / App Service |
| Guardar archivos | object storage | S3 | Blob Storage |
| Base de datos | managed DB | RDS (PostgreSQL) | Azure DB for PostgreSQL |
| Tarea por evento | serverless | Lambda | Functions |
| Logs/métricas | observabilidad | CloudWatch | Monitor / App Insights |
| Secretos | config 12-factor | Secrets Manager / SSM Param Store | Key Vault |
| (control de acceso transversal) | identity & access | IAM | Entra ID + RBAC |

## Criterios y niveles

### C1 — Mapeo de primitivos (¿traduce bien?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 6 filas, o errores de traducción (p. ej. "S3 = base de datos", "Lambda = VM"). |
| **en-progreso** | 6 filas pero falta el equivalente Azure en varias, o confunde EC2 con un servicio de contenedores. |
| **competente** | ≥6 filas correctas con primitivo + AWS + Azure; identifica IAM como transversal, no "un servicio más". |
| **excelente** | Además distingue EC2 (VM cruda) de ECS/App Runner (contenedor gestionado) y nombra Secrets Manager para la config. |

### C2 — IAM / least privilege (seguridad) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Propone access keys, o una policy con `Action: "*"` / `Resource: "*"`, o un bucket público. |
| **en-progreso** | Usa role pero la policy es demasiado amplia (`s3:*`, o `Resource: *`), o no explica el porqué del role. |
| **competente** | Policy con acciones **enumeradas** (`s3:GetObject` + logs) y `Resource` acotado a ARN; explica role vs key. |
| **excelente** | Separa statements (S3 / logs), acota cada ARN, y conecta con credenciales temporales del execution role / instance metadata; menciona IAM Identity Center para humanos. |

### C3 — Compute con trade-off · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige sin justificar, o "Lambda porque es lo más nuevo/serverless". |
| **en-progreso** | Justifica débil ("EC2 porque la conozco") sin pesar patrón de carga. |
| **competente** | Liga la elección al patrón de carga (API de tráfico parejo → contenedor always-on; tarea por evento → Lambda) y menciona cold start o costo. |
| **excelente** | Compara 2+ opciones, pesa costo/operación/latencia, y deja la decisión como un mini-ADR. |

### C4 — Costo / riesgo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Afirma "free tier 12 meses" (desactualizado) o ignora el costo. |
| **en-progreso** | Sabe que cambió pero no concreta la medida de control. |
| **competente** | Describe el modelo de créditos 2026 (≤USD 200, 6 meses) y propone un AWS Budget con alarma el día 1. |
| **excelente** | Además anota que RDS cobra por hora aunque esté "parada ≤7 días" y prioriza apagar/destruir recursos de prueba. |

## Errores típicos a marcar

- "Aprender AWS = empezar de cero": no captó que es traducción de primitivos (señal de que no leyó la sección 1).
- Access keys pegadas en la app o en variables de entorno (anti-patrón #1).
- Policy con `*` en `Action` o `Resource` presentada como "least privilege".
- Elegir Lambda para una API de tráfico constante sin notar cold start / costo always-on.
- Creer que el free tier da 12 meses gratis (cambió en julio 2025).
- Confundir RDS con serverless ("solo pago cuando consulto").
- (transversal) falta un solo trade-off defendible; el diseño no tiene ADR ni razón detrás de las elecciones.

## Señales de dependencia-IA

- Tabla de mapeo perfecta y exhaustiva pero **sin** la decisión de compute justificada ni la medida de costo (copia el "qué", no el "por qué").
- Policy IAM impecable que el alumno no puede defender ("¿por qué `GetObject` y no `s3:*`?" sin respuesta).
- Menciona servicios sofisticados (Aurora Serverless v2, Step Functions) impropios del nivel, sin justificar por qué encajan.
- Cifras de free tier genéricas sin la consecuencia práctica (la boleta sorpresa).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu tabla mapea bien, pero ¿tu decisión de compute pesa el patrón de carga? Una API de tráfico parejo, ¿es el caso ideal de Lambda? Revisa el trade-off de la sección 4.6."
- **Pregunta socrática (nivel 2):** "Si tu app en EC2 necesita leer un bucket, ¿qué pasa si pegas una access key y se filtra en un log? ¿Qué le da a tu app las credenciales sin que tú escribas ningún secreto?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Cambia las access keys por un **IAM role** con instance profile; la policy debe enumerar `s3:GetObject` sobre el ARN del bucket (no `s3:*`, no `Resource: *`). Para el costo, el free tier 2026 son créditos por 6 meses: agrega un AWS Budget con alarma el día 1. Revisa secciones 4.3 y 5."

## Conexión con el proyecto / capstone

- Este diseño **es** el borrador del ADR de despliegue del Capstone F5 si lo llevas a AWS: justifica cloud, servicios, IAM y costo antes de tocar la consola. La otra mitad (escribir la Lambda) la cubre `aws-lambda-s3-procesador`.
