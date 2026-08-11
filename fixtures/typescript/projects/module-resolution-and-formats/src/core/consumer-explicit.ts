// Explicit ESM .js extensions resolving to .ts (nodenext / bundler)
import { makeLeaf } from "./util.js";
import { coreTag } from "./constants.js";
import { describeNode } from "./types.js";
import { getCoreTag } from "./index.js";

export function runExplicit(): string {
  const node = makeLeaf("beta");
  return `${getCoreTag()}:${describeNode(node)}:${coreTag}`;
}
