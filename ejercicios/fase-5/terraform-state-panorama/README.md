# Diseña el state y el panorama IaC de tu proyecto

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.11` Terraform / IaC
**Ruta:** opcional / profundización · **Timebox:** 30–40 min · **Modalidad:** a mano (diseño/razonamiento)

## 🎯 Objetivo

Escribir el **ADR de IaC** del capstone de la fase: las decisiones de infraestructura como código,
defendidas. No escribes HCL aquí; escribes **criterio**. Al terminar sabrás explicar qué problema
resuelve Terraform, por qué es declarativo, cómo se cuida el **state**, y por qué existe OpenTofu.

## 📋 Contexto

El capstone de la Fase 5 no exige Terraform en su Definition of Done. Este ejercicio te obliga a
razonar las decisiones que tomarías **si** llevaras tu infra a IaC, y a escribirlas como un ADR —el
documento que un equipo revisa antes de adoptar una herramienta—. La pieza más delicada es el
**state**: dónde vive, cómo se comparte, por qué nunca va a Git. No necesitas cuenta de cloud ni
ejecutar nada: es 100% diseño en `diseno.md`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Diseña con lo que entendiste, aunque dudes.
2. Solo entonces, consulta **documentación oficial** (Terraform State, Backend S3, OpenTofu).
3. **Solo al final**, usa IA para *revisar y explicar* tu diseño — no para *generarlo*.
4. Mañana, **reescribe de memoria** qué es el state y por qué no va a Git. Si no puedes, no lo
   aprendiste todavía.

## 🛠️ Instrucciones

Completa `diseno.md` (hay una plantilla en este directorio) con cinco secciones:

1. **El problema** (3–4 líneas): ¿por qué desplegar el capstone clickeando la consola es un problema?
   Nombra **config drift** y **reproducibilidad** con un ejemplo concreto (algo que ya te pasó).
2. **Declarativo vs imperativo** (2–3 líneas): con el ejemplo de "correr `apply` dos veces", explica
   por qué Terraform es declarativo e idempotente, y en qué se diferencia de un script de bash.
3. **Diseño del state**: ¿dónde vive, cómo se comparte en equipo, cómo se bloquea? Escribe el bloque
   `backend` que usarías (S3 con `use_lockfile`, o el equivalente de tu cloud) y da **3 razones** por
   las que el state nunca va a Git.
4. **Terraform vs OpenTofu** (3–4 líneas): elige uno y **justifica** el trade-off (BSL vs MPL,
   compatibilidad, a quién le importa de verdad).
5. **Una regla de oro** (1 línea): sobre cambios manuales una vez que un recurso es de Terraform.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Explicas el problema con un **ejemplo concreto** de drift, no en abstracto.
- [ ] Distingues declarativo de imperativo con el caso de la **idempotencia**.
- [ ] El bloque `backend` es correcto y usas **`use_lockfile`** (no DynamoDB) o el equivalente actual.
- [ ] Das **3 razones** por las que el state no va a Git (al menos: secretos en texto plano, colisión
      de equipo / falta de locking).
- [ ] Tu elección Terraform/OpenTofu tiene un **trade-off defendible**, no "porque es el más popular".
- [ ] Puedes **explicar sin notas** qué es el state y qué pasa si lo borras.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el problema, piensa en algo que YA te pasó: creaste un recurso a mano, pasaron semanas y no
recuerdas la config exacta (no-reproducibilidad); alguien lo tocó y nadie sabe qué cambió (drift).
Para el backend, parte del bloque de la sección 4.6 de la lección y adáptalo a tu cloud y tu proyecto.
Para Terraform vs OpenTofu, la pregunta clave no es "cuál es mejor" sino **"¿a quién le afecta la
BSL?"** — a ti, que corres `apply` contra tu propia infra, casi nada; a un SaaS que revende Terraform,
mucho. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (`diseno.md` en este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/terraform-state-panorama.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/terraform-state-panorama.md` — no la
mires antes de intentarlo de verdad.
