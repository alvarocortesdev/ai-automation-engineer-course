---
ejercicio_id: fase-2/patrones-adapter-notificaciones
fase: fase-2
sub_unidad: "2.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Integra dos terceros con Adapter (y prueba Open/Closed)

## Respuesta canónica

Dos clases Adapter que **componen** la librería de terceros (la reciben en `__init__`) y cumplen el contrato
`Notificador` por fuera, traduciendo la llamada por dentro. El dominio (`enviar_alerta`, el `Protocol`) no cambia.

```python
# notificaciones.py — adapters agregados al final, sin tocar nada más.

class SmsAdapter:                                  # cumple Notificador
    def __init__(self, gateway: GatewaySmsLegacy, remitente: str) -> None:
        self._gateway = gateway                    # composición, no herencia
        self._remitente = remitente

    def enviar(self, destino: str, mensaje: str) -> None:
        self._gateway.send_text(destino, mensaje, sender=self._remitente)


class EmailAdapter:                                # la extensión (Open/Closed)
    def __init__(self, cliente: ClienteEmailV2) -> None:
        self._cliente = cliente

    def enviar(self, destino: str, mensaje: str) -> None:
        self._cliente.dispatch(
            {"recipient": destino, "subject": "Alerta", "html": mensaje}
        )
```

Test del proveedor nuevo que el alumno agrega (sin tocar `SmsAdapter` ni `enviar_alerta`):

```python
def test_email_adapter_traduce_la_llamada():
    cliente = ClienteEmailV2()
    enviar_alerta(EmailAdapter(cliente), "ana@correo.cl")
    assert cliente.bandeja == [
        {"recipient": "ana@correo.cl", "subject": "Alerta", "html": "Tu pedido fue confirmado"}
    ]
```

Resultado: `pytest` → 3 passed (2 de SMS dados + 1 de email agregado).

## Razonamiento paso a paso

1. **El que se adapta es el extraño.** El contrato `Notificador.enviar(destino, mensaje)` es de tu dominio y no
   se toca. Cada librería de terceros habla otro idioma; el Adapter es el único punto que conoce ese idioma.
2. **Composición, no herencia.** El adapter **guarda** la librería (`self._gateway = gateway`) y delega. Heredar
   (`class SmsAdapter(GatewaySmsLegacy)`) acoplaría el adapter a la interfaz interna del tercero y haría imposible
   la traducción limpia de nombres/orden de argumentos.
3. **La traducción es solo mapeo.** `enviar(destino, mensaje)` → `send_text(destino, mensaje, sender=...)` para
   SMS; → `dispatch({"recipient", "subject", "html"})` para email. No se reimplementa el envío: se traduce la llamada.
4. **Open/Closed demostrado.** Agregar `EmailAdapter` es una clase nueva; `enviar_alerta` y `SmsAdapter` quedan
   intactos. Migrar de proveedor = inyectar otro adapter, sin editar el dominio.

## Variantes aceptables (NO penalizar)
- **`subject` distinto** ("Notificación", "Aviso", etc.): el enunciado no fija el asunto exacto; cualquier string
  razonable es `competente` mientras las claves del payload sean `recipient`/`subject`/`html`. (El test del alumno
  debe ser coherente con el asunto que eligió.)
- **Adapter con manejo de errores del tercero** (try/except alrededor de `send_text`, log, re-raise tipado): es
  **mejora legítima** (hilo seguridad/frontera) y cuenta como `excelente` si el alumno lo justifica; no es obligatorio.
- **Un `Protocol` explícito de "tercero"** o type hints más estrictos: válido, no requerido.
- **Función-adapter** en vez de clase para un caso trivial: aceptable si cumple la firma, aunque la clase es más
  clara cuando hay estado (`remitente`). Para SMS, que necesita `remitente`, la clase es la opción natural.

## Puntos resbalosos (donde el corrector debe mirar)
1. **¿Modificó el dominio?** Si tocó `enviar_alerta` o el `Protocol` `Notificador`, adaptó al revés → `incompleto` en C1.
2. **¿Heredó en vez de componer?** `class SmsAdapter(GatewaySmsLegacy)` es la señal #1 de no haber entendido el patrón.
3. **¿Perdió datos?** Olvidar `sender`, invertir `destino`/`mensaje`, o claves de payload mal (no recipient/subject/html).
4. **¿El negocio importa la librería?** Cualquier `import` o referencia directa a `GatewaySmsLegacy`/`ClienteEmailV2`
   desde código de dominio rompe el objetivo: el dominio solo conoce `Notificador`.
5. **¿Agregó email editando lo existente?** Si para integrar email tocó `SmsAdapter` o `enviar_alerta`, no demostró Open/Closed.
6. **(robustez) ¿Propaga la falla del tercero a ciegas?** No es obligatorio manejarla, pero el alumno debería al
   menos **reconocer** que la frontera es el lugar para hacerlo (hilo transversal).
