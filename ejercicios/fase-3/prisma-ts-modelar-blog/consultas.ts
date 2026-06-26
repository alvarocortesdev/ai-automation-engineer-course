// consultas.ts — STARTER del ejercicio (Primero-Sin-IA).
//
// Completa las cuatro funciones a mano, sin IA. NO cambies las firmas.
// El objetivo es que las queries sean type-safe (campos que existen en tu
// schema) y que las lecturas de relaciones NO caigan en N+1
// (usa include/select, nunca una query dentro de un loop).
//
// Nota: este archivo no se "ejecuta" como test del ejercicio (necesitaría una
// base corriendo y el cliente generado). El corrector evalúa que las queries
// sean correctas y type-safe leyéndolas; si tienes Postgres + `prisma generate`
// puedes ejecutarlas tú para verificar.

import { PrismaClient } from "./generated/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

// 1) Crea un usuario y, en LA MISMA operación, su primer post (nested write).
//    Debe devolver el usuario creado.
export async function crearUsuarioConPost(email: string, titulo: string) {
  // TODO(estudiante): usa prisma.user.create({ data: { ..., posts: { create: [...] } } })
  throw new Error("Implementa esta función a mano, sin IA.");
}

// 2) Lista TODOS los usuarios con sus posts, sin caer en N+1 (una sola operación).
export async function usuariosConPosts() {
  // TODO(estudiante): prisma.user.findMany({ include: { ... } })
  throw new Error("Implementa esta función a mano, sin IA.");
}

// 3) Trae los 10 posts publicados más recientes, cada uno con el NOMBRE de su autor.
//    Usa select para traer solo lo necesario.
export async function postsPublicadosRecientes() {
  // TODO(estudiante): prisma.post.findMany({ where, select, orderBy, take })
  throw new Error("Implementa esta función a mano, sin IA.");
}

// 4) Cuenta cuántos posts publicados hay.
export async function contarPublicados(): Promise<number> {
  // TODO(estudiante): prisma.post.count({ where: { ... } })
  throw new Error("Implementa esta función a mano, sin IA.");
}
