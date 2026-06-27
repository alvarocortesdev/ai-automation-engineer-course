import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node", // reducer puro: no necesita DOM
    globals: true,
  },
});
