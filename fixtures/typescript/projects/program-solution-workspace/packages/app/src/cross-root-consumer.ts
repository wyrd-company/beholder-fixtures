// Relative cross-root import via rootDirs virtual merge.
// Authored file imports generated file as if sibling in merged root.

import { describeRootDirs } from "./rootdirs/shared.js";
import type { GeneratedModel } from "../../../generated/models.js";
import { ROOT_MODELS_MARKER } from "../../../generated/models.js";

export function readCrossRoot(): string {
  const authored = describeRootDirs();
  const marker: GeneratedModel = { id: "cross", revision: 1 };
  return `${authored}|${ROOT_MODELS_MARKER}:${marker.id}`;
}
