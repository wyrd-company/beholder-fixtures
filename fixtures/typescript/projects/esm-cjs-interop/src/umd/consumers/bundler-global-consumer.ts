// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

/// <reference path="../types/bundler-dial-shim.d.ts" />

export function readBundlerDialGlobal(): number {
  return BundlerDial.spin();
}
