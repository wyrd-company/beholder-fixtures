// PreserveSymlinks:true keeps package symlink distinct from real path (split identities)
// This file is compiled only under the preserveSymlinks:true context.
import { Shared as SharedReal, sharedValue as viaReal } from "./real/shared.js";
import {
  Shared as SharedLink,
  sharedValue as viaLink,
} from "@fixtures/shared-real/shared.js";

export function readBothPreserved(): string {
  const r: SharedReal = viaReal;
  const l: SharedLink = viaLink;
  return `${r.tag}:${l.tag}:${r.value}:${l.value}`;
}

export type AreSharedSameUnderPreserve = SharedReal extends SharedLink
  ? true
  : false;
export const areSharedSame: AreSharedSameUnderPreserve = false;
