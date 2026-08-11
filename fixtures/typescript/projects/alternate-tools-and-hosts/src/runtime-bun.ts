/**
 * Runtime-native execution on Bun (TS-CAN-091).
 * Bun executes TypeScript natively including non-erasable syntax,
 * with partial tsconfig support and distinct specifier resolution.
 *
 * - Uses enum, namespace, and parameter-property (non-erasable) — contrast with runtime-node-erasable.ts
 * - Uses real relative extension "./helpers.ts" and extensionless "./helpers"
 * - Executes without type checking: a type error here would still run (execution without type checking)
 */

import { Status } from "./non-erasable-enum.ts";
import { Catalog } from "./non-erasable-namespace.ts";
import { CatalogEntry } from "./non-erasable-param-property.ts";
import { helperValue } from "./helpers.ts";

// Bun partial tsconfig support: "erasableSyntaxOnly" and declaration options are ignored at runtime
// Bun distinct specifier: resolves both "./helpers.ts" and "./helpers"

// type mismatch that would fail `tsc` but Bun executes without checking (execution without type checking)
const unchecked: string = helperValue as unknown as string;

const entry = new CatalogEntry("bun-1", "BunEntry", "runtime");

console.log(`bun host: status=${Status[Status.Active]} catalog=${Catalog.version} entry=${entry.display} helper=${helperValue} unchecked=${unchecked}`);
