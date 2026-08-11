import { coreTag } from "./constants.js";
import type { GraphNode } from "./types.js";

export function makeLeaf(id: string): GraphNode {
  return { kind: "leaf", id, next: undefined };
}

export function joinIds(a: string, b: string): string {
  return `${coreTag}:${a}/${b}`;
}

export const coreUtilMarker = "util-marker";
