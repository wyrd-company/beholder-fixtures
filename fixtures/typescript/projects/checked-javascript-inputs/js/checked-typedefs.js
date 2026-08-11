// @ts-check

/**
 * @export
 * @typedef {Object} Coordinate
 * @property {number} x
 * @property {number} y
 */

/**
 * @template T
 * @callback Mapper
 * @param {T} value
 * @returns {T}
 */

/**
 * @template {string} K
 * @param {Record<K, number>} table
 * @param {K} key
 * @returns {number}
 */
function pick(table, key) {
  return table[key];
}

module.exports = { pick };
