// Wildcard specificity — longer pattern "@data/special/*" wins over "@data/*" for special/* imports.

import { describeGeneral } from "@data/general.js";
import { describeSpecific } from "@data/special/specific.js";

export function readWildcard(): string {
  return `${describeGeneral()}|${describeSpecific()}`;
}
