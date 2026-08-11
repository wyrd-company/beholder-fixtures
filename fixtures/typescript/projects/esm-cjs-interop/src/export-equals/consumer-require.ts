// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import Chronometer = require("./chronometer.cjs.js");
import Beacon = require("./beacon-publisher.js");

export function readChronometerUnit(): string {
  return Chronometer.unit;
}

export function createChronometer(): Chronometer {
  return Chronometer.zero();
}

export function readBeaconPulse(): string {
  return Beacon.pulse();
}
