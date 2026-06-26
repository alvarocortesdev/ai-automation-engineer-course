// COMPLETA ESTE ARCHIVO.
// El controller es la ÚNICA pieza que habla HTTP. Inyecta el service por constructor
// (no hagas `new TareasService()`) y delega toda la lógica en él.
import { Body, Controller, Get, Param, Post } from "@nestjs/common";
import { TareasService, Tarea } from "./tareas.service";
import { CrearTareaDto } from "./dto/crear-tarea.dto";

@Controller("tareas")
export class TareasController {
  // TODO: inyecta TareasService por el constructor (constructor injection).

  @Post()
  crear(@Body() dto: CrearTareaDto): Tarea {
    // TODO: delega en el service usando dto.titulo.
    throw new Error("TODO: implementar crear");
  }

  @Get()
  listar(): Tarea[] {
    // TODO: delega en el service.
    throw new Error("TODO: implementar listar");
  }

  @Get(":id")
  obtener(@Param("id") id: string): Tarea {
    // TODO: @Param siempre llega como string -> conviértelo con Number(id) antes de delegar.
    throw new Error("TODO: implementar obtener");
  }
}
