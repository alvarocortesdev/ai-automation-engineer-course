# Escribe un módulo de bucket testeable, verificado sin tocar la nube

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.11` Terraform / IaC
**Ruta:** opcional / profundización · **Timebox:** 40–45 min · **Modalidad:** código (HCL)

## 🎯 Objetivo

Escribir una configuración Terraform mínima y **reusable** (un bucket privado con versioning,
parametrizado), y verificarla con `terraform test` usando un **`mock_provider`** — sin credenciales,
sin AWS, sin gastar un peso. Es el hilo de **testing** aplicado a la infraestructura.

## 📋 Contexto

Probar infraestructura "de verdad" cuesta dinero y tiempo (crear recursos, esperarlos, borrarlos).
Terraform trae testing nativo: `terraform test` corre archivos `.tftest.hcl`, y `mock_provider`
simula al provider para que puedas afirmar sobre el **plan** sin tocar la nube. Aquí practicas
escribir config limpia (provider pineado, cero secretos, variables) y validarla en segundos.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que dudes de la sintaxis al principio.
2. Solo entonces, consulta **documentación oficial** (Terraform Language, `aws_s3_bucket`, tests).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe el `resource` del bucket de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Archivos en esta carpeta:
- `terraform.tf` — versión y provider pineados (**completo**, no lo toques).
- `variables.tf` — las tres variables declaradas (**completo**).
- `main.tf` — los recursos, con **TODOs** que completas.
- `outputs.tf` — con **TODOs**.
- `tests/bucket.tftest.hcl` — `mock_provider` + un `run` con un assert hecho y otro por completar.
- `.gitignore` — ya excluye el state y `.terraform/`.

Tu trabajo:

1. En `main.tf`, implementa `aws_s3_bucket.this` (usa `var.bucket_name`; tags `Environment =
   var.environment` y `ManagedBy = "Terraform"`) y `aws_s3_bucket_versioning.this` (status `"Enabled"`
   si `var.enable_versioning`, si no `"Suspended"`). **No cambies los nombres** de los recursos.
2. En `outputs.tf`, expón `bucket_id` (el `id`) y `bucket_arn` (el `arn`).
3. En `tests/bucket.tftest.hcl`, completa el assert que falta (versioning `"Enabled"` con
   `enable_versioning = true`).
4. Corre la verificación hasta el verde y agrega **un `run` tuyo** (p. ej. `enable_versioning = false`
   verificando `status == "Suspended"`).

Verificación (corre en tu máquina, sin AWS):

```bash
terraform init   # descarga el provider (necesita internet, NO credenciales de AWS)
terraform test   # corre los .tftest.hcl con el mock_provider, sin tocar la nube
terraform fmt    # formatea; no debe quedar nada por cambiar
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `terraform test` pasa: los `run` con `command = plan` validan tu config con el mock.
- [ ] `aws_s3_bucket.this` usa `var.bucket_name` y los tags por variable; **nada hardcodeado**.
- [ ] El versioning depende de `var.enable_versioning` (Enabled/Suspended), no un literal fijo.
- [ ] Los dos outputs (`bucket_id`, `bucket_arn`) existen y referencian el recurso.
- [ ] Completaste el assert que faltaba y agregaste **un `run` propio** con otra entrada.
- [ ] `terraform fmt` no reporta cambios y **no hay credenciales** en ningún `.tf`.
- [ ] Puedes **explicar sin notas** por qué `mock_provider` permite testear sin AWS.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el bucket, copia la estructura de la sección 4.2 de la lección pero reemplaza los literales por
`var.bucket_name` y `var.environment`. Para el versioning condicional, usa el ternario:
`status = var.enable_versioning ? "Enabled" : "Suspended"`. Para el assert que falta, el valor está en
`aws_s3_bucket_versioning.this.versioning_configuration[0].status` (es un bloque, por eso el `[0]`).
Para tu `run` propio, copia el existente, cambia `enable_versioning = false` y ajusta el assert a
`"Suspended"`. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/terraform-bucket-modulo.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/terraform-bucket-modulo.md` — no la mires
antes de intentarlo de verdad.
