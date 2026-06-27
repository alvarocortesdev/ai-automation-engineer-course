# Diseño — Estados y seguridad de una UI de chat de IA

> Completa los huecos. **No escribes código de implementación**: es un documento de
> diseño, como el que llevarías a una revisión de UX/seguridad. Borra estas guías al
> entregar.

## 1. Inventario de estados de primera clase

> Lista los SEIS estados de una UI de chat de IA. Para cada uno: qué ve el usuario y
> qué transición lo activa.

| Estado | Qué ve el usuario | Qué transición lo activa |
|---|---|---|
| vacío | … | … |
| enviando | … | … |
| streaming | … | … |
| completado | … | … |
| error | … | … |
| cancelado | … | … |

## 2. Diagnóstico del componente `ChatIA` (respuesta-buggy.md)

> Un defecto por viñeta. Nombra el problema y el patrón de la lección que lo arregla.

- Defecto 1: …  → arreglo: …
- Defecto 2: …  → arreglo: …
- Defecto 3: …  → arreglo: …
- Defecto 4: …  → arreglo: …
- (agrega los que encuentres)

## 3. Seguridad

> ¿Por qué renderizar la salida del LLM como HTML es un riesgo? ¿Cuál es la regla
> correcta? Una línea conectándolo con OWASP de la Fase 3.

- Riesgo: …
- Regla correcta: …
- Conexión con OWASP: …

## 4. Accesibilidad

> Dos medidas concretas para el texto que llega en vivo (token por token).

- Medida 1: …
- Medida 2: …

## 5. Trade-off

> ¿Por qué streaming + optimistic UI en vez de esperar la respuesta completa? ¿Cuál es
> el costo y cuál el beneficio?

- Beneficio: …
- Costo: …
- Tu decisión y por qué: …
