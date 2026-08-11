// Directory import (resolves to ./index.ts via directory)
import { makeLeaf } from "./index.js";
import { describeNode } from "./index.js";

export function runDirectory(): string {
  const node = makeLeaf("gamma");
  return describeNode(node);
}
