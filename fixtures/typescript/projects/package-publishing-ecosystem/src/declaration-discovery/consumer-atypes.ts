// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { GenericAmbientMarker } from "generic-ambient";
import { readGenericAmbient } from "generic-ambient";
import { readScoped } from "@scope/name";
import type { ScopedMarker } from "@scope/name";

export function describeAtypes(value: string): string {
  const a = readGenericAmbient(value);
  const b = readScoped(value);
  return `${a}|${b}`;
}

export type AtypesMarker = GenericAmbientMarker & ScopedMarker;

// typeRoots restriction is demonstrated by tsconfig.json { typeRoots: ["./local-types", "./node_modules/@types"], types: [] }
// types: [] restricts automatic inclusion; only local-types and generic-ambient are resolved via explicit import or triple-slash.
