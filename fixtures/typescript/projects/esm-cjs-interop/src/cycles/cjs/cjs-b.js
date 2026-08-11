"use strict";

// @ts-check

const cjsA = require("./cjs-a.js");

module.exports = {
  /** @returns {unknown} */
  readFromA: function readFromA() {
    return cjsA.readFromB();
  },
};
