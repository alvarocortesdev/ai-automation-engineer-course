# Ejercicio 8.4b — Rediseña un flujo síncrono frágil a event-driven

> **Modalidad: a mano (diseño, sin IA).** Tomas una cadena toda síncrona y frágil y la rediseñas a
> event-driven, decidiendo qué queda síncrono, qué pasa a evento, qué garantía cambias a **eventual** y
> cómo blindas lo asíncrono (idempotencia, outbox). Produces un diagrama Mermaid y un ADR. No hay código
> de aplicación; hay un diseño defendido con sus trade-offs.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.4` Comunicación entre servicios
**Ruta:** opcional / profundización · **Timebox:** 40–45 min

## 🎯 Objetivo

- **O1** — Rediseñar un flujo síncrono en cadena separando el **corazón** (lo que el usuario necesita
  consistente al instante) de los **reactores** (efectos secundarios que pasan a consumir un **evento**).
- **O2** — Articular en un **ADR** el trade-off de la consistencia **eventual** (qué deja de ser inmediato,
  qué riesgo nuevo aceptas) y blindar lo asíncrono contra **dual write** (outbox) y **at-least-once**
  (idempotencia).

## 📋 Contexto

Una cadena toda síncrona tiene un problema silencioso: la disponibilidad del flujo principal queda atada a
la del **eslabón más débil**. Si el registro de un usuario depende síncronamente del CRM, una caída del CRM
**impide registrarse**. Event-driven rompe ese acoplamiento —al precio de la consistencia eventual y de los
riesgos de duplicado/orden/dual write. Este ejercicio entrena exactamente el rediseño que pide el capstone
de la fase y que cae en entrevistas de system design.

## 📏 Primero-Sin-IA

1. Diseña **solo**, a mano, dentro del timebox. Dibuja el Mermaid en papel primero si ayuda.
2. Solo entonces consulta la lección (secciones 4.2–4.5 y las misconceptions de la sección 5).
3. **Solo al final**, usa IA para *revisar y corregir* tu diseño — no para *generarlo*.
4. Mañana, reescribe el ADR de memoria y ve si nombras el mismo trade-off.

## 🛠️ El flujo de partida (todo síncrono y frágil)

Hoy, registrar un usuario es **una sola cadena de llamadas HTTP síncronas**; si **cualquiera** falla, el
registro entero falla y el usuario ve un error:

```
POST /registro
  └─ 1. alta en la BD de usuarios          (síncrono)
  └─ 2. correo de bienvenida               (síncrono)  ← si el SMTP está caído, NO te registras
  └─ 3. crear contacto en el CRM externo   (síncrono)  ← si el CRM responde lento, el registro tarda
  └─ 4. emitir un cupón de bienvenida      (síncrono)
  └─ 5. registrar el alta en analítica     (síncrono)
  → 200 solo si los CINCO pasos salieron bien
```

Produce un documento `diseno.md` (hay una plantilla en este directorio) con **cuatro partes**:

1. **Qué queda síncrono y qué pasa a evento:** por cada uno de los 5 pasos, la decisión y la **pregunta que
   manda**.
2. **Diagrama Mermaid** del flujo rediseñado: la parte síncrona (el alta) y el **evento**
   (`UsuarioRegistrado`) con sus consumidores.
3. **ADR corto** (contexto · decisión · alternativas · trade-off) titulado "Registro event-driven con
   consistencia eventual". El trade-off **debe** nombrar qué **renuncias** y qué **riesgo nuevo** aceptas.
4. **Blindaje de lo asíncrono:** cómo publicas el evento sin **dual write** (pista: outbox) y cómo cada
   consumidor se vuelve **idempotente** ante el at-least-once.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **alta** (lo que hace que la cuenta "exista") queda **síncrona**; correo, CRM, cupón y analítica
      pasan a **consumir un evento**, no a bloquear el registro.
- [ ] El **diagrama Mermaid renderiza** y distingue el salto síncrono del **fan-out por evento** (un
      publicador, varios consumidores independientes).
- [ ] El **ADR** nombra al menos **una renuncia real** (algo deja de ser inmediato) **y** un **riesgo nuevo**
      (duplicado / orden / dual write), no solo las ventajas.
- [ ] El diseño menciona **idempotencia** en los consumidores **y** una estrategia contra el **dual write**
      (outbox o equivalente), no "publico el evento y ya".
- [ ] Puedes **defender el diseño sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/comunicacion-rediseno-event-driven/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará tu **diseño y tu trade-off** (la separación corazón/reactores, el modelo de
consistencia y el blindaje), no una solución única — caben variantes válidas si el razonamiento es sólido.
