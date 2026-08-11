// Honoring `exports` and `imports` maps under nodenext / bundler
import { pkgTag } from "./pkg/index.js";
import { utilTag } from "./pkg/util.js";
import { coreTag } from "#core/constants.js";

export function consumeExports(): string {
  return `${pkgTag}:${utilTag}:${coreTag}`;
}
