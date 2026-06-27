# Tests del capstone (guía, no solución)

`aceptacion.plantilla.test.tsx` es un **molde** con los patrones que tu frontend debe cumplir, no una solución.
Cada test está marcado con `it.skip` y trae TODOs para que lo adaptes a TUS componentes. Quita el `skip` cuando
lo cablees a tu app.

## Qué se prueba (y por qué)

- **Los cuatro estados de una vista con datos** (empty/loading/error/success): que cada cara se renderice. Es el
  gate de [4.10](../../../src/content/docs/fase-4-frontend/4-10-usabilidad-estados.mdx).
- **Seguridad — salida del LLM como texto:** que un texto con `<script>` aparezca **escapado** (como texto), no
  como nodo HTML ejecutable. Es el gate anti-XSS de [4.11](../../../src/content/docs/fase-4-frontend/4-11-ui-apps-ia.mdx).
- **Accesibilidad con axe:** un chequeo automatizado con `jest-axe`. **Ojo:** axe cubre solo una parte; el foco de
  teclado, el orden de lectura y el manejo del foco en el modal exigen una **pasada manual** que no se automatiza.
- **La máquina de estados del chat:** reusa el reducer del ejercicio `chat-reducer-streaming` y pruébalo aquí
  (optimistic UI, acumulación de chunks, error sin borrar el parcial). Es TypeScript puro, no necesita React.

## Cómo correr

```bash
pnpm install
pnpm test
```

Configura Vitest con entorno `jsdom` y `@testing-library/jest-dom` (y `jest-axe`) en tu setup. Mídete por lo que
los tests **detectan**, no por el % de cobertura.
