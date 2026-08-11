/**
 * CommonJS assignment exports and `require` without a file-level check directive.
 */

/**
 * @param {number} a
 * @param {number} b
 */
function add(a, b) {
  return a + b;
}

module.exports = add;
exports.add = add;
/**
 * @param {number} a
 * @param {number} b
 */
exports.multiply = function multiply(a, b) {
  return a * b;
};

const helper = require("./unchecked-plain.js");
exports.helperRef = helper;
