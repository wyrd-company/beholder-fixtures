// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { Bundle, BundleKind, type BundleOptions } from "./bundle-module.js";

/** Import alias carrying constructor, enum, and namespace meanings from one module. */
import BundleAlias = Bundle;

export function useImportAlias(): {
  options: BundleOptions;
  instance: BundleAlias;
  kind: BundleKind;
  flattened: BundleOptions;
} {
  const options: BundleOptions = { size: 3 };
  const instance = new BundleAlias(options);
  const kind: BundleKind = BundleKind.Nested;
  const flattened = BundleAlias.flatten(options);

  return { options, instance, kind, flattened };
}
