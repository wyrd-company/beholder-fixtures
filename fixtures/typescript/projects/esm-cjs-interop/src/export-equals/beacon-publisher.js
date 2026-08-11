// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

"use strict";

function Beacon() {
  this.signal = "steady";
}

Beacon.pulse = function pulse() {
  return "pulse";
};

module.exports = Beacon;
