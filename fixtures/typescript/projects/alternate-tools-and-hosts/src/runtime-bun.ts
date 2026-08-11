/**
 * Runtime-native execution on Bun (TS-CAN-091).
 * Bun executes TypeScript natively including non-erasable syntax,
 * with partial tsconfig support and distinct specifier resolution.
 *
 * - Uses enum, namespace, and parameter-property (non-erasable) — contrast with runtime-node-erasable.ts
 * - Uses real relative extension "./helpers.ts" (extensionless "./helpers" is exercised via `bun run src/with-extension.ts` in Taskfile)
 * - Executes without type checking: `bun run` executes without a prior `tsc` check (see Taskfile build/test)
 */

import { Status } from "./non-erasable-enum.ts";
import { Catalog } from "./non-erasable-namespace.ts";
import { CatalogEntry } from "./non-erasable-param-property.ts";
import { helperValue } from "./helpers.ts";

// Bun partial tsconfig support: "erasableSyntaxOnly" and declaration options are ignored at runtime
// Bun distinct specifier: `runtime-bun.ts` uses real "./helpers.ts"; extensionless "./helpers" is covered by `src/with-extension.ts` via `bun run`

// double assertion passes `tsc`; execution without type checking is the separate `bun run` invocation without a type check
const unchecked: string = helperValue as unknown as string;

const entry = new CatalogEntry("bun-1", "BunEntry", "runtime");

console.log(
  `bun host: status=${Status[Status.Active]} catalog=${Catalog.version} entry=${entry.display} helper=${helperValue} unchecked=${unchecked}`,
);
