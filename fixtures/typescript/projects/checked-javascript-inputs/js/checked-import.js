// @ts-check

/** @import { Coordinate } from "./checked-typedefs.js" */

/**
 * Describe a coordinate using an imported typedef.
 * @param {Coordinate} point
 * @returns {string}
 */
function describe(point) {
  return `${point.x},${point.y}`;
}

module.exports = { describe };
