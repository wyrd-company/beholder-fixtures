// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import type { TypeShapeA } from "./type-a.js";

export type TypeShapeB = {
  payload: TypeShapeA;
};
