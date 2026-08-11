// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import measureSpan = require("../../../deps/callable-cjs/index.js");
import measureDefault from "../../../deps/callable-cjs/index.js";
import * as recordNs from "../../../deps/object-cjs/index.js";
import objectRecord = require("../../../deps/object-cjs/index.js");
import objectDefault from "../../../deps/object-cjs/index.js";
import * as propertyBagNs from "../../../deps/inherited-cjs/index.js";
import propertyBagDefault from "../../../deps/inherited-cjs/index.js";
import propertyBagEquals = require("../../../deps/inherited-cjs/index.js");
import * as fakeEsmNs from "../../../deps/fake-esm-cjs/index.js";
import fakeEsmDefault from "../../../deps/fake-esm-cjs/index.js";

export function spanWidth(left: number, right: number): number {
  return measureSpan(left, right);
}

export function spanViaDefault(left: number, right: number): number {
  return measureDefault(left, right);
}

export function readOwnField(): string {
  return recordNs.ownField;
}

export function readOwnViaEquals(): string {
  return objectRecord.readOwn();
}

export function readOwnViaDefault(): string {
  return objectDefault.readOwn();
}

export function readOwnMarkerNamespace(): string {
  return propertyBagNs.ownMarker;
}

export function readInheritedMarkerNamespace(): string {
  return propertyBagNs.inheritedMarker;
}

export function readOwnMarkerDefault(): string {
  return propertyBagDefault.ownMarker;
}

export function readInheritedMarkerDefault(): string {
  return propertyBagDefault.inheritedMarker;
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

export function readFakeEsmDefault(): string {
  return fakeEsmDefault("default").value;
}
