# Ejercicio 3.7 — Diseña la API de un sistema de eventos

> **Modalidad: a mano (diseño/razonamiento, sin IA, sin servidor que correr).** Es el ejercicio
> que más se parece a una pizarra de entrevista: te dan un requisito en prosa y tienes que entregar
> el **diseño** de una API REST defendible. No se programa nada — se decide y se justifica.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.7` Diseño de APIs REST
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

A partir de un requisito en lenguaje natural, diseñar los **recursos**, **endpoints** y **status
codes** de una API REST; definir un **modelo de errores** consistente; tomar (y justificar) una
decisión de **paginación** y una de **versionado**; y escribir un **fragmento de contrato OpenAPI**
para los endpoints clave. Sin esto, "sé hacer APIs" es solo saber que existe `@app.get`.

## 📋 Contexto

Este diseño es, casi tal cual, el plano del **capstone de la fase** (API de producción). Cambiando
el dominio, el esqueleto que produzcas aquí es el que implementarás en FastAPI. Diseñar bien en
papel ahorra el doble de tiempo en código.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Razona antes de escribir.
2. Solo entonces, valida contra **documentación oficial** (MDN HTTP status codes; RFC 9457; OpenAPI spec).
3. **Solo al final**, usa IA para *revisar* tu diseño — no para generarlo.
4. Mañana, redibuja de memoria la tabla de endpoints y explica en voz alta cada status code.

## El requisito

> *"Queremos una plataforma de eventos. Un **organizador** crea **eventos** (cada uno con título,
> categoría, fecha/hora y un cupo máximo de asistentes). Un **asistente** puede **inscribirse** a un
> evento y **cancelar** su inscripción. La plataforma debe poder: listar los eventos próximos,
> filtrar eventos por categoría, ver la lista de inscritos de un evento, y ver a qué eventos está
> inscrito un asistente. Reglas de negocio: **no se puede inscribir a un evento que ya alcanzó su
> cupo**, ni a un **evento cuya fecha ya pasó**. Puede haber miles de eventos."*

## 🛠️ Qué entregar (deja estos archivos en esta carpeta)

### `diseno-api.md`

Completa la plantilla que ya viene en el archivo. Debe incluir, como mínimo:

1. **Recursos** — la lista de sustantivos del dominio convertidos en recursos (colección + elemento).
2. **Tabla de endpoints** — para cada operación: verbo + URL + status de éxito + si es idempotente.
   Incluye el CRUD de cada recurso **y** las acciones que no son CRUD (inscribirse, cancelar).
3. **Casos de error** — al menos: evento no existe, cuerpo inválido, evento lleno, evento ya pasó,
   sin autenticación, sin permiso. Para cada uno, el **status code** y una frase de por qué.
4. **Modelo de errores** — muestra un ejemplo de cuerpo `problem+json` (RFC 9457) para el caso
   "evento lleno", con su `Content-Type`.
5. **Listado y paginación** — cómo se filtra/ordena/pagina `GET /eventos`. Decide **offset o cursor**
   y **justifica** en 2–3 líneas (pista: "puede haber miles de eventos").
6. **Versionado** — elige **URL o header** y escribe un mini-ADR (contexto, decisión, consecuencia).

### `openapi.yaml`

Completa el esqueleto OpenAPI que viene en el archivo con **al menos dos** operaciones reales:
`POST /inscripciones` (incluye la respuesta `409` con `application/problem+json`) y
`GET /eventos` (incluye los parámetros de filtro y paginación que decidiste).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todas las URLs son **sustantivos**; ninguna acción quedó como verbo en la ruta.
- [ ] "Inscribirse" y "cancelar" están modeladas como recurso/cambio de estado, no como `/inscribir`.
- [ ] "Evento lleno" y "evento ya pasó" usan el status code de **conflicto con el estado** (no 400/404 a secas) y lo justificas.
- [ ] Hay un ejemplo de cuerpo `problem+json` con sus campos y el `Content-Type` correcto.
- [ ] La decisión offset-vs-cursor está **justificada**, no solo elegida.
- [ ] El mini-ADR de versionado tiene contexto, decisión y consecuencia.
- [ ] El `openapi.yaml` valida como YAML y describe al menos `POST /inscripciones` y `GET /eventos`.
- [ ] Puedes **defender sin notas** por qué elegiste cada status code dudoso.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Subraya los sustantivos del requisito: *evento, organizador, asistente, inscripción*. Esos son tus
recursos. "Inscribirse" **crea** una inscripción → `POST /inscripciones`. "Cancelar" la borra o
cambia su estado → `DELETE /inscripciones/{id}` o `PATCH`. "Evento lleno" y "evento pasado" no son
peticiones mal formadas (400) ni recursos inexistentes (404): chocan con el **estado actual** del
evento → `409 Conflict` (algunos defienden `422` para el de fecha; cualquiera de los dos es
aceptable si lo justificas). Con miles de eventos y scroll de "próximos", el cursor envejece mejor
que el offset. Revisa las secciones 4.2 a 4.7 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `diseno-api.md` + `openapi.yaml` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/disenar-api-rest-eventos.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/disenar-api-rest-eventos.md` — no la
mires antes de intentarlo de verdad.
