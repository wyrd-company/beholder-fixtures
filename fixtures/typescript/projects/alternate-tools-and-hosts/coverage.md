---
relationships:
  references:
    - ground-rules
    - reports/typescript/synthesis/checklist
---

# Coverage — alternate-tools-and-hosts

| Canonical identifier | Stable source path | Named coverage source | Compilation context | Additional locators |
| --- | --- | --- | --- | --- |
| TS-CAN-090 | `tsconfig.json` | TypeScript check context: `compilerOptions.strict`, `target`, `module`, `declaration` — retained `tsc` type check | tsc type-check (pinned `typescript@5.9.3`) | Separate from non-tsc transform; `npx tsc --noEmit` in Taskfile `build` |
| TS-CAN-090 | `bunfig.toml` | Bun transpiler configuration: `loader: "ts"`, `target: "bun"` | Bun transpiler (locally installed `bun@1.3.14`) | Own config distinct from `tsconfig.json`; per-file `Bun.Transpiler` with `loader: "ts"` in `scripts/bun-transpile.ts` |
| TS-CAN-090 | `src/enum-differ.ts` | `enum Color { Red, Green, Blue }`, `colorName`, `primary` — construct whose transform differs | tsc vs Bun transpiler | `tsc` emits `(Color \|\| (Color = {}))` IIFE; Bun emits `(Color \|\|= {})` — documented in file comment and exercised by `scripts/bun-transpile.ts` |
| TS-CAN-090 | `scripts/bun-transpile.ts` | `new Bun.Transpiler({ loader: "ts", target: "bun" }).transformSync` per-file transform | Bun transpiler | Reads `src/enum-differ.ts`; logs transpiled output; also logs extensionless sample showing partial tsconfig behavior |
| TS-CAN-090 | `scripts/compiler-transform.ts` | `createExampleTransformer` — `ts.TransformerFactory` before transformer via `ts.transform` | Pinned compiler API (`typescript@5.9.3`) before transformer | Uses `ts.createSourceFile` + `ts.transform` + `ts.createPrinter`; transformer kind: before |
| TS-CAN-090 | `scripts/compiler-transform.ts` | `factory.createStringLiteral("synthetic-node")` with `ts.setTextRange(..., { pos: -1, end: -1 })` | Pinned compiler API | Synthetic node without source position; verified `pos === -1` on literal |
| TS-CAN-090 | `scripts/compiler-transform.ts` | Injected `export const __generatedRuntimeEdge = "synthetic-node"` | Pinned compiler API before transformer | Generated runtime edge absent from `src/transform-source.ts`; appended to `SourceFile.statements`; printed via `ts.createPrinter` |
| TS-CAN-090 | `src/transform-source.ts` | `function greet`, `type GreetFn`, `greetingKind` — source consumed by transformer | Pinned compiler API source input | Input to `scripts/compiler-transform.ts`; no generated edge in source |
| TS-CAN-091 | `src/erasable.ts` | `type Alias`, `interface Item`, `type Handler`, `type Config`, `makeItem`, `handleItem` — erasable syntax only | Node.js type stripping (`node --experimental-strip-types`) | Succeeds under `node --experimental-strip-types src/runtime-node-erasable.ts` via `erasable.ts` types |
| TS-CAN-091 | `src/runtime-node-erasable.ts` | `type Config`, `const config: Config`, `describe` — erasable-only file executed natively | Node.js type stripping | Executed in Taskfile `build`/`test` via `node --experimental-strip-types src/runtime-node-erasable.ts`; no type checking |
| TS-CAN-091 | `src/non-erasable-enum.ts` | `enum Status`, `current`, `isActive` | Node.js strip-only (rejected) vs Bun (accepted) | `node --experimental-strip-types` on this file emits `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` (enum not supported); `bun run` succeeds — contrast documented in file comment |
| TS-CAN-091 | `src/non-erasable-namespace.ts` | `namespace Catalog`, `version`, `Entry`, `describe` | Node.js strip-only (rejected) vs Bun (accepted) | Same contrast as enum; namespace emits runtime object |
| TS-CAN-091 | `src/non-erasable-param-property.ts` | `class CatalogEntry` with `public id`, `private label`, `protected kind` parameter properties | Node.js strip-only (rejected) vs Bun (accepted) | `constructor(public id: string, ...)` — Bun synthesizes field assignment, Node rejects |
| TS-CAN-091 | `src/non-erasable-import-equals.ts` | `import fs = require("fs")`, `export import AliasFS = fs` | Node.js strip-only (rejected) vs Bun (accepted) | `import = require` CommonJS modeling; Bun transpiles, Node strip rejects |
| TS-CAN-091 | `tsconfig.erasable.json` | `compilerOptions.erasableSyntaxOnly: true` with `include: ["src/erasable.ts", "src/runtime-node-erasable.ts"]` | tsc erasableSyntaxOnly check | Validates that erasable-only files pass under `erasableSyntaxOnly`; non-erasable files excluded — `npx tsc --noEmit -p tsconfig.erasable.json` in Taskfile |
| TS-CAN-091 | `src/with-extension.ts` | `import { helperValue } from "./helpers.ts"` (real `.ts` extension) and `from "./helpers"` (extensionless) | tsc (`allowImportingTsExtensions` + `rewriteRelativeImportExtensions`) and Bun/Node resolution | Real relative extensions: `.ts` import rewritten to `.js` by tsc; extensionless resolved by Bun but not Node ESM — no `paths` used |
| TS-CAN-091 | `src/helpers.ts` | `helperValue`, `HelperType`, `helperAdd` — target of relative imports | Default tsc / Bun / Node | No `paths` or `baseUrl` in `tsconfig.json`; all specifiers are relative `./helpers` or `./helpers.ts` |
| TS-CAN-091 | `tsconfig.json` | No `paths`, no `baseUrl` — `compilerOptions` omits both | tsc (all contexts) | Demonstrates "no `paths`" obligation; imports are relative only; Bun also lacks `paths` mapping |
| TS-CAN-091 | `src/runtime-bun.ts` | `import { Status } from "./non-erasable-enum.ts"`, `Catalog`, `CatalogEntry`, `helperValue`, unchecked `string = helperValue as unknown as string` | Bun runtime-native (`bun run src/runtime-bun.ts`) | Bun's distinct specifier: accepts both `"./helpers.ts"` and `"./helpers"`; partial tsconfig: ignores `erasableSyntaxOnly` and declaration opts; execution without type checking — type mismatch `helperValue as unknown as string` would fail `tsc` but runs |
| TS-CAN-091 | `Taskfile.yml` | `build` task: `node --experimental-strip-types src/runtime-node-erasable.ts` and `bun run src/runtime-bun.ts` | Node.js and Bun host contexts | Execution without type checking in both hosts; `lint` is `tsc --noEmit`; `test` repeats host execution; no downloads |
