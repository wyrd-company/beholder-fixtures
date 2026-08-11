// @ts-check

/**
 * @param {unknown} value
 * @returns {number}
 */
function asNumber(value) {
  return /** @type {number} */ (value);
}

/** @type {{ count: number, expando?: string }} */
const holder = { count: 1 };
holder.expando = "extra";

module.exports = { asNumber, holder };
