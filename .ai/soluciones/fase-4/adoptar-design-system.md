---
ejercicio_id: fase-4/adoptar-design-system
fase: fase-4
sub_unidad: "4.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — ¿Tailwind directo, shadcn/ui o design system?

## Decisiones canónicas

| # | Escenario | Estrategia | Justificación (trade-off) |
|---|---|---|---|
| 1 | Portafolio (~4 páginas, solo) | **Tailwind directo** | Pocas pantallas, un solo dev, repetición baja. Extraer a componente solo lo que se repita 3+ veces. Costo que acepto: la consistencia depende de mi disciplina, pero a esta escala es trivial mantenerla. Montar un DS aquí sería sobre-engineering. |
| 2 | Capstone ChatLab (~6 pantallas, modales/menús/select accesibles) | **shadcn/ui + tokens** | El factor decisivo no es el tamaño, son los **componentes interactivos accesibles** (modal, dropdown, select, tooltip): Radix los resuelve por mí y los poseo. Tokens en CSS variables me dan el tema claro/oscuro. Costo: aprender el flujo de shadcn y mantener el código copiado. Vale la pena: me ahorra reimplementar accesibilidad. |
| 3 | MVP startup 3 personas (2 devs, crecerá) | **shadcn/ui + tokens** (ambiguo; ver abajo) | Dos devs tocando los mismos componentes → la consistencia ya no es solo disciplina personal. shadcn + tokens compartidos da una base común sin el costo de publicar un paquete. Costo: acordar convenciones de uso. Un DS publicado todavía es prematuro para 3 personas y un producto. |
| 4 | Empresa 4 equipos / 3 productos, misma marca | **Design system publicado** | Varios equipos y productos comparten marca y deben evolucionarla coordinadamente → tokens versionados (Style Dictionary), paquete compartido y documentación (Storybook) son justificables. Costo alto (un equipo lo mantiene), pero el costo de la inconsistencia entre 3 productos lo supera. |

## Respuestas trampa

**T1 — "shadcn es una dependencia más".** Se equivoca en el modelo: shadcn/ui sigue el modelo **"open code"**. El CLI (`npx shadcn@latest add ...`) **copia el código del componente dentro de tu repo**; no vive escondido en `node_modules` como una librería tradicional. Consecuencias prácticas: (1) **lo posees y lo editas** —agregas una variante sin esperar al mantenedor ni pelear con `!important`—; (2) **no se actualiza solo** —lo que copiaste no cambia bajo tus pies; las mejoras del upstream no llegan automáticas, y eso es a la vez el costo y el control—. Tratarlo como dependencia tradicional lleva a no entender ni su ventaja (control total) ni su costo (mantenimiento propio).

**T2 — Modal/menú "a mano con div y onClick".** Mala idea. Un diálogo o un menú **accesibles** exigen mucho más que mostrar/ocultar: **foco atrapado** dentro del modal mientras está abierto y devuelto al disparador al cerrar, cierre con **`Esc`**, navegación con **teclado** (flechas en el menú, `Tab` que no se escapa), roles y atributos **ARIA** correctos (`role="dialog"`, `aria-modal`, `aria-expanded`, etc.) y anuncios a lectores de pantalla. Reimplementar todo eso a mano es brutalmente difícil y casi siempre se hace mal, rompiendo justo los criterios de **WCAG 2.2** (operable por teclado, foco visible y gestionado) que viste en [4.4](/fase-4-frontend/4-4-accesibilidad-wcag/). Radix (sobre lo que se construye shadcn) ya lo resuelve. Usar Radix no es pereza: es no reinventar (mal) algo resuelto.

## Escenario ambiguo (trade-off esperado)
El **escenario 3 (MVP, 3 personas)** es el caso ambiguo legítimo. Respuesta competente: empezar con **shadcn/ui + tokens** (base común suficiente para dos devs, sin el costo de publicar un paquete) y **subir a un DS publicado solo cuando** aparezca el segundo o tercer producto o más equipos. Reconocer que no hay una única respuesta correcta —y justificar la elegida por el costo presente, no por el futuro hipotético— es lo que distingue una respuesta excelente. También es válido elegir Tailwind directo + algunos componentes propios si los interactivos accesibles son pocos; lo importante es nombrar el riesgo de divergencia entre dos devs.

## Qué premiar y qué penalizar
- **Premiar:** que la justificación apele al **trade-off** (costo de montar vs costo de inconsistencia), que el portafolio (1) sea Tailwind directo, la empresa (4) sea DS publicado, y que T1 nombre "open code / código que posees" y T2 ataque desde accesibilidad (foco/teclado/ARIA + WCAG).
- **Penalizar (marcar como antipatrón):** montar un DS publicado para el portafolio (sobre-engineering); construir modales/menús accesibles a mano (escenario 2/T2); decir que shadcn "se actualiza solo como una dependencia".
- **No penalizar:** elegir Tailwind directo en el escenario 3 **si** justifica el bajo número de interactivos y nombra el riesgo de divergencia; usar shadcn en el 4 **si** además reconoce que los tokens deben publicarse/versionarse para compartirse entre productos.

## Variantes aceptables
- Escenario 2 con "Tailwind directo + traer solo el Dialog y el DropdownMenu de shadcn": válido; sigue siendo "usar Radix para lo difícil".
- Escenario 4 que mencione Storybook, design tokens en formato W3C/Style Dictionary, o un monorepo con paquete `@marca/ui`: todas señales de comprensión, no obligatorias.
- Llamar a las estrategias en inglés ("utility-first", "design system as a package"): válido (terminología técnica en inglés).
