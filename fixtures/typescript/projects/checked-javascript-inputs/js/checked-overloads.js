// @ts-check

/**
 * @overload
 * @param {string} input
 * @returns {string}
 */

/**
 * @overload
 * @param {number} input
 * @returns {number}
 */

/**
 * @template T
 * @param {T} input
 * @returns {T}
 */
function normalize(input) {
  return input;
}

/** @satisfies {Record<string, unknown>} */
const metadata = { version: 1 };

module.exports = { normalize, metadata };
