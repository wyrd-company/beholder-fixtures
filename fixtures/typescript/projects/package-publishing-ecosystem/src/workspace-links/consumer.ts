// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readWorkspaceA } from "@fixtures/workspace-a";
import { readWorkspaceB } from "@fixtures/workspace-b";
import { readDirect } from "@fixtures/direct-dep";
import { readTransitive } from "@fixtures/transitive-dep";
import { readPeer } from "@fixtures/peer-dep";
import { tokenV1 } from "@fixtures/sensitive-lib";
import { tokenV2 } from "../../packages/workspace-a/src/sensitive-bridge.js";
import { readAlias } from "@fixtures/source-alias-pkg/src/index.js";
import { readAlias as readAliasBuilt } from "@fixtures/source-alias-pkg/dist/index.js";

export function describeWorkspace(value: string): string {
  const a = readWorkspaceA(value);
  const b = readWorkspaceB(value);
  const c = readDirect(value);
  const d = readTransitive(value);
  const e = readPeer(value);
  const f = readAlias(value).value;
  const g = readAliasBuilt(value).value;
  return `${a}|${b}|${c}|${d}|${e}|${f}|${g}`;
}

export function describeSensitive(
  a: import("@fixtures/sensitive-lib").SensitiveToken,
  b: import("../../packages/workspace-a/src/sensitive-bridge.js").SensitiveToken,
): string {
  return `${a.getValue()}|${b.getValue()}:${(b as import("../../packages/workspace-a/node_modules/@fixtures/sensitive-lib/index.js").SensitiveToken).getVersion()}`;
}

// Demonstrates two installed versions of nominally sensitive declaration with private brand incompatibility.
export const v1Token: import("@fixtures/sensitive-lib").SensitiveToken =
  tokenV1;
export const v2Token: import("../../packages/workspace-a/src/sensitive-bridge.js").SensitiveToken =
  tokenV2;

// npm hoisting: transitive-dep is hoisted to root node_modules and also reachable as dependency of direct-dep.
// peer type dependency is consumed directly.
// workspace link is consumed via @fixtures/workspace-a which depends on workspace-b.
// source-alias versus built-declaration consumption shows both src alias and dist declaration paths.
