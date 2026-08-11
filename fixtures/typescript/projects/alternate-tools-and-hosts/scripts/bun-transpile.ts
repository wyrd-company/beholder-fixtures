/**
 * Per-file transform through the locally installed Bun transpiler (TS-CAN-090).
 * Own configuration is via bunfig.toml and the per-file loader option.
 * The retained `tsc` check is separate (tsconfig.json).
 */

import { readFileSync } from "node:fs";

const sourcePath = "src/enum-differ.ts";
const source = readFileSync(sourcePath, "utf8");

// Bun.Transpiler is available when running under Bun (bun run)
const TranspilerCtor = (
  globalThis as unknown as {
    Bun: {
      Transpiler: new (opts: unknown) => { transformSync(s: string): string };
    };
  }
).Bun?.Transpiler;

if (!TranspilerCtor) {
  console.error(
    "Bun.Transpiler not available: run with `bun run scripts/bun-transpile.ts`",
  );
  process.exit(1);
}

const transpiler = new TranspilerCtor({ loader: "ts", target: "bun" });
const output = transpiler.transformSync(source);

console.log(
  `// per-file Bun transform of ${sourcePath} — enum differs from tsc`,
);
console.log(output);

// Also demonstrate that Bun ignores `erasableSyntaxOnly` and `paths` (partial tsconfig support)
const transpiler2 = new TranspilerCtor({ loader: "ts", target: "bun" });
const erasableSample = `import { helperValue } from "./helpers"; const x: number = helperValue;`;
console.log(
  "// bun partial tsconfig: extensionless import kept, erasableSyntaxOnly not enforced",
);
console.log(transpiler2.transformSync(erasableSample));
