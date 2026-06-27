/**
 * Catálogo fijo de modelos. NO lo edites: los tests dependen de estos datos.
 * En un proyecto Next.js real esto vendría de una base de datos; aquí es un
 * arreglo en memoria para que el ejercicio corra sin infraestructura.
 */

export interface Modelo {
  id: string;
  nombre: string;
  proveedor: string;
}

export const MODELOS: Modelo[] = [
  { id: "1", nombre: "Claude Opus 4.8", proveedor: "Anthropic" },
  { id: "2", nombre: "Claude Sonnet 4.8", proveedor: "Anthropic" },
  { id: "3", nombre: "Claude Haiku 4.8", proveedor: "Anthropic" },
  { id: "4", nombre: "GPT-5.1", proveedor: "OpenAI" },
  { id: "5", nombre: "GPT-5.1 mini", proveedor: "OpenAI" },
  { id: "6", nombre: "o4", proveedor: "OpenAI" },
  { id: "7", nombre: "Gemini 3 Pro", proveedor: "Google" },
  { id: "8", nombre: "Gemini 3 Flash", proveedor: "Google" },
  { id: "9", nombre: "Llama 4 Scout", proveedor: "Meta" },
  { id: "10", nombre: "Llama 4 Maverick", proveedor: "Meta" },
  { id: "11", nombre: "Mistral Large 3", proveedor: "Mistral" },
  { id: "12", nombre: "Qwen3 Coder", proveedor: "Alibaba" },
];
