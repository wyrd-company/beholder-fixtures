// @ts-check

const { sum } = require("./unchecked-plain.js");
const { pick } = require("./checked-typedefs.js");
const fromTs = require("../src/to-javascript.js");

module.exports = {
  combined: sum(1, 2) + pick({ a: 1 }, "a"),
  fromTs: fromTs.describeFromTs(),
};
