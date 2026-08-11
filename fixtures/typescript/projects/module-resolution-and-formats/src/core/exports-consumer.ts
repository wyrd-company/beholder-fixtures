// Exports / imports field honoring via root package.json
import { makeLeaf } from "#core/util.js";
import { coreTag } from "#core/constants.js";
import { describeNode } from "#core/types.js";

export function runViaImportsField(): string {
  const node = makeLeaf("delta");
  return `${coreTag}:${describeNode(node)}`;
}
