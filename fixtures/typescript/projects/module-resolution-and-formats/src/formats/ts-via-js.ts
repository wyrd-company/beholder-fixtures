// .js-suffixed import resolving to .ts source under nodenext / bundler (rewrite)
import { coreTag } from "../core/constants.js";
import { makeLeaf } from "../core/util.js";
import type { DeclShape } from "./decl-shapes.js";

export function viaJsExtension(id: string): DeclShape {
  const leaf = makeLeaf(id);
  return { tag: coreTag, value: leaf.id.length };
}
