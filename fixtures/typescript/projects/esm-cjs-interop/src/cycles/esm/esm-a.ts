// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

export let mutableCount = 0;

import { readMutableFromB } from "./esm-b.js";

mutableCount = readMutableFromB();
