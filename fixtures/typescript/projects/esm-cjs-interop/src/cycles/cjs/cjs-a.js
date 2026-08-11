"use strict";

const cjsB = require("./cjs-b.js");

module.exports = {
  readFromB: function readFromB() {
    return cjsB.readFromA();
  },
};
