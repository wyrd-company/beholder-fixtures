// Relative cross-root import via rootDirs virtual merge.
// This specifier "./models.js" is absent under the authored root
// (no packages/app/src/models.ts) and resolves through the
// corresponding path under the generated root (generated/models.ts)
// via rootDirs ["./src","../../generated"] / ["./packages/app/src","./generated"].

import { describeRootDirs } from "./rootdirs/shared.js";
import type { GeneratedModel } from "./models.js";
import { ROOT_MODELS_MARKER } from "./models.js";

export function readCrossRoot(): string {
  const authored = describeRootDirs();
  const marker: GeneratedModel = { id: "cross", revision: 1 };
  return `${authored}|${ROOT_MODELS_MARKER}:${marker.id}`;
}
