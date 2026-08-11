// Consumer that uses imports preserved verbatim under module: preserve
import { makeLeaf } from "../core/util.js";
import { coreTag } from "../core/constants.js";

export function preserved(): string {
  const leaf = makeLeaf("preserve");
  return `${coreTag}:${leaf.id}`;
}
