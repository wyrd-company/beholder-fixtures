"use strict";

// @ts-check

const cjsB = require("./cjs-b.js");

module.exports = {
  /** @returns {unknown} */
  readFromB: function readFromB() {
    return cjsB.readFromA();
  },
};
