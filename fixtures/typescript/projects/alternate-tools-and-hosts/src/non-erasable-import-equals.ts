/**
 * Non-erasable syntax: import-equals is CommonJS modeling that requires transform.
 * Node strip-only mode rejects `import = require()`; Bun transpiles it (TS-CAN-091).
 */

import fs = require("fs");

export const read = fs.readFileSync;

export import AliasFS = fs;

export function fileExists(path: string): boolean {
  return fs.existsSync(path);
}
