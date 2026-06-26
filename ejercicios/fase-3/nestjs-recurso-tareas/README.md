# Ejercicio 3.10 — Recurso de tareas en NestJS

> **Modalidad: código (Node + TypeScript + NestJS, sin IA).** Montas el patrón completo de un backend NestJS —módulo, controller, service con inyección de dependencias y DTO validado— sobre un recurso de tareas en memoria. Es el "hola mundo robusto" de NestJS y el espejo en Node de lo que hiciste con FastAPI.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.10` Backend con Node.js + NestJS
**Ruta:** opcional / profundización · **Timebox:** 40–45 min

## 🎯 Objetivo

Completar tres archivos (`tareas.service.ts`, `tareas.controller.ts`, `crear-tarea.dto.ts`) para que `npm test` quede en verde, demostrando que sabes:

1. Escribir un **service** `@Injectable()` con lógica de negocio que **no habla HTTP** (salvo `NotFoundException`).
2. Escribir un **controller** que **inyecta** el service por constructor (sin `new`) y mapea `POST`/`GET`/`GET /:id`.
3. Escribir un **DTO** como **clase** con `class-validator` (no como interface).

## 📋 Contexto

Cada recurso de un backend NestJS se ve igual: un módulo que agrupa, un controller que habla HTTP, un service con la lógica, un DTO que valida la entrada. Si interiorizas este patrón con un recurso de juguete, lo replicas en cualquier API real —y, de paso, ves con tus manos por qué un DTO debe ser una clase y qué apaga la validación si lo quitas—. Es la base sobre la que se montan auth (`3.12`) y la capa de datos (`3.6` Prisma) en la ruta Node.

## ⚙️ Requisitos

Necesitas Node 20+ instalado. Luego, dentro de la carpeta del ejercicio:

```bash
npm install      # instala NestJS, class-validator, jest, ts-jest
npm test         # corre la suite (al principio falla: es lo esperado)
```

> El `npm install` lo corres **tú** en tu máquina; el starter no trae `node_modules`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Corre el test y mira fallar cada pieza por separado.
2. Solo entonces, consulta la **documentación oficial** (NestJS: *Providers*, *Controllers*, *Validation*).
3. **Solo al final**, usa IA para *revisar* tu solución — no para generarla.
4. Mañana, reescribe de memoria el service `@Injectable` y la inyección por constructor del controller.

## 🛠️ Instrucciones

1. **`src/tareas/tareas.service.ts`** — declara el estado en memoria (array de `Tarea` + contador de id). Implementa `crear` (id incremental, `completada=false`), `listar` y `obtener` (lanza `NotFoundException` si el id no existe). No importes nada de HTTP salvo `Injectable`/`NotFoundException`.
2. **`src/tareas/tareas.controller.ts`** — inyecta `TareasService` por **constructor** (`constructor(private readonly tareasService: TareasService) {}`). Implementa los tres métodos delegando en el service. Recuerda: `@Param("id")` llega como **string** → `Number(id)`.
3. **`src/tareas/dto/crear-tarea.dto.ts`** — conviértelo en una `class` con `@IsString()` + `@IsNotEmpty()` sobre `titulo`.
4. Corre el test hasta el verde:

   ```bash
   npm test
   ```

5. Escribe **`BITACORA.md`** respondiendo: (a) ¿por qué el DTO es una clase y no una interface? (b) ¿por qué inyectas el service en vez de hacer `new TareasService()` dentro del controller? (c) ¿qué cambiarías para que el dominio (el service) no conociera HTTP en absoluto, y con qué pieza de FastAPI se corresponde esa traducción?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `npm test` en **verde** (7 tests: 4 de DI/dominio + 3 de validación del DTO).
- [ ] `CrearTareaDto` es una **`class`** con los decoradores correctos (no una interface).
- [ ] El controller **inyecta** el service por constructor; no aparece `new TareasService()`.
- [ ] El service no toca `req`/`res`; toda la conversación HTTP vive en el controller.
- [ ] `BITACORA.md` responde las tres preguntas.
- [ ] Puedes explicar **sin notas** por qué una interface como DTO falla en silencio y qué pieza apaga la validación si la quitas (el `ValidationPipe` de `main.ts`).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Service:** `private tareas: Tarea[] = [];` y `private siguienteId = 1;`. En `crear`: `const tarea = { id: this.siguienteId++, titulo, completada: false };`. En `obtener`: `const t = this.tareas.find((x) => x.id === id); if (!t) throw new NotFoundException(...); return t;`.
- **Controller:** la inyección es literalmente el parámetro del constructor: `constructor(private readonly tareasService: TareasService) {}`. Cada método: `return this.tareasService.<algo>(...)`. En `obtener`, `Number(id)` antes de delegar.
- **DTO:** `import { IsNotEmpty, IsString } from "class-validator";` y encima de `titulo`: `@IsString() @IsNotEmpty()`.

Si los tests de DI fallan, revisa que el service esté `@Injectable()` y registrado en `providers` (ya viene en `tareas.module.ts`). Si los tests del DTO fallan, casi seguro dejaste el DTO como `interface`. Repasa las secciones 4.3–4.6 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio) + `BITACORA.md`,
- la **rúbrica**: `.ai/rubricas/fase-3/nestjs-recurso-tareas.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/nestjs-recurso-tareas.md` — no la mires antes de intentarlo de verdad.
