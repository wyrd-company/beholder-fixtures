// Generated source entering through import and include — imports committed generated file.
import type { GeneratedModel } from "../generated/models.js";
import { ROOT_MODELS_MARKER, formatModel } from "../generated/models.js";
import type { GeneratedApi } from "../generated/api-types.js";

export function consumeGenerated(model: GeneratedModel): string {
  return `${ROOT_MODELS_MARKER}:${formatModel(model)}`;
}

export type ReExportedGeneratedApi = GeneratedApi;
