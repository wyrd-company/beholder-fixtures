// Path alias with ordered fallback targets "@alias/*" -> ["./src/alias/*","./src/alias/fallback/*"].
// First target "primary" exists, second "secondary" only via fallback.

import { describePrimary } from "@alias/primary.js";
import { describeSecondary } from "@alias/secondary.js";

export function describeAlias(id: string): string {
  return `${describePrimary(id)}|${describeSecondary(id)}`;
}
