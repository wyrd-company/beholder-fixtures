// Multiple path spellings resolving to one physical file through symlink layout
// Both logical spellings (real vs linked) point to same inode on case-sensitive linux host.
import { deepMarker as viaRealDeep } from "./real/nested/deep.js";
import { deepMarker as viaLinkDeep } from "./linked/nested/deep.js";

export function checkSpellings(): boolean {
  return viaRealDeep === viaLinkDeep;
}
