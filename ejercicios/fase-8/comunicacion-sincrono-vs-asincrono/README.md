# Ejercicio 8.4a — Decisor: ¿llamada síncrona o evento asíncrono?

> **Modalidad: a mano (razonamiento, sin IA).** Este ejercicio entrena el **juicio** de comunicación
> entre servicios: decidir con la pregunta que manda ("¿el que llama necesita la respuesta para
> continuar?") en vez de con la moda. No hay código de producción; hay decisiones defendidas. Es
> exactamente el tipo de pregunta que cae en una entrevista de system design.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.4` Comunicación entre servicios
**Ruta:** opcional / profundización · **Timebox:** 30–40 min

## 🎯 Objetivo

- **O1** — Decidir, para cada salto de comunicación, entre **síncrono** (REST/gRPC) y **asíncrono**
  (cola/evento), nombrando la **pregunta que manda**.
- **O2** — Clasificar cada salto asíncrono como **comando** o **evento**, nombrar el **modelo de
  consistencia** (eventual) que asume y **una anomalía** concreta a mitigar.

## 📋 Contexto

Hacer síncrono lo que debía ser un evento acopla servicios que deberían ser independientes y fragiliza el
flujo principal; hacer asíncrono lo que el usuario necesita ya, complica sin beneficio. Este ejercicio te
obliga a separar **consultas que necesito ahora** (síncronas) de **efectos secundarios y hechos que otros
observan** (asíncronos), y a reconocer la **consistencia eventual** que aceptas al desacoplar. Alimenta
directo el capstone de la fase, donde diseñas la comunicación de tres sistemas y la justificas en ADRs.

## 📏 Primero-Sin-IA

1. Resuelve los **seis saltos** solo, a mano, dentro del timebox. Está bien dudar en el ambiguo.
2. Solo entonces consulta la lección (secciones 4.2, 4.3 y 4.5).
3. **Solo al final**, usa IA para *revisar y corregir* tu razonamiento — no para *generarlo*.
4. Mañana, vuelve a decidir el caso ambiguo de memoria y ve si llegas a la misma defensa.

## 🛠️ Instrucciones

Resuelve los **seis saltos** en `decisiones.md` (hay una plantilla en este directorio). Para **cada uno**,
escribe: (a) tu decisión (**síncrono** / **asíncrono**); (b) si es asíncrono, si es **comando** o
**evento** y por qué; (c) la **pregunta que manda** que justifica la decisión; y (d) para los asíncronos,
el **modelo de consistencia** (eventual) más **una anomalía** concreta (duplicado / orden /
read-your-writes) con su mitigación. En el **caso ambiguo**, además, el **trade-off explícito** que rompe
el empate.

### Los saltos

1. **Veredicto de fraude.** El checkout pregunta al servicio de fraude "¿apruebo esta transacción?" antes
   de cobrar la tarjeta.
2. **Analítica de ventas.** Tras confirmar el pedido, hay que sumar la venta al dashboard de analítica.
3. **Factura por correo.** El sistema debe generar la factura PDF y enviarla por correo (puede tardar
   segundos).
4. **Precio en la página.** Una página de producto necesita el precio actual para mostrarlo al usuario.
5. **Alta de usuario (fan-out).** Cuando un usuario se registra, deben reaccionar: correo de bienvenida,
   alta en el CRM y emisión de un cupón.
6. **Caso ambiguo (decídelo y defiéndelo).** Al confirmar un pedido, el sistema debe **reservar stock**.
   El equipo duda: ¿llamada **síncrona** a `Inventario` (el usuario sabe al instante si su pedido procede,
   pero el checkout se cae si `Inventario` se cae) o **evento** `PedidoConfirmado` que `Inventario`
   consume y, si no hay stock, **compensa** (cancela el pedido) después? No hay respuesta obvia: elige una
   y defiéndela contra la otra.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Cada decisión nombra la **pregunta que manda** (no "es más moderno", "más rápido" ni "escala mejor"
      sin contexto).
- [ ] Cada salto **asíncrono** se clasifica correctamente como **comando** (un destinatario que ejecuta) o
      **evento** (un hecho que varios observan).
- [ ] Cada salto asíncrono nombra el **modelo de consistencia** (eventual) y **una anomalía** concreta a
      mitigar con su mitigación (idempotencia / orden por clave / leer del dueño del dato).
- [ ] El **caso 6** se resuelve con un **trade-off explícito** (una fuerza a favor y una en contra), no
      esquivándolo.
- [ ] Puedes **defender tus seis decisiones sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/comunicacion-sincrono-vs-asincrono/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará tu **razonamiento** (la pregunta que manda, la clasificación comando/evento y el
trade-off), no si coincidiste con una respuesta única — el caso 6 admite ambas decisiones bien defendidas.
