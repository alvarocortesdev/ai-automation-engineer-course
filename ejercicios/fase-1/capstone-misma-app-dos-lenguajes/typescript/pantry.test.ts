/**
 * Tests del dominio de la despensa (TypeScript / vitest).
 *
 * Vienen escritos y FALLAN (rojo) hasta que implementes `pantry.ts`.
 * Mismo ciclo red-green que la versión Python: el test te dice qué construir.
 *
 * Corre:  npm test
 *
 * Antes de cerrar el capstone, AGREGA al menos un test tuyo.
 */

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { beforeEach, describe, expect, it } from "vitest";
import { ZodError } from "zod";
import { PantryStore } from "./pantry";

describe("PantryStore", () => {
  let store: PantryStore;

  beforeEach(() => {
    const dir = mkdtempSync(join(tmpdir(), "despensa-"));
    store = new PantryStore(join(dir, "data.json"));
  });

  it("empieza vacía", () => {
    expect(store.list()).toEqual([]);
  });

  it("agrega con id incremental", () => {
    const a = store.add({ name: "arroz", quantity: 2, unit: "kg" });
    const b = store.add({ name: "leche", quantity: 1, unit: "L" });
    expect(a.id).toBe(1);
    expect(b.id).toBe(2);
    expect(store.list()).toHaveLength(2);
  });

  it("rechaza cantidad no positiva", () => {
    expect(() => store.add({ name: "sal", quantity: 0, unit: "kg" })).toThrow(ZodError);
  });

  it("rechaza nombre vacío", () => {
    expect(() => store.add({ name: "", quantity: 1, unit: "kg" })).toThrow(ZodError);
  });

  it("un dato inválido no se persiste", () => {
    expect(() => store.add({ name: "sal", quantity: -1, unit: "kg" })).toThrow(ZodError);
    expect(store.list()).toEqual([]);
  });

  it("get devuelve undefined si no existe", () => {
    expect(store.get(99)).toBeUndefined();
  });

  it("remove devuelve false si no existe y true si existe", () => {
    store.add({ name: "pan", quantity: 4, unit: "u" });
    expect(store.remove(99)).toBe(false);
    expect(store.remove(1)).toBe(true);
    expect(store.list()).toEqual([]);
  });

  it("persiste entre instancias (mismo archivo)", () => {
    const dir = mkdtempSync(join(tmpdir(), "despensa-"));
    const path = join(dir, "data.json");
    const a = new PantryStore(path);
    a.add({ name: "café", quantity: 1, unit: "kg" });
    const b = new PantryStore(path);
    expect(b.list()).toHaveLength(1);
  });

  // TODO: agrega aquí al menos un test tuyo.
});
