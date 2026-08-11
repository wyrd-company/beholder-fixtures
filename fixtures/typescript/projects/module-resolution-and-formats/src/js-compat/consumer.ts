import { jsCompatMarker } from "./util.js";
import { makeLeaf } from "../core/util.js";

export function consumeJsCompat(id: string): string {
  const leaf = makeLeaf(id);
  return `${jsCompatMarker}:${leaf.id}`;
}
