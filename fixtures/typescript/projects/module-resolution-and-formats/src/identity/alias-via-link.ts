// Logical access via symlink path — resolves to same physical file as alias-via-real
import { sharedValue, describeShared } from "./linked/shared.js";
import { readDeep } from "./linked/nested/deep.js";

export function viaLink(): string {
  return `${describeShared(sharedValue)}:${readDeep()}`;
}
