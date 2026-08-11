// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import type { TypeShapeB } from "./type-b.js";

export type TypeShapeA = {
  payload: TypeShapeB;
};
