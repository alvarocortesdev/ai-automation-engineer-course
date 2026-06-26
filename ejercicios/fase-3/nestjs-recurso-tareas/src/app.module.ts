// DADO — no necesitas modificar este archivo.
import { Module } from "@nestjs/common";
import { TareasModule } from "./tareas/tareas.module";

@Module({
  imports: [TareasModule],
})
export class AppModule {}
