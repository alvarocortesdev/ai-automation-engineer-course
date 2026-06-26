import { defineConfig, devices } from "@playwright/test";

// Config mínima del ejercicio. La app es un archivo estático (app.html), así que
// NO necesitamos un webServer: cada test navega con una file:// URL (ver gastos.spec.ts).
// En una app real con servidor usarías baseURL + webServer (ver la lección, sección 4.6).
export default defineConfig({
  testDir: ".",
  testMatch: "*.spec.ts",
  forbidOnly: !!process.env.CI,
  retries: 0, // a propósito 0: el ejercicio exige que el test sea determinista sin reintentos
  reporter: "list",
  use: {
    trace: "on-first-retry", // observabilidad: graba la traza si un test reintenta
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
