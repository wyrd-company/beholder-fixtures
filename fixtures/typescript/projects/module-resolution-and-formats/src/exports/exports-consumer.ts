// Honoring `exports` and `imports` maps under nodenext / bundler via package symlink
import { pkgTag } from "@fixtures/exported-pkg";
import { utilTag } from "@fixtures/exported-pkg/util";
import { withInternal } from "@fixtures/exported-pkg/with-internal";
import { coreTag } from "#core/constants.js";

export function consumeExports(): string {
  return `${pkgTag}:${utilTag}:${withInternal}:${coreTag}`;
}
