#!/usr/bin/env node
// Incremental rebuild-scope demonstration for TS-CAN-005 — valid, non-mutating.
//
// Proves the two required build-mode rebuild scopes with `tsc -b` and
// `.tsbuildinfo`:
//   - an implementation-only edit rebuilds only `core`; its emitted `.d.ts` is
//     unchanged, so `app` stays up to date with its dependencies' declarations;
//   - a public-declaration edit rebuilds `core` and `app`.
//
// Every edit happens in a throwaway temp copy, so tracked source is never
// mutated and no network is used. The demo fails (non-zero exit) if any
// compiler run reports an error or if either observed rebuild scope differs
// from the scope TS-CAN-005 requires — a green run is therefore evidence of the
// distinct scopes, not merely that `tsc` was invoked.

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(here, "..");
const tsc = path.join(projectRoot, "node_modules/.bin/tsc");

const CORE = "packages/core/tsconfig.json";
const APP = "packages/app/tsconfig.json";

function runTscB(cwd, verbose = false) {
  const args = verbose ? ["-b", "--verbose"] : ["-b"];
  const res = spawnSync(tsc, args, { cwd, encoding: "utf8" });
  return {
    output: (res.stdout || "") + (res.stderr || ""),
    status: res.status,
  };
}

// True when `tsc -b --verbose` emitted a "Building project '<...>/relConfig'"
// line — the project was recompiled rather than skipped as up to date.
function rebuilt(output, relConfig) {
  const escaped = relConfig.replace(/[/.]/g, (c) => "\\" + c);
  return new RegExp("Building project '[^']*" + escaped + "'").test(output);
}

function fail(message, output) {
  throw new Error(
    "incremental-demo: " + message + (output ? "\n" + output : ""),
  );
}

function assertClean(step, run) {
  if (run.status !== 0) {
    fail(
      step + " must be valid source but tsc exited " + run.status,
      run.output,
    );
  }
}

// Assemble the minimal solution tree the composite build needs, plus the
// node_modules/@fixtures/shared-config link that resolves the package-based
// `extends`. The real tsc from projectRoot is reused, so TypeScript itself is
// never copied.
function stageProject(to) {
  for (const sub of [
    "packages",
    "config",
    "generated",
    "src",
    "tsconfig.json",
  ]) {
    const src = path.join(projectRoot, sub);
    if (fs.existsSync(src)) {
      fs.cpSync(src, path.join(to, sub), { recursive: true });
    }
  }
  const scope = path.join(to, "node_modules/@fixtures");
  fs.mkdirSync(scope, { recursive: true });
  fs.symlinkSync(
    "../../packages/shared-config",
    path.join(scope, "shared-config"),
  );
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "incremental-demo-"));
try {
  stageProject(tmp);

  // Clean baseline build populates dist/core and dist/app .tsbuildinfo state.
  assertClean("initial build", runTscB(tmp));

  // Implementation-only edit: change the value of `internalMultiplier`. It is
  // annotated `: number`, so its emitted declaration is unchanged; only core's
  // implementation differs, so core rebuilds and app stays up to date.
  const internal = path.join(tmp, "packages/core/src/internal.ts");
  const internalBefore = fs.readFileSync(internal, "utf8");
  const internalAfter = internalBefore.replace(
    "internalMultiplier: number = 3",
    "internalMultiplier: number = 7",
  );
  if (internalAfter === internalBefore) {
    fail("could not apply the implementation-only edit; source shape changed");
  }
  fs.writeFileSync(internal, internalAfter, "utf8");
  const impl = runTscB(tmp, true);
  assertClean("implementation-only rebuild", impl);
  const implCore = rebuilt(impl.output, CORE);
  const implApp = rebuilt(impl.output, APP);

  // Public-declaration edit: widen `formatResult` with an optional parameter.
  // This alters core's emitted api.d.ts without breaking app's existing call,
  // so both core and app rebuild.
  const api = path.join(tmp, "packages/core/src/api.ts");
  const apiBefore = fs.readFileSync(api, "utf8");
  const apiAfter = apiBefore
    .replace(
      "export function formatResult(result: RelayResult): string",
      "export function formatResult(result: RelayResult, suffix?: string): string",
    )
    .replace(
      "return `${result.label}:${result.value}`;",
      "return suffix === undefined\n    ? `${result.label}:${result.value}`\n    : `${result.label}:${result.value}:${suffix}`;",
    );
  if (apiAfter === apiBefore) {
    fail("could not apply the public-declaration edit; source shape changed");
  }
  fs.writeFileSync(api, apiAfter, "utf8");
  const pub = runTscB(tmp, true);
  assertClean("public-declaration rebuild", pub);
  const pubCore = rebuilt(pub.output, CORE);
  const pubApp = rebuilt(pub.output, APP);

  console.log(
    "incremental-demo: implementation-only edit rebuilds core:",
    implCore,
    "app:",
    implApp,
  );
  console.log(
    "incremental-demo: public-declaration edit rebuilds core:",
    pubCore,
    "app:",
    pubApp,
  );
  console.log(
    "incremental-demo: .tsbuildinfo present:",
    fs.existsSync(path.join(tmp, "dist/core/.tsbuildinfo")),
  );

  // Required TS-CAN-005 scopes: the implementation-only edit rebuilds core
  // alone; the public-declaration edit additionally rebuilds app.
  if (!implCore) {
    fail("implementation-only edit did not rebuild core", impl.output);
  }
  if (implApp) {
    fail(
      "implementation-only edit rebuilt app; scope is not implementation-only",
      impl.output,
    );
  }
  if (!pubCore) {
    fail("public-declaration edit did not rebuild core", pub.output);
  }
  if (!pubApp) {
    fail(
      "public-declaration edit did not rebuild app; declaration change did not propagate",
      pub.output,
    );
  }
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
