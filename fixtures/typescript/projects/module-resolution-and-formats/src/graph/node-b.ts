import { makeLeaf } from "../core/util.js";
import type { GraphNode } from "../core/types.js";
import { readA } from "./node-a.js";

export function readB(): GraphNode {
  return makeLeaf("b");
}

export function linkBtoA(): string {
  return `${readB().id}->${readA().id}`;
}
