#!/usr/bin/env node
// Compares inferred declarations emitted under the two vendored compilers.
// Reads dist and dist-5.4 declarations for the boundary predicate and prints
// the inspectable difference without mutating tracked source.

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const p54 = resolve(root, "dist-5.4/boundary/predicate.d.ts");
const p59 = resolve(root, "dist/boundary/predicate.d.ts");

function read(p) {
  if (!existsSync(p)) {
    return `missing: ${p} (run task build first)`;
  }
  return readFileSync(p, "utf8");
}

const a = read(p54);
const b = read(p59);

console.log("=== TypeScript 5.4.5 declaration (vendor/typescript-5.4.5) ===");
console.log(a);
console.log("=== TypeScript 5.9.3 declaration (node_modules/typescript) ===");
console.log(b);

if (a !== b) {
  console.log("=== boundary observable: declarations differ ===");
  const linesA = a.split("\n");
  const linesB = b.split("\n");
  for (const line of linesB) {
    if (!linesA.includes(line) && line.trim()) {
      console.log(`+ ${line}`);
    }
  }
  for (const line of linesA) {
    if (!linesB.includes(line) && line.trim()) {
      console.log(`- ${line}`);
    }
  }
} else {
  console.log("declarations are identical (unexpected)");
}
