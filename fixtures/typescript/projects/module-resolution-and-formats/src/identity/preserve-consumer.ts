// PreserveSymlinks:true keeps symlink identity distinct from real path
// This file is compiled only under the preserveSymlinks:true context.
import { sharedValue as viaReal } from "./real/shared.js";
import { sharedValue as viaLink } from "./linked/shared.js";

export function readBothPreserved(): string {
  return `${viaReal.tag}:${viaLink.tag}`;
}
