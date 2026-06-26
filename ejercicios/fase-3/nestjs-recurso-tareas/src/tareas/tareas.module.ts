// DADO — no necesitas modificar este archivo.
// Declara qué controller y qué provider viven juntos; el contenedor DI lo lee para inyectar.
import { Module } from "@nestjs/common";
import { TareasController } from "./tareas.controller";
import { TareasService } from "./tareas.service";

@Module({
  controllers: [TareasController],
  providers: [TareasService],
})
export class TareasModule {}
