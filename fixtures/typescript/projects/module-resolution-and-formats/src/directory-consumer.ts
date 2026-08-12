// Directory import (resolves to ./core/index.ts via directory specifier)
import { makeLeaf } from "./core";
import { describeNode } from "./core";

export function runDirectory(): string {
  const node = makeLeaf("gamma");
  return describeNode(node);
}
