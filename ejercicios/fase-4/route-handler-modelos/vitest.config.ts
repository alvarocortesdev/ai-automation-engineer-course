import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node", // Request/Response/URL son globales en Node 18+
    globals: true,
  },
});
