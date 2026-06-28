# Escenario — Soporte con IA que consulta un ERP legacy

Tu empresa construye un **sistema de soporte con IA** (el mismo del agente de tickets de
Fase 7). Flujo:

1. Entra un **ticket** de un cliente (correo / formulario).
2. Un **LLM clasifica** el ticket: `facturacion` | `tecnico` | `comercial`.
3. Para los de `facturacion`, el sistema consulta un **ERP externo legacy** (de un proveedor,
   **no lo controlas**) para traer el **estado de pago** del cliente y decidir la respuesta.
4. El agente redacta una respuesta y, según el estado de pago, decide si escala a un humano.

## El ERP externo (lo que NO controlas)

El ERP expone `GET /customers/{id}` y devuelve este JSON crudo. Sus nombres son crípticos,
los estados son enteros mágicos sin documentar bien, hay nulls, y las fechas son strings:

```json
{
  "cli": "C-00481",
  "nm": "  alvaro  cortes ",
  "pay_st": 3,
  "bal": "15990.00",
  "last_pay": "2026-05-30",
  "ovd": null
}
```

Diccionario que te pasó (a regañadientes) el proveedor:

| Campo      | Significado real                                  |
|------------|---------------------------------------------------|
| `cli`      | id del cliente                                    |
| `nm`       | nombre (viene con espacios y casing inconsistente)|
| `pay_st`   | estado de pago: `1`=al día, `2`=pendiente, `3`=moroso, `9`=en revisión |
| `bal`      | saldo adeudado, como **string** con decimales (pesos) |
| `last_pay` | fecha del último pago, string `YYYY-MM-DD` (o `null` si nunca pagó) |
| `ovd`      | días de mora; `null` si no aplica                 |

> Ojo: el proveedor ya cambió `pay_st` una vez el año pasado (antes `0`=al día). Y a veces
> el endpoint devuelve un `pay_st` que **no** está en la tabla (han aparecido `4` y `7`
> sin aviso). No puedes confiar en que el payload venga limpio.

## Tu dominio (lo que SÍ controlas)

En tu sistema de **Soporte**, lo que necesitas para decidir es algo limpio y con significado,
por ejemplo un `EstadoPagoCliente` con un enum legible (`AL_DIA`/`PENDIENTE`/`MOROSO`/`EN_REVISION`),
un saldo como **`Dinero`** (centavos, no string), y los días de mora como entero (o ausente).
Tú decides la forma exacta —eso es parte del ejercicio.
