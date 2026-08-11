// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import Dial = require("../types/dial");

export function spinDial(): number {
  return Dial.spin();
}
