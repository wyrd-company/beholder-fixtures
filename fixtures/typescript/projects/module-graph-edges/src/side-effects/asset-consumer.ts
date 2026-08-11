// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Non-code side-effect import admitted by wildcard declaration
import "./asset.css";

// Default checking versus noUncheckedSideEffectImports with asset loader present:
// The side-effect import above resolves via the wildcard declaration; under
// default checking it is unchecked, under `noUncheckedSideEffectImports` it
// is verified against the declaration — both pass because loader is present.

export function describeAssetSideEffect(): string {
  return "asset-side-effect-loaded";
}
