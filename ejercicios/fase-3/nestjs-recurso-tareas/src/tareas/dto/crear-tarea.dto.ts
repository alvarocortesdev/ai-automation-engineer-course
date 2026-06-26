// COMPLETA ESTE ARCHIVO.
// OJO: un DTO debe ser una `class` (no una `interface`), porque class-validator necesita
// leer sus decoradores en TIEMPO DE EJECUCIÓN, y las interfaces se borran al compilar.
//
// TODO: añade los decoradores de class-validator para que `titulo` sea un string NO vacío.
//       (pista: import { IsNotEmpty, IsString } from "class-validator";)
export class CrearTareaDto {
  titulo: string;
}
