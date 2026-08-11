// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import measureSpan = require("../../../deps/callable-cjs/index.js");
import * as recordNs from "../../../deps/object-cjs/index.js";
import objectRecord = require("../../../deps/object-cjs/index.js");
import DerivedReader = require("../../../deps/inherited-cjs/index.js");
import * as fakeEsmNs from "../../../deps/fake-esm-cjs/index.js";
import fakeEsmDefault from "../../../deps/fake-esm-cjs/index.js";

export function spanWidth(left: number, right: number): number {
  return measureSpan(left, right);
}

export function readOwnField(): string {
  return recordNs.ownField;
}

export function readOwnViaEquals(): string {
  return objectRecord.readOwn();
}

export function describeInherited(): string {
  const reader = new DerivedReader();
  return `${reader.describe()}:${reader.describeOwn()}`;
}

export function readFakeEsmNamespace(): string {
  return fakeEsmNs.packValue("ns").value;
}

export function readFakeEsmDefault(): string {
  return fakeEsmDefault.default("default").value;
}
