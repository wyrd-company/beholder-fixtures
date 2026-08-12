import { describeNative } from "./native.mjs";
import { describeLegacy } from "./legacy.cjs";
import { Panel } from "./component.jsx";

export function describeMixed(title: string): string {
  const native = describeNative(title);
  const legacy = describeLegacy(title);
  const panel = Panel({ title, count: 1 });
  return `${native}|${legacy}|${panel}`;
}
