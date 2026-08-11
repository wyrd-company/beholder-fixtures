#!/usr/bin/env node
// Generator source — committed alongside generated outputs.
// Reads scripts/schema.json and emits generated/*.ts and generated/*.d.ts with distinct source/map identities.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const schemaPath = path.join(here, "schema.json");
const generatedDir = path.join(root, "generated");

const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

ensureDir(generatedDir);

// Generated .ts entering through `include`, import, and rootDirs.
// Header records provenance: authored generator vs generated output vs emitted JS.
const modelsTs = `// Generated from scripts/schema.json by scripts/generate.mjs — do not edit.
// Generator input version: ${schema.version}
// This file is authored: generator source is scripts/generate.mjs
// Generated identity: generated/models.ts
// Emitted identity: dist/**/generated/models.js with external source map

export const ROOT_MODELS_MARKER = "generated-models-v${schema.version}";

export type GeneratedModel = {
  id: string;
  revision: number;
};

export function formatModel(model: GeneratedModel): string {
  return \`\${model.id}:\${model.revision}:\${ROOT_MODELS_MARKER}\`;
}

// Changed generated types after input changes — altering schema.json revision produces:
//   revision: number -> revision: string | number
// and would update this file on re-generation.
`;

fs.writeFileSync(path.join(generatedDir, "models.ts"), modelsTs, "utf8");

const apiTypesDts = `// Generated declaration from scripts/schema.json — version ${schema.version}
// Source identity: generated/api-types.d.ts (generated declaration)
// Map identity: generated/api-types.d.ts.map (external declaration map)
// Authored generator: scripts/generate.mjs
// Consumer: src/generated-consumer.ts via import

export type GeneratedApi = {
  endpoint: string;
  timeout: number;
};
`;

fs.writeFileSync(
  path.join(generatedDir, "api-types.d.ts"),
  apiTypesDts,
  "utf8",
);

// Generated implementation — also shows source vs emitted distinction
const apiTs = `// Generated implementation — demonstrates generated .ts vs .d.ts provenance.
// Inline map would embed sources in emitted JS; external map keeps map file separate.

import type { GeneratedModel } from "./models.js";
import type { GeneratedApi } from "./api-types.js";

export function readGeneratedApi(model: GeneratedModel): string {
  return \`api:\${model.id}:\${model.revision}\`;
}

export type ReExportedGeneratedApi = GeneratedApi;
`;

fs.writeFileSync(path.join(generatedDir, "api.ts"), apiTs, "utf8");

console.log(
  "generate: wrote generated/models.ts, generated/api-types.d.ts, generated/api.ts",
);
