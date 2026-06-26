# Ejercicio 3.9 — Diseña los puertos de una feature (y decide dónde NO ponerlos)

> **Modalidad: a mano (razonamiento y diseño, sin IA, sin código que correr).** Entrena el criterio que
> separa a un semi-senior: decidir qué es dominio y qué es adaptador, qué merece un puerto y —tan
> importante— qué NO lo merece (la sobre-ingeniería mata tantos proyectos como el acoplamiento).

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.9` Ports & adapters / hexagonal light
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Demostrar, por escrito y con un diagrama, que sabes (1) separar dominio puro de adaptadores, (2) proponer
los puertos justos con sus métodos, (3) decidir con criterio "light" dónde un puerto paga y dónde es
ceremonia, y (4) dibujar la **dirección de las dependencias** correctamente. Sin este criterio, "sé
hexagonal" se convierte en 6 capas y mappers por todos lados en un CRUD de 200 líneas.

## 📋 Contexto

En el capstone tendrás features que tocan varios sistemas externos. La hexagonal *light* te dice dónde
trazar límites para que el código sea testeable y cambiable, **sin** inflarlo. Este ejercicio es puro
criterio: no hay código que pase un test, hay decisiones que defender.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Razona antes de escribir.
2. Solo entonces, consulta la **documentación oficial** (`typing.Protocol`; FastAPI — *Dependencies*) y la
   lección (secciones 4.2, 4.3 y 4.9) para validar.
3. **Solo al final**, usa IA para *revisar* tu diseño — no para generarlo.
4. Mañana, redibuja el hexágono de memoria y explícalo en voz alta a alguien.

## La feature a diseñar

Te piden implementar, en el backend FastAPI del capstone, esta feature:

> **"Registrar un pago"**: cuando llega un pago (monto, email del cliente, id de la orden), el sistema debe:
> 1. **Validar** la regla de negocio: el monto debe ser positivo y la orden no puede estar ya pagada.
> 2. **Persistir** la transacción del pago en la base de datos (Postgres).
> 3. **Enviar** un recibo por **email** al cliente (vía un proveedor externo, p. ej. un SMTP o una API tipo Resend/SendGrid).
> 4. **Notificar** a un **webhook externo** del comercio (un `POST` HTTP a una URL configurada) con el resultado.
> 5. Formatear el monto a texto legible para el recibo (p. ej. `15000` → `"$15.000 CLP"`).

## Las tres micro-decisiones (el corazón del ejercicio)

Para **cada una** de estas tres piezas, decide **PUERTO SÍ** o **PUERTO NO**, y justifica con el criterio
de la lección (¿hay testabilidad real o un punto de cambio probable? ¿o sería sobre-ingeniería?):

- **D1 — El envío de email** (paso 3).
- **D2 — El formateo del monto a texto legible** (paso 5).
- **D3 — La notificación al webhook externo** (paso 4).

## 🛠️ Qué entregar (deja estos archivos en esta carpeta)

### `diseno.md`

1. **Clasificación**: lista cada una de las 5 piezas de la feature y marca si es **dominio puro** o
   **adaptador** (y de qué tipo: entrada/salida).
2. **Puertos propuestos**: para cada puerto que introduzcas, dale un nombre y enumera sus métodos con
   firmas (estilo `enviar_recibo(email: str, cuerpo: str) -> None`). No escribas la implementación.
3. **Las tres micro-decisiones (D1, D2, D3)**: para cada una, **PUERTO SÍ / PUERTO NO** + 2–3 líneas de
   justificación defendible. Al menos una debe ser **"PUERTO NO"** bien argumentada.
4. **Testabilidad**: explica en 3–4 líneas cómo testearías la regla de negocio del paso 1 **sin** enviar
   un email real, sin pegarle al webhook y sin levantar Postgres (qué doble pondrías en lugar de qué).
5. **Seguridad (1 línea)**: el webhook externo recibe datos y la URL es configurable — menciona **un**
   riesgo de seguridad a tener en cuenta al hacer ese `POST` saliente (pista: piensa en SSRF / validar la
   URL de destino; lo verás a fondo en [`3.13`](/fase-3-backend/3-13-owasp-top10-web/)).

### `diagrama.md`

Un diagrama **Mermaid** (`flowchart`) del hexágono que muestre: el adaptador de entrada (HTTP), el
dominio (servicio + reglas) al centro, los puertos, y los adaptadores de salida. **Todas** las flechas de
dependencia deben apuntar hacia el dominio (o los adaptadores implementando los puertos); **ninguna** debe
salir del dominio hacia un adaptador concreto.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Clasificaste las 5 piezas (dominio vs adaptador) correctamente.
- [ ] Cada puerto propuesto tiene una razón defendible (algo que mockear o que podría cambiar), no "porque sí".
- [ ] Al menos una micro-decisión es **"PUERTO NO"** bien justificada (detectaste la sobre-ingeniería).
- [ ] El diagrama tiene todas las flechas apuntando hacia el dominio; ninguna sale del dominio hacia la infra.
- [ ] Explicaste cómo testear la regla de negocio sin email, webhook ni DB.
- [ ] Mencionaste el riesgo de seguridad del `POST` saliente.
- [ ] Puedes defender **sin notas** por qué el formateo de monto NO merece un puerto.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Dominio puro:** la regla "monto positivo y orden no pagada" (paso 1). No toca el mundo exterior → no necesita puerto, es lógica pura sobre datos.
- **Adaptadores de salida (con puerto):** persistencia (DB), email y webhook son cosas **lentas, con efectos, que querrás mockear en tests o cambiar de proveedor**. Candidatos claros a puerto.
- **El formateo del monto** (`15000 -> "$15.000 CLP"`) es una **función pura**: no toca DB, ni red, ni nada externo; ya es trivial de testear sola. Ponerle un puerto (`FormateadorDeMonto`) sería sobre-ingeniería salvo que de verdad necesitaras intercambiar formatos por país en runtime —y aun así, una función o una estrategia simple basta—. Ésta es tu "PUERTO NO".
- **Testabilidad:** al servicio le inyectas dobles que cumplen los puertos `RepositorioPagos`, `EnviadorDeEmail` y `NotificadorWebhook`; el doble registra "se llamó con estos argumentos" sin efectos reales. La regla del paso 1 se prueba con todos esos dobles, cero infraestructura.
- **Seguridad:** un `POST` a una URL configurable es un vector de **SSRF** — un atacante podría apuntar la URL a un servicio interno. Hay que validar/limitar el destino.

Repasa las secciones 4.2, 4.3 y 4.9 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `diseno.md` + `diagrama.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/disenar-puertos-cobranza.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/disenar-puertos-cobranza.md` — no la mires
antes de intentarlo.
