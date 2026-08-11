// Consumer using .ts extensions with allowImportingTsExtensions + rewriteRelativeImportExtensions
// Under rewrite mode, "./util.ts" is rewritten to "./util.js" in emit
import { makeLeaf } from "../core/util.ts";
import { coreTag } from "../core/constants.ts";

export function rewriteViaTsExt(id: string): string {
  const leaf = makeLeaf(id);
  return `${coreTag}:${leaf.id}`;
}
