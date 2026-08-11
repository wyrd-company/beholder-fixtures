// Demonstrates .mjs <-> .mts pairing and .cjs <-> .cts pairing via explicit extensions
import { describeNative } from "./native.mjs";
import { describeLegacy } from "./legacy.cjs";
import { describeMjs } from "./esm-helpers.mjs";
import type { NativeDecl } from "./native-decl.d.mjs";
import type { LegacyDecl } from "./legacy-decl.d.cts";

export function bridgeFormats(token: string): string {
  const fromMts = describeNative(token);
  const fromCts = describeLegacy(token);
  const fromMjs = describeMjs(token);
  return `${fromMts}|${fromCts}|${fromMjs}`;
}

export function readDeclPair(native: NativeDecl, legacy: LegacyDecl): string {
  return `${native.token}:${legacy.marker}`;
}
