// Duplicate logical access paths: unify through one real path (default preserveSymlinks:false)
// and split into distinct identities when preserveSymlinks:true. Both imports below
// spell different logical paths but hit one physical file via symlink.
import { sharedValue as viaRealValue } from "./real/shared.js";
import { sharedValue as viaLinkValue } from "./linked/shared.js";
import { sensitiveV1 } from "./vendor-v1/sensitive.js";
import { sensitiveV2 } from "./vendor-v2/sensitive.js";

export function checkUnify(): boolean {
  // Under preserveSymlinks:false both Shared identities unify to one declaration
  return viaRealValue.value === viaLinkValue.value;
}

export function checkTwoVersions(): string {
  return `${sensitiveV1.brand}:${sensitiveV2.brand}`;
}
