/**
 * TypeScript consumer of checked and unchecked JavaScript modules.
 */

import unchecked = require("../js/unchecked-plain.js");
import overloads = require("../js/checked-overloads.js");
import checkedImport = require("../js/checked-import.js");
import casts = require("../js/checked-casts-expand.js");
import commonjs = require("../js/commonjs-shapes.js");
import constructorProto = require("../js/constructor-prototype.js");
import ignored = require("../js/ignored-tag.js");
import nocheck = require("../js/nocheck-module.js");
import jsxComponent = require("../js/component.jsx");
import fromJs = require("../js/from-typescript.js");
import shallowTyped = require("@fixtures/shallow-typed");
import { describeFromTs } from "./to-javascript.ts";

const counter = new constructorProto.Counter();
counter.increment();

export function aggregate(): string {
  const sum = unchecked.sum(1, 2);
  const norm = overloads.normalize("ok");
  const coordDesc = checkedImport.describe({ x: 1, y: 2 });
  const casted = casts.asNumber("3");
  const tagged = ignored.label;
  const loose = nocheck.loose(1);
  const multiplied = commonjs.multiply(2, 3);
  const shallow = shallowTyped.read();
  const fromJsCombined = fromJs.combined;
  const tsFromJs = fromJs.fromTs;
  const marker = jsxComponent.Marker({ label: "jsx" });
  return [
    sum,
    norm,
    coordDesc,
    casted,
    tagged,
    loose,
    multiplied,
    shallow,
    fromJsCombined,
    tsFromJs,
    describeFromTs(),
    counter.value,
    marker,
  ].join("-");
}

export { jsxComponent };
