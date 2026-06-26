// DADO — no modifiques este archivo. Es la suite que tu implementación debe poner en verde.
//
// Dos bloques:
//  1) DI + dominio: el contenedor de NestJS arma el controller con su service y se prueba
//     el comportamiento llamando a los métodos del controller directamente (sin servidor HTTP).
//  2) Contrato del DTO: se valida CrearTareaDto con class-validator directamente.
import { Test, TestingModule } from "@nestjs/testing";
import { NotFoundException } from "@nestjs/common";
import { validate } from "class-validator";
import { plainToInstance } from "class-transformer";

import { TareasController } from "../src/tareas/tareas.controller";
import { TareasService } from "../src/tareas/tareas.service";
import { CrearTareaDto } from "../src/tareas/dto/crear-tarea.dto";

describe("Tareas — inyección de dependencias y dominio", () => {
  let controller: TareasController;

  beforeEach(async () => {
    // Si esto arma el controller, es porque el service quedó inyectable y registrado.
    const moduleRef: TestingModule = await Test.createTestingModule({
      controllers: [TareasController],
      providers: [TareasService],
    }).compile();
    controller = moduleRef.get<TareasController>(TareasController);
  });

  it("crea una tarea y le asigna id 1 y completada=false", () => {
    const creada = controller.crear({ titulo: "comprar pan" } as CrearTareaDto);
    expect(creada.id).toBe(1);
    expect(creada.titulo).toBe("comprar pan");
    expect(creada.completada).toBe(false);
  });

  it("lista todas las tareas creadas", () => {
    controller.crear({ titulo: "a" } as CrearTareaDto);
    controller.crear({ titulo: "b" } as CrearTareaDto);
    expect(controller.listar()).toHaveLength(2);
  });

  it("obtiene una tarea existente por id", () => {
    const creada = controller.crear({ titulo: "x" } as CrearTareaDto);
    expect(controller.obtener(String(creada.id)).titulo).toBe("x");
  });

  it("lanza NotFoundException al obtener un id inexistente", () => {
    expect(() => controller.obtener("999")).toThrow(NotFoundException);
  });
});

describe("CrearTareaDto — contrato de entrada (class-validator)", () => {
  it("rechaza un titulo vacío", async () => {
    const dto = plainToInstance(CrearTareaDto, { titulo: "" });
    const errores = await validate(dto);
    expect(errores.length).toBeGreaterThan(0);
  });

  it("rechaza un titulo ausente", async () => {
    const dto = plainToInstance(CrearTareaDto, {});
    const errores = await validate(dto);
    expect(errores.length).toBeGreaterThan(0);
  });

  it("acepta un titulo válido", async () => {
    const dto = plainToInstance(CrearTareaDto, { titulo: "tarea real" });
    const errores = await validate(dto);
    expect(errores).toHaveLength(0);
  });
});
