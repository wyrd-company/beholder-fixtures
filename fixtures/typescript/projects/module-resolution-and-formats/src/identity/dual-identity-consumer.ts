// Duplicate logical access paths unify through one real path when preserveSymlinks:false.
// Package/workspace symlink @fixtures/shared-real points to src/identity/real; both specifiers
// resolve to the same physical file when symlinks are resolved.
import {
  Shared as SharedReal,
  sharedValue as viaRealValue,
} from "./real/shared.js";
import {
  Shared as SharedLink,
  sharedValue as viaLinkValue,
} from "@fixtures/shared-real/shared.js";
import {
  Sensitive as SensitiveV1,
  sensitiveV1,
} from "./vendor-v1/sensitive.js";
import {
  Sensitive as SensitiveV2,
  sensitiveV2,
} from "./vendor-v2/sensitive.js";

export function checkUnify(): boolean {
  // Under preserveSymlinks:false both Shared imports unify to one declaration identity
  const a: SharedReal = viaRealValue;
  const b: SharedLink = a;
  return b.value === a.value && viaLinkValue.value === 42;
}

export type AreSensitiveCompatible = SensitiveV1 extends SensitiveV2
  ? true
  : false;
export const areSensitiveCompatible: AreSensitiveCompatible = false;

export function checkTwoVersions(v1: SensitiveV1, v2: SensitiveV2): string {
  return `${v1.brand}:${v2.brand}`;
}

export function acceptV1Only(v: SensitiveV1): string {
  return v.brand;
}

export const keepV1 = sensitiveV1;
export const keepV2 = sensitiveV2;
