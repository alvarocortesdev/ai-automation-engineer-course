# Ejercicio 5.5 — Despliega el contenedor en un servicio managed (seguro)

> **Modalidad: código (un script de despliegue).** Escribes el `deploy.sh` que pone tu contenedor
> en la nube **bien**: ingress público, identidad administrada (sin secretos), mínimo privilegio.
> **No necesitas una cuenta de Azure:** los tests **revisan tu script como texto** (un "lint" de
> seguridad), no lo ejecutan contra la nube. Si tienes créditos gratis, puedes correrlo de verdad.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.5` Cloud troncal
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Desplegar un contenedor en un servicio managed (**Azure Container Apps**) con **ingress público** y el **puerto** correcto.
- **O2** — Autenticar el pull de la imagen con una **identidad administrada**, sin admin user ni passwords de registry.
- **O3** — Asignar el acceso con **mínimo privilegio** (solo `acrpull` sobre el registry), evitando roles amplios como `Contributor`/`Owner`.

## 📋 Contexto

Es el **paso final de tu pipeline** de CI/CD (5.3): después de build + gates de seguridad (5.4), el
job de deploy corre un script como este. Hacerlo con identidad administrada y mínimo privilegio es
un entregable de seguridad del Definition of Done del capstone de la fase.

## 📏 Primero-Sin-IA (en este orden, timebox 45 min)

1. Escríbelo **solo**, a mano. Apóyate en el **mapa de pasos** de la sección 4.7 de la lección, pero **no copies** los comandos sin entenderlos: completa los `TODO` razonando cada flag.
2. Solo entonces, consulta la **documentación oficial** de la Azure CLI (enlaces en la sección 9 de la lección).
3. **Solo al final**, usa IA para *revisar* tu script —no para generarlo.
4. Mañana, reescríbelo de memoria. Si no salen los pasos en orden, vuelve a la lección.

## 🛠️ Instrucciones

1. Abre `deploy.sh` y completa los pasos marcados con `# TODO`. Tu script debe:
   - crear el **grupo de recursos** (`az group create`) y el **entorno** de Container Apps (`az containerapp env create`);
   - crear el **registry** y construir la imagen (`az acr create`, `az acr build`);
   - crear una **identidad administrada** (`az identity create`);
   - asignar **solo el rol `acrpull`** a esa identidad **sobre el registry** (`az role assignment create`) — jamás `Contributor`/`Owner`;
   - desplegar con `az containerapp create` usando `--ingress external`, `--target-port`, y el pull por `--registry-identity`/`--user-assigned` (sin `--admin-enabled`, sin `--registry-password`).
2. Añade **un comentario por cada paso** explicando *por qué*, no solo *qué*.
3. Corre los tests:

   ```bash
   pytest
   ```

4. Itera hasta que **todas las verificaciones pasen en verde**.

> Los tests solo necesitan Python + pytest (no instalan ni llaman a Azure). Validan que tu script
> tome las decisiones de seguridad correctas, no que el despliegue real funcione.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa en verde (todas las verificaciones).
- [ ] El script crea grupo, entorno, identidad y registry, y despliega la app.
- [ ] El pull va por **identidad administrada**: no hay `--admin-enabled true`, ni `--registry-password`, ni `--registry-username`.
- [ ] El rol asignado es **`acrpull`** (no `Contributor`/`Owner`).
- [ ] Hay un comentario de *por qué* en cada paso.
- [ ] Puedes **explicar sin notas**: qué flag hace pública la app, cuál evita guardar un secreto, y por qué `acrpull` y no `Contributor`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Tres flags llevan toda la seguridad del deploy: uno para la **exposición** (`--ingress`), uno para
el **puerto** (`--target-port`, debe coincidir con el que escucha tu FastAPI), y uno para la
**credencial** (`--registry-identity`, que nunca debe ser un password). Para el rol: piensa en lo
*único* que el contenedor necesita de IAM —leer su imagen— y busca el rol con ese nombre exacto
(empieza con `acr...`). El scope del rol es el **registry**, no la suscripción. Revisa la sección
4.5 y 4.7 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/desplegar-en-container-apps.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/desplegar-en-container-apps.md` — no la
mires antes de intentarlo de verdad.
