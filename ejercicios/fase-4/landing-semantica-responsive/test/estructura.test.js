// Tests del ESQUELETO de la landing. Se corren con:  node --test
//
// Qué verifican: que la ESTRUCTURA semántica y el CSS responsive estén presentes.
// Qué NO verifican: que la página se VEA bien (eso lo juzgas tú en el navegador y
// lo evalúa el corrector IA con la rúbrica). Pasar estos tests es necesario, no suficiente.
//
// Nota: se ignoran los comentarios de HTML (<!-- ... -->) y de CSS (/* ... */) antes
// de medir, para que un TODO en un comentario no cuente como solución.

const { test } = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");

const dir = path.join(__dirname, "..");
const rawHtml = fs.readFileSync(path.join(dir, "index.html"), "utf8");
const rawCss = fs.readFileSync(path.join(dir, "styles.css"), "utf8");

// Quita comentarios para no contar etiquetas/propiedades que solo aparecen en TODOs.
const html = rawHtml.replace(/<!--[\s\S]*?-->/g, "");
const css = rawCss.replace(/\/\*[\s\S]*?\*\//g, "");

// Cuenta etiquetas de apertura <tag ...> (no cierres </tag>).
function countOpenTags(s, tag) {
  const re = new RegExp(`<${tag}(?:\\s[^>]*)?>`, "gi");
  return (s.match(re) || []).length;
}

test("el <html> declara el idioma con lang", () => {
  assert.match(rawHtml, /<html[^>]*\blang\s*=/i, "Falta el atributo lang en <html>");
});

test("el <head> tiene charset y viewport", () => {
  assert.match(rawHtml, /<meta[^>]*charset/i, "Falta <meta charset>");
  assert.match(
    rawHtml,
    /<meta[^>]*name=["']viewport["'][^>]*width=device-width/i,
    "Falta <meta name=viewport ... width=device-width>",
  );
});

test("hay exactamente un <main>", () => {
  assert.equal(countOpenTags(html, "main"), 1, "Debe haber exactamente un <main>");
});

test("usa los landmarks header, nav y footer", () => {
  assert.ok(countOpenTags(html, "header") >= 1, "Falta <header>");
  assert.ok(countOpenTags(html, "nav") >= 1, "Falta <nav>");
  assert.ok(countOpenTags(html, "footer") >= 1, "Falta <footer>");
});

test("hay exactamente un <h1>", () => {
  assert.equal(countOpenTags(html, "h1"), 1, "Debe haber un solo <h1> por página");
});

test("hay al menos 3 tarjetas (<article>)", () => {
  assert.ok(countOpenTags(html, "article") >= 3, "Se esperan al menos 3 <article> como tarjetas");
});

test("toda <img> tiene atributo alt", () => {
  const imgs = html.match(/<img\b[^>]*>/gi) || [];
  assert.ok(imgs.length >= 1, "Se espera al menos una <img> (con su alt)");
  for (const img of imgs) {
    assert.match(img, /\salt\s*=/i, `Esta <img> no tiene alt: ${img}`);
  }
});

test("el CSS aplica box-sizing: border-box", () => {
  assert.match(css, /box-sizing\s*:\s*border-box/i, "Falta box-sizing: border-box");
});

test("el CSS es mobile-first (una @media con min-width)", () => {
  assert.match(css, /@media[^{]*min-width/i, "Falta una @media con min-width (mobile-first)");
});

test("usa Grid y Flexbox", () => {
  assert.match(css, /display\s*:\s*grid/i, "Falta display: grid (rejilla de tarjetas)");
  assert.match(css, /display\s*:\s*flex/i, "Falta display: flex (p. ej. la nav)");
});

test("usa unidades rem (no todo en px)", () => {
  assert.match(css, /\d*\.?\d+rem\b/i, "Usa rem para tipografía/espaciado, no solo px");
});
