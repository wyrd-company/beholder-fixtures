// Generated from scripts/schema.json by scripts/generate.mjs — do not edit.
// Generator input version: 1
// This file is authored: generator source is scripts/generate.mjs
// Generated identity: generated/models.ts
// Emitted identity: dist/**/generated/models.js with external source map

export const ROOT_MODELS_MARKER = "generated-models-v1";

export type GeneratedModel = {
  id: string;
  revision: number;
};

export function formatModel(model: GeneratedModel): string {
  return `${model.id}:${model.revision}:${ROOT_MODELS_MARKER}`;
}

// Changed generated types after input changes — altering schema.json revision produces:
//   revision: number -> revision: string | number
// and would update this file on re-generation.
