---
ejercicio_id: fase-3/nestjs-recurso-tareas
fase: fase-3
sub_unidad: "3.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Recurso de tareas en NestJS

## Implementación canónica

### `src/tareas/tareas.service.ts`

```typescript
import { Injectable, NotFoundException } from "@nestjs/common";

export interface Tarea {
  id: number;
  titulo: string;
  completada: boolean;
}

@Injectable()
export class TareasService {
  private tareas: Tarea[] = [];
  private siguienteId = 1;

  crear(titulo: string): Tarea {
    const tarea: Tarea = { id: this.siguienteId++, titulo, completada: false };
    this.tareas.push(tarea);
    return tarea;
  }

  listar(): Tarea[] {
    return this.tareas;
  }

  obtener(id: number): Tarea {
    const tarea = this.tareas.find((t) => t.id === id);
    if (!tarea) {
      throw new NotFoundException(`Tarea ${id} no encontrada`);
    }
    return tarea;
  }
}
```

### `src/tareas/tareas.controller.ts`

```typescript
import { Body, Controller, Get, Param, Post } from "@nestjs/common";
import { TareasService, Tarea } from "./tareas.service";
import { CrearTareaDto } from "./dto/crear-tarea.dto";

@Controller("tareas")
export class TareasController {
  constructor(private readonly tareasService: TareasService) {}

  @Post()
  crear(@Body() dto: CrearTareaDto): Tarea {
    return this.tareasService.crear(dto.titulo);
  }

  @Get()
  listar(): Tarea[] {
    return this.tareasService.listar();
  }

  @Get(":id")
  obtener(@Param("id") id: string): Tarea {
    return this.tareasService.obtener(Number(id));
  }
}
```

### `src/tareas/dto/crear-tarea.dto.ts`

```typescript
import { IsNotEmpty, IsString } from "class-validator";

export class CrearTareaDto {
  @IsString()
  @IsNotEmpty()
  titulo: string;
}
```

Verificado contra `test/tareas.spec.ts`: **7 passed** (4 de DI/dominio + 3 de validación del DTO).

## Por qué cada decisión

- **`@Injectable()` en el service** — sin ese decorador, el contenedor DI no puede gestionarlo y `Test.createTestingModule(...).compile()` falla al armar el controller. Es lo que lo vuelve un *provider* inyectable.
- **Inyección por constructor (`private readonly tareasService`)** — el contenedor entrega una instancia ya construida; el controller no la crea. Esto comparte una sola instancia y permite sustituirla en tests (`overrideProvider`). Hacer `new TareasService()` rompe ambas cosas.
- **DTO como `class`, no `interface`** — `class-validator` lee los decoradores con `reflect-metadata` en **tiempo de ejecución**. Las interfaces se borran al compilar a JS, así que no existirían para leer; la validación se saltaría en silencio. Por eso los 3 tests del DTO fallan si el alumno lo deja como interface.
- **`Number(id)` en `obtener`** — `@Param("id")` siempre llega como string; sin el cast, `find((t) => t.id === id)` compara `number === string` y nunca coincide (todo daría 404). El test `obtiene una tarea existente` lo caza.
- **`NotFoundException` en el service** — es la opción idiomática y pragmática para un service chico. El test la verifica con `toThrow(NotFoundException)`.

## Variantes aceptables
- Service que usa un `Map<number, Tarea>` en vez de un array: válido.
- DTO con `@IsString()` solo (sin `@IsNotEmpty()`): **no** aceptable como competente — el test `rechaza un titulo vacío` falla, porque `""` es un string válido para `@IsString()`. Hace falta `@IsNotEmpty()`.
- `obtener(id: string)` en el service y comparar como string: aceptable si es coherente, pero menos limpio; el dominio idealmente trabaja con `number`.
- Métodos del controller marcados `async` y devolviendo `Promise<Tarea>`: aceptable (no hay I/O real aquí).

## No aceptable como competente
- ❌ `CrearTareaDto` como `interface`: los 3 tests del DTO fallan; traiciona O2.
- ❌ `new TareasService()` dentro del controller: anula la DI (O1).
- ❌ Lógica de negocio en el controller (crear/filtrar inline) en vez de delegar al service: rompe la separación de capas (O3).
- ❌ El service tocando `req`/`res` o lanzando `HttpException` por todo: acopla dominio a transporte.
- ❌ Quitar/olvidar `@Injectable()`: el módulo no compila la DI.

## Puntos resbalosos (donde el corrector debe mirar)
1. **El primer renglón del DTO.** Si dice `interface`, ese es el bug; los tests de validación lo delatan. Verifica que sea `class` con los dos decoradores.
2. **El cast `Number(id)`.** Fácil de olvidar; sin él, "obtener existente" falla aunque el resto esté bien.
3. **`BITACORA.md`** debe explicar: (a) class vs interface = metadata en runtime; (b) inyección = testeo + instancia compartida; (c) desacople total = excepción de dominio (`TareaNoEncontrada`) + **exception filter** que la traduce a 404, equivalente al exception handler de FastAPI. Si la bitácora no conecta con FastAPI o no menciona el `ValidationPipe`, está en "en-progreso".
