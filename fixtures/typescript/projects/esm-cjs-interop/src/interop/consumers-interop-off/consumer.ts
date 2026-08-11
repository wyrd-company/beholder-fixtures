// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import measureSpan = require("../../../deps/callable-cjs/index.js");
import * as recordNs from "../../../deps/object-cjs/index.js";
import objectRecord = require("../../../deps/object-cjs/index.js");
import propertyBagEquals = require("../../../deps/inherited-cjs/index.js");
import * as fakeEsmNs from "../../../deps/fake-esm-cjs/index.js";
import fakeEsmEquals = require("../../../deps/fake-esm-cjs/index.js");

export function spanWidth(left: number, right: number): number {
  return measureSpan(left, right);
}

export function readOwnField(): string {
  return recordNs.ownField;
}

export function readOwnViaEquals(): string {
  return objectRecord.readOwn();
}

export function readOwnMarkerEquals(): string {
  return propertyBagEquals.ownMarker;
}

export function readInheritedMarkerEquals(): string {
  return propertyBagEquals.inheritedMarker;
}

export function readFakeEsmNamespace(): string {
  return fakeEsmNs.packValue("ns").value;
}

export function readFakeEsmEquals(): string {
  return fakeEsmEquals.packValue("equals").value;
}
