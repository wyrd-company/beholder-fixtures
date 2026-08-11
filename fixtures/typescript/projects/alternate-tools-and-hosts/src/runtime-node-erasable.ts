/**
 * Runtime-native execution on Node.js type stripping (TS-CAN-091).
 * This file contains only erasable syntax so it executes via
 * `node --experimental-strip-types` without type checking.
 */

type Config = {
  debug: boolean;
  label: string;
};

const config: Config = { debug: false, label: "node-erasable" };

function describe(c: Config): string {
  return `${c.label}:${c.debug}`;
}

console.log(describe(config));
