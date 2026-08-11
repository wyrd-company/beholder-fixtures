// Generated implementation — demonstrates generated .ts vs .d.ts provenance.
// Inline map would embed sources in emitted JS; external map keeps map file separate.

import type { GeneratedModel } from "./models.js";
import type { GeneratedApi } from "./api-types.js";

export function readGeneratedApi(model: GeneratedModel): string {
  return `api:${model.id}:${model.revision}`;
}

export type ReExportedGeneratedApi = GeneratedApi;
