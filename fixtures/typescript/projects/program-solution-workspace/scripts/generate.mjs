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
// Derive field types from schema.models so a schema type change
// (e.g. revision: number -> string) produces changed generated types.
const modelDef =
  schema.models.find((m) => m.name === "GeneratedModel") ?? schema.models[0];
const apiDef =
  schema.models.find((m) => m.name === "GeneratedApi") ?? schema.models[1];

function fieldsToTs(fields) {
  return Object.entries(fields)
    .map(([k, v]) => `  ${k}: ${v};`)
    .join("\n");
}

const modelFieldsTs = fieldsToTs(modelDef.fields);
const apiFieldsTs = apiDef ? fieldsToTs(apiDef.fields) : "";

const modelsTs = `// Generated from scripts/schema.json by scripts/generate.mjs — do not edit.
// Generator input version: ${schema.version}
// Models: ${schema.models.map((m) => m.name).join(", ")}
// This file is authored: generator source is scripts/generate.mjs
// Generated identity: generated/models.ts
// Emitted identity: dist/**/generated/models.js with external source map

export const ROOT_MODELS_MARKER = "generated-models-v${schema.version}";

export type ${modelDef.name} = {
${modelFieldsTs}
};

export function formatModel(model: ${modelDef.name}): string {
  return \`\${model.id}:\${model.revision}:\${ROOT_MODELS_MARKER}\`;
}

// Changed generated types after input changes — altering schema.json fields
// (e.g. ${modelDef.name}.revision: ${modelDef.fields.revision} -> string) would
// update this file on re-generation.
`;

fs.writeFileSync(path.join(generatedDir, "models.ts"), modelsTs, "utf8");

const apiTypesDts = `// Generated declaration from scripts/schema.json — version ${schema.version}
// Source identity: generated/api-types.d.ts (generated declaration)
// Map identity: generated/api-types.d.ts.map (external declaration map)
// Authored generator: scripts/generate.mjs
// Consumer: src/generated-consumer.ts via import
// Derived from schema.models: ${apiDef ? apiDef.name : "GeneratedApi"}

export type ${apiDef ? apiDef.name : "GeneratedApi"} = {
${apiFieldsTs}
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
