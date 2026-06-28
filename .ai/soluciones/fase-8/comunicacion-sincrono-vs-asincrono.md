---
ejercicio_id: fase-8/comunicacion-sincrono-vs-asincrono
fase: fase-8
sub_unidad: "8.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Los saltos 1–5 tienen respuesta clara; el
> 6 es deliberadamente ambiguo y admite ambas decisiones bien defendidas.

# Solución de referencia — Decisor: ¿llamada síncrona o evento asíncrono?

## Respuestas canónicas (saltos 1–5)

### Salto 1 — Veredicto de fraude → **Síncrono**
- **Pregunta que manda:** el checkout **necesita** el veredicto para decidir si cobra. No puede continuar
  sin él → síncrono, consistencia fuerte.
- Variante aceptable: si el negocio tolera "cobrar y revisar fraude después", podría ser asíncrono con
  compensación —pero hay que defenderlo explícitamente; por defecto es síncrono.

### Salto 2 — Analítica de ventas → **Evento** (asíncrono)
- **Tipo:** **evento** (`PedidoConfirmado` / `VentaRegistrada`): es un hecho que analítica observa; el
  emisor no la conoce.
- **Pregunta que manda:** nadie espera en línea a que la analítica sume. No debe bloquear ni fragilizar el
  checkout.
- **Consistencia eventual + anomalía:** el dashboard converge en segundos; el at-least-once puede **contar
  doble** → idempotencia por `evento_id`.

### Salto 3 — Factura PDF por correo → **Asíncrono (comando)**
- **Tipo:** **comando** (`GenerarYEnviarFactura`): hay **un** responsable que debe ejecutar la acción; no
  es un broadcast. Encaja con una **cola** (repartir trabajo entre workers).
- **Pregunta que manda:** el usuario no debe esperar segundos a que el PDF se genere; y una caída del SMTP
  no debe romper nada aguas arriba.
- **Consistencia eventual + anomalía:** la factura llega "después"; el reintento puede mandar el correo
  **dos veces** → idempotencia (marcar factura ya enviada).
- Nota: aceptar "evento" en vez de "comando" es `competente` si el razonamiento de desacoplar es correcto;
  es `excelente` notar que tiene un único responsable (sabor comando).

### Salto 4 — Precio en la página → **Síncrono**
- **Pregunta que manda:** la página **necesita** el precio para renderizar al usuario ahora → síncrono.
- Matiz `excelente`: puede servirse de un **caché** (lo de 8.1) para latencia, pero el salto sigue siendo
  una consulta síncrona; el caché no lo convierte en asíncrono.

### Salto 5 — Alta de usuario (fan-out) → **Evento** (asíncrono)
- **Tipo:** **evento** (`UsuarioRegistrado`): es el caso canónico de evento —**un** hecho, **varios**
  observadores (correo, CRM, cupón), el emisor no los conoce y mañana entra uno nuevo sin tocar el
  registro.
- **Pregunta que manda:** ninguno de los tres reactores debe bloquear ni fragilizar el alta.
- **Consistencia eventual + anomalía:** correo/CRM/cupón convergen en segundos; at-least-once → cada
  consumidor idempotente (no dos cupones, no dos contactos en CRM).

## Salto 6 — Caso ambiguo (ambas defendibles): reservar stock

No hay respuesta única. Se evalúa el **trade-off explícito**.

**Defensa A — Síncrono a `Inventario` (certeza inmediata):**
- **Fuerza a favor:** el usuario sabe **al instante** si su pedido procede; no hay "confirmado y luego
  cancelado". UX limpia.
- **Renuncia/riesgo:** acopla el checkout a la disponibilidad de `Inventario` (si `Inventario` cae, no se
  confirma); la latencia se suma.
- **Desempate:** si el negocio considera **inaceptable** confirmar y cancelar después, gana síncrono.

**Defensa B — Evento `PedidoConfirmado` + compensación (desacople):**
- **Fuerza a favor:** el checkout no depende de `Inventario` arriba; amortigua picos; servicios
  independientes.
- **Renuncia/riesgo:** consistencia eventual → existe una ventana donde un pedido "confirmado" puede
  **cancelarse** si no había stock (saga con compensación, de 8.3); requiere UX honesta y idempotencia.
- **Desempate:** si el sobre-venta ocasional con compensación es tolerable (boletos, retail con backorder),
  gana el desacople.

> Ambas son **excelentes** si nombran una fuerza a favor, una en contra (la renuncia) y el desempate.
> Es **en-progreso** si decide sin nombrar qué renuncia. Es **incompleto** si esquiva el caso.

## Patrón de cierre (lo que debería notar)
Los síncronos (1, 4) comparten "el flujo necesita el dato ahora" (consultas). Los asíncronos (2, 3, 5)
comparten "nadie lo espera en línea / quiero aislar fallas" (reactores). 2 y 5 son **eventos** (hechos,
broadcast); 3 es **comando** (un responsable). El caso 6 es la frontera: certeza inmediata vs
desacoplamiento, mediada por la tolerancia del negocio a la compensación.

## Rango de soluciones aceptables
- Llamar al salto 3 "evento" en vez de "comando" es `competente` si el razonamiento de desacople es
  correcto; `excelente` si nota el único-responsable.
- En el salto 6 cualquiera de las dos defensas cuenta como `excelente` con su trade-off; la decisión
  concreta no determina el nivel, el razonamiento sí.
- Mencionar caché en el salto 4 sin convertirlo en "asíncrono" es señal de buena comprensión, no error.
