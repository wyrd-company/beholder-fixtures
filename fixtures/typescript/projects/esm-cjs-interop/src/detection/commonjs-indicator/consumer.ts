// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import { esmMarker } from "../package-type-esm/marker.js";
import publisher = require("./publisher.js");

export function readMarkers(): string {
  return `${esmMarker}:${publisher.cjsMarker}`;
}
