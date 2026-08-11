// Logical access via real path
import { sharedValue, describeShared } from "./real/shared.js";
import { readDeep } from "./real/nested/deep.js";

export function viaReal(): string {
  return `${describeShared(sharedValue)}:${readDeep()}`;
}
