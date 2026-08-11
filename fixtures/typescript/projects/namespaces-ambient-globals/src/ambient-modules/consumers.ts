// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import exactHue, { hue } from "exact-palette";
import readTone from "equals-palette";
import { slotId } from "pattern-slot-alpha";
import shorthandValue from "shorthand-slot";
import { ledgerId } from "unmatched-ledger";

export function describeAmbientModules(): {
  exactDefault: number;
  exactNamed: number;
  equalsShape: string;
  wildcardSlot: string;
  shorthandAny: any;
  unmatchedLedger: string;
  flippedTone: string;
} {
  const exactDefault = exactHue();
  const exactNamed = hue;
  const equalsShape = readTone();
  const wildcardSlot = slotId;
  const shorthandAny = shorthandValue;
  const unmatchedLedger = ledgerId;
  const flippedTone = describeFlippedPalette().tone;

  return {
    exactDefault,
    exactNamed,
    equalsShape,
    wildcardSlot,
    shorthandAny,
    unmatchedLedger,
    flippedTone,
  };
}

function describeFlippedPalette(): import("./external-module-flip.js").FlippedToneCard {
  return { tone: "flipped", revision: 1 };
}
