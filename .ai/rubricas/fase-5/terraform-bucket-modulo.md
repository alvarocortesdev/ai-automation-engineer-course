---
ejercicio_id: fase-5/terraform-bucket-modulo
fase: fase-5
sub_unidad: "5.11"
version: 1
---

# Rúbrica — Módulo de bucket testeable (Terraform)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay verificación automática
> (`terraform test` con `mock_provider`), pero el verde no basta: se evalúa que la config sea
> **limpia** (sin secretos, parametrizada) y que el alumno entienda **por qué** el mock permite
> testear sin AWS. Variaciones válidas existen (nombres de variables, formato).

## Objetivos evaluados

- O1: Escribir config Terraform mínima reusable (bloque terraform + provider pineado + resource + outputs).
- O2: Parametrizar con variables sin hardcodear; versioning condicional con ternario.
- O3: Verificar con `terraform test` + `mock_provider`, sin tocar la nube ni usar credenciales.

## Cómo verificar (corrector)

```bash
cd ejercicios/fase-5/terraform-bucket-modulo
terraform init   # descarga el provider AWS (internet, sin credenciales)
terraform test   # debe pasar: los run con command=plan y el mock_provider
terraform fmt -check   # no debe reportar diferencias
```

## Criterios y niveles

### C1 — Corrección (¿la config hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `terraform test` no pasa; falta el bucket o el versioning; recursos renombrados (rompen el test). |
| **en-progreso** | Pasa el assert del nombre/tags pero el versioning no depende de la variable (status hardcodeado), o faltan outputs. |
| **competente** | Bucket con `var.bucket_name` + tags por variable; versioning con ternario sobre `var.enable_versioning`; ambos outputs; `terraform test` verde. |
| **excelente** | Además `terraform fmt` limpio, validación de variables aprovechada, y el `run` propio cubre el caso `false` (Suspended). |

### C2 — Calidad de ingeniería (testing + clean config) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No completó el assert del versioning, o no agregó ningún `run` propio. |
| **en-progreso** | Completó el assert pero el `run` propio es trivial o no afirma nada nuevo. |
| **competente** | Assert del versioning correcto (`versioning_configuration[0].status`); un `run` propio con otra entrada y aserción real. |
| **excelente** | El `run` propio prueba el camino contrario (Suspended) y/o un caso borde; explica por qué `command = plan` basta para estas aserciones. |

### C3 — Seguridad / higiene · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Metió credenciales en algún `.tf`, o quitó el `.gitignore`, o ignoró el `.terraform.lock.hcl`. |
| **en-progreso** | Sin credenciales, pero no entiende por qué (no sabe de dónde las toma Terraform). |
| **competente** | Cero secretos en código; provider pineado intacto; entiende que el mock evita tocar AWS. |
| **excelente** | Explica que en la nube real las credenciales vienen del entorno/role, que el state nunca va a Git, y que el lock de deps SÍ. |

## Errores típicos a marcar

- `status = "Enabled"` hardcodeado en vez de `var.enable_versioning ? "Enabled" : "Suspended"`.
- Olvidar el `[0]` al referenciar `versioning_configuration` (es un bloque → lista).
- Renombrar los recursos (`this` → otro) y romper las referencias del test.
- Hardcodear el nombre del bucket o los tags en vez de usar variables.
- Pegar credenciales `access_key`/`secret_key` en el provider "para que funcione".
- Pensar que `terraform test` toca AWS (con `mock_provider` no toca nada; no hace falta cuenta).
- (transversal) verde sin entender: pasa el test pero no sabe explicar qué hace el mock.

## Señales de dependencia-IA

- Config impecable con features no pedidos (encryption, lifecycle, policies) que el alumno no puede justificar al nivel del ejercicio.
- `terraform test` verde pero no sabe explicar por qué `command = plan` + mock no necesita credenciales.
- Comentarios genéricos de IA ("This resource creates an S3 bucket") en inglés mezclados sin sentido.
- El `run` propio es una copia idéntica del dado, sin variar la entrada (no demuestra comprensión).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu bucket está bien, pero el versioning, ¿cambia si pongo `enable_versioning = false`? Pruébalo en un `run` y mira si tu status es fijo o condicional."
- **Pregunta socrática (nivel 2):** "¿Por qué `terraform test` corre sin que le des credenciales de AWS? ¿Qué hace exactamente `mock_provider \"aws\" {}`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El status del versioning debe ser `var.enable_versioning ? \"Enabled\" : \"Suspended\"`. El assert que falta apunta a `aws_s3_bucket_versioning.this.versioning_configuration[0].status` (ojo al `[0]`). Agrega un `run` con `enable_versioning = false` que afirme `\"Suspended\"`. Revisa secciones 4.2 y 4.4 de la lección."

## Conexión con el proyecto / capstone

- Escribir y **testear** config limpia es lo que llevarías al Capstone F5 si provisionas con Terraform: el `terraform test` encaja como gate en el CI/CD (5.3) y el provider pineado es el supply chain (5.4) de la infra. El ADR de por qué hacerlo lo cubre `terraform-state-panorama`.
