// Nearest package `type` lookup: .ts file under type:module vs type:commonjs
// Import is relative; resolution respects nearest package.json `type` field
import { esmValue } from "../packages/esm-type/index.js";
import { cjsValue } from "../packages/cjs-type/index.js";

export function checkNearestType(): string {
  return `${esmValue}:${cjsValue}`;
}
