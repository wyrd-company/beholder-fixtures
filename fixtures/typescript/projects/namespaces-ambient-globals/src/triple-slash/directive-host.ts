/// <reference path="./lib-stub.d.ts" preserve="true" />
/// <reference types="fixture-reference-types" />
/// <reference path="./types/@fixture/lib-stub/index.d.ts" preserve="true" />
/// <reference path="../../pregen/triple-slash/generated-marker.d.ts" />

// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readStubToken } from "@fixture/lib-stub";

export function describeTripleSlashHost(): {
  clock: number;
  stub: string;
  generated: string;
  referenceToken: string;
} {
  const clock = LibStubClock.tick();
  const stub = readStubToken().label;
  const generated: import("../../pregen/triple-slash/generated-marker.js").FixtureMarker =
    {
      marker: "generated-ref",
    };
  const referenceToken = readFixtureReferenceToken().token;

  return { clock, stub, generated: generated.marker, referenceToken };
}
