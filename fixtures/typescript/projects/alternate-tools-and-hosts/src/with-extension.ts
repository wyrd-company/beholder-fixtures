/**
 * Real relative extensions and Bun vs Node resolution (TS-CAN-091).
 *
 * - `withExtensionTs` uses a real `.ts` extension permitted by
 *   `allowImportingTsExtensions` and rewritten by `rewriteRelativeImportExtensions`.
 *   Node's type-stripping requires a real extension; Bun accepts both.
 * - `withExtensionJs` style import would be the emitted `.js` form.
 * - `extensionless` uses no extension; Bun resolves it, Node ESM does not.
 * - No `paths` mapping is present; all specifiers are relative.
 */

// real relative extension: ".ts" source extension (allowed by tsconfig)
import { helperValue as hvTs } from "./helpers.ts";

// extensionless specifier: Bun's distinct resolution accepts this, Node requires extension
import { helperValue as hvBare } from "./helpers";

export const withExtensionTs = hvTs + 1;

export const extensionless = hvBare + 2;

export const bothResolveToSameValue = withExtensionTs === extensionless + 0;
