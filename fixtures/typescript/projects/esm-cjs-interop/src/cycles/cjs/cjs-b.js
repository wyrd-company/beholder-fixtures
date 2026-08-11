"use strict";

const cjsA = require("./cjs-a.js");

module.exports = {
  readFromA: function readFromA() {
    return cjsA.readFromB();
  },
};
