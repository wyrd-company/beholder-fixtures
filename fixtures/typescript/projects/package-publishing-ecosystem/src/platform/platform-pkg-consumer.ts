// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { read as readPlatformDefault } from "@fixtures/platform-pkg";
import { read as readBrowser } from "@fixtures/platform-pkg/browser";
import { read as readServer } from "@fixtures/platform-pkg/server";
import { read as readNative } from "@fixtures/platform-pkg/native";

export function describePlatformPkg(value: string): string {
  return `${readPlatformDefault(value)}|${readBrowser(value)}|${readServer(value)}|${readNative(value)}`;
}
