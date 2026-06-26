// COMPLETA ESTE ARCHIVO.
// El service tiene la lógica de negocio y NO sabe de HTTP (salvo NotFoundException, que es
// idiomático en Nest). Estado en memoria: un array de Tarea + un contador de id.
import { Injectable, NotFoundException } from "@nestjs/common";

export interface Tarea {
  id: number;
  titulo: string;
  completada: boolean;
}

@Injectable()
export class TareasService {
  // TODO: declara el estado en memoria (un array privado de Tarea y un contador de id).

  crear(titulo: string): Tarea {
    // TODO: crea una Tarea con id incremental y completada=false, guárdala y devuélvela.
    throw new Error("TODO: implementar crear");
  }

  listar(): Tarea[] {
    // TODO: devuelve todas las tareas.
    throw new Error("TODO: implementar listar");
  }

  obtener(id: number): Tarea {
    // TODO: busca por id; si no existe, lanza NotFoundException(`Tarea ${id} no encontrada`).
    throw new Error("TODO: implementar obtener");
  }
}
