import { makeLeaf } from "../core/util.js";
import type { GraphNode } from "../core/types.js";
import { readB } from "./node-b.js";

export function readA(): GraphNode {
  return makeLeaf("a");
}

export function linkAtoB(): string {
  return `${readA().id}->${readB().id}`;
}
