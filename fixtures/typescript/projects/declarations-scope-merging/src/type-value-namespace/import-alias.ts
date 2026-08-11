// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import {
  Bundle,
  BundleKind,
  createBundle,
  type BundleOptions,
} from "./bundle-module.js";

/** Import alias carrying constructor, enum, and namespace meanings from one module. */
import BundleAlias = Bundle;

export function useImportAlias(): {
  options: BundleOptions;
  instance: Bundle;
  kind: BundleKind;
  flattened: BundleOptions;
} {
  const options: BundleOptions = { size: 3 };
  const instance = createBundle(options);
  const kind: BundleKind = BundleKind.Nested;
  const flattened = Bundle.flatten(options);
  const aliasType: BundleAlias = instance;

  return { options, instance: aliasType, kind, flattened };
}
