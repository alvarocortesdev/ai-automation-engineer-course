# mapeo-primitivos-azure — Mapea una app de IA a primitivos de Azure

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.6` Azure profundización
**Ruta:** opcional / profundización · **Timebox:** 35–45 min · **Modalidad:** a-mano (diseño/razonamiento)

## 🎯 Objetivo

Diseñar, a mano y sin IA, el despliegue de una app de IA sobre Azure: mapear cada componente a su
**primitivo cloud** y al **servicio Azure** correcto, justificar la elección por el **perfil de
carga** (ráfaga vs. sostenido, administrado vs. propio) y **defender dos trade-offs** con criterio
de costo/seguridad/latencia, sin marketing.

## 📋 Contexto

En una entrevista no te van a pedir que hagas clic en el portal: te van a pedir que **decidas** qué
servicio resuelve qué y por qué. Este ejercicio entrena ese músculo —el que separa "usé Azure" de
"diseñé sobre Azure"— y alimenta el [Capstone F5](/fase-5-devops/proyecto/) si Azure es tu cloud.

## 📐 El brief

Diseña el despliegue en Azure de un **asistente de soporte**:

1. **Recibe tickets por email** (llegan a ráfagas, en cualquier momento).
2. **Clasifica** cada ticket con un LLM (urgencia + categoría).
3. **Busca** en una base de conocimiento (KB) de artículos de ayuda.
4. **Genera** un borrador de respuesta con el LLM, citando la KB.
5. Una **API web** deja a los agentes humanos revisar y editar el borrador (tráfico sostenido).
6. Los **tickets y borradores** se guardan para auditoría.

## 📏 Primero-Sin-IA

1. Diséñalo **solo**, a mano (timebox arriba). Razona el perfil de carga de cada pieza.
2. Solo entonces consulta la **documentación oficial** de los servicios (ver Recursos de la lección).
3. **Solo al final**, usa IA para *criticar tu diseño* — no para *generarlo*.
4. Mañana, **redibuja el mapa de memoria** para otra app distinta.

## 🛠️ Instrucciones

Completa `mapeo.md` (ya tiene la plantilla). Para **cada** componente (al menos 5):

1. **Primitivo** de la [5.5](/fase-5-devops/5-5-cloud-troncal/): compute / serverless / storage / IAM / búsqueda-DB / inferencia.
2. **Servicio Azure** elegido + **por qué ese** (una razón ligada al perfil de carga).
3. Un **diagrama Mermaid** del flujo y dependencias (con al menos una relación de IAM / Managed Identity).

Cierra con **dos trade-offs defendidos** (un párrafo cada uno), eligiendo de:
- Managed Identity vs. clave en variable de entorno.
- Azure OpenAI **pay-as-you-go** vs. **PTU** (capacidad reservada).
- Azure AI Search vs. `pgvector` para la KB.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Cada componente tiene **primitivo + servicio + justificación** ligada al perfil de carga (no "es de Azure").
- [ ] El diagrama Mermaid muestra el flujo y al menos **una** relación de Managed Identity.
- [ ] El **ingest/clasificación por evento** está en **Functions** (serverless) y la **API** en **App Service**, con el porqué.
- [ ] Tus **dos trade-offs** pesan costo/seguridad/latencia con un argumento concreto.
- [ ] Reconoces al menos un caso donde **NO** usarías el servicio Azure (p. ej. pgvector para KB pequeña).
- [ ] Puedes **defender el diseño sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada componente pregúntate primero el **perfil de carga**: ¿corre por un evento puntual (un
email que llega) o atiende tráfico sostenido (una API que un humano consulta)? Lo primero grita
**Functions**; lo segundo, **App Service**. Clasificación y generación son llamadas a **Azure
OpenAI** (inferencia). La KB es **AI Search** *o* `pgvector` según volumen. Para los trade-offs,
ancla en escenarios concretos (PTU se justifica con tráfico **alto y predecible**). Revisa la tabla
del 4.1 de la lección.

</details>

## 🤖 Cómo pedir la corrección

Entrega a tu IA: tu `mapeo.md`, la **rúbrica** (`.ai/rubricas/fase-5/mapeo-primitivos-azure.md`) y
`.ai/INSTRUCCIONES-CORRECTOR.md`. No hay test automático: se corrige por la **solidez del
razonamiento**. La solución de referencia (`.ai/soluciones/fase-5/mapeo-primitivos-azure.md`) es para
el corrector — no la mires antes de intentarlo.
