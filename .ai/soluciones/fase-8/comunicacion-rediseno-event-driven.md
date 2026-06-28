---
ejercicio_id: fase-8/comunicacion-rediseno-event-driven
fase: fase-8
sub_unidad: "8.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). No es una solución única: hay variantes
> válidas; lo que importa es el criterio (corazón síncrono vs reactores por evento, trade-off honesto,
> blindaje).

# Solución de referencia — Rediseña un flujo síncrono frágil a event-driven

## Parte 1 — Qué queda síncrono y qué pasa a evento

| Paso | Decisión | Pregunta que manda |
|---|---|---|
| 1. Alta en la BD de usuarios | **Síncrono** | El registro debe responder "tu cuenta existe"; sin esto no hay nada que confirmar. Es el **corazón**. |
| 2. Correo de bienvenida | **Evento** | Nadie espera el correo en línea; una caída del SMTP no debe impedir registrarse. |
| 3. Contacto en el CRM | **Evento** | El CRM es un sistema externo (lento/caído a veces); el alta no debe depender de su disponibilidad. |
| 4. Cupón de bienvenida | **Evento** | Efecto secundario; puede emitirse segundos después. |
| 5. Registro en analítica | **Evento** | Reacción a un hecho; converge en segundos sin que nadie la espere. |

Clave: **un solo evento `UsuarioRegistrado`** con **cuatro consumidores independientes** (no cuatro
comandos que el registro dispara uno a uno). El emisor no conoce a los consumidores → un consumidor nuevo
(p. ej. "alta en newsletter") se suscribe sin tocar el registro.

## Parte 2 — Diagrama (forma esperada)

```mermaid
flowchart LR
    U[Usuario] -->|POST /registro| API[Servicio de Registro]
    API -->|1. INSERT usuario + outbox<br/>(misma transacción)| DB[(BD usuarios)]
    API -->|200 cuenta creada| U
    DB -.relay del outbox.-> B(("Broker / log<br/>topic 'usuarios'"))
    B -->|UsuarioRegistrado| C1[Correo bienvenida]
    B -->|UsuarioRegistrado| C2[Contacto CRM]
    B -->|UsuarioRegistrado| C3[Cupón]
    B -->|UsuarioRegistrado| C4[Analítica]
```

Lo importante del diagrama: (a) el alta es síncrona y responde antes del fan-out; (b) hay **un** evento y
**varios** consumidores independientes; (c) el evento sale vía **outbox** (no un publish suelto).

## Parte 3 — ADR (esqueleto correcto)

- **Contexto:** el registro es una cadena síncrona de 5 pasos; la disponibilidad del flujo = la del eslabón
  más débil (un CRM lento o un SMTP caído impiden registrarse).
- **Decisión:** el alta queda síncrona y consistente; correo, CRM, cupón y analítica pasan a consumir el
  evento `UsuarioRegistrado`.
- **Alternativas:** (1) dejar todo síncrono (rechazada: frágil, lenta); (2) cola de comandos por paso
  (rechazada: reacopla el emisor con cada consumidor); (3) evento con fan-out (elegida).
- **Trade-off honesto:**
  - **Renuncio a:** que correo/CRM/cupón sean inmediatos → **consistencia eventual** (~segundos de
    ventana). El usuario podría ver "cuenta creada" antes de que su cupón exista.
  - **Riesgo nuevo que acepto:** **dual write** (BD + publish no atómicos) y **duplicados** por
    at-least-once. Los cubro en la Parte 4.

## Parte 4 — Blindaje (esperado)

- **Dual write → outbox:** escribir el evento en una tabla `outbox` **dentro de la misma transacción** que
  el `INSERT` del usuario; un relay aparte lee la tabla y publica al broker. Así, "usuario guardado" y
  "evento pendiente de publicar" son atómicos.
- **At-least-once → idempotencia:** cada consumidor recuerda los `evento_id` ya procesados (o usa una clave
  natural única) y descarta repetidos → no dos correos, no dos cupones, no dos contactos en CRM.
- **(Opcional) Orden:** si llegaran `UsuarioRegistrado` y luego `UsuarioEliminado`, ordenarlos por clave
  (`user_id` → misma partición) o diseñar consumidores tolerantes a desorden.
- **(Excelente) Fallos del consumidor:** reintentos + **DLQ** (de 7.2) para mensajes envenenados; trazas
  con correlation ID para responder "¿dónde está mi evento?".

## Rango de soluciones aceptables
- Modelar 2–5 como **un** evento con fan-out (recomendado) o como eventos separados por capacidad: ambos
  válidos si los consumidores son independientes.
- Sustituir "outbox" por otra mitigación real del dual write (p. ej. CDC del log de la BD) es `excelente`.
- Es `incompleto` si el alta se vuelve asíncrona, si todo queda síncrono, o si el ADR no nombra ninguna
  renuncia.
- Es `en-progreso` si rediseña bien pero ignora dual write **o** idempotencia.
