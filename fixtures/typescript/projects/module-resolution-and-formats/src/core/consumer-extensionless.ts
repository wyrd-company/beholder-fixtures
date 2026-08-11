// Extensionless relative and directory imports (classic / node10)
import { makeLeaf } from "./util";
import { coreTag } from "./constants";
import { describeNode } from "./types";
import { getCoreTag } from "./index";

export function runExtensionless(): string {
  const node = makeLeaf("alpha");
  return `${getCoreTag()}:${describeNode(node)}:${coreTag}`;
}
