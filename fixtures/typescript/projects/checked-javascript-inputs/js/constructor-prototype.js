// @ts-check

/**
 * @param {*} proto
 * @param {string} name
 * @param {function} fn
 */
function attach(proto, name, fn) {
  proto[name] = fn;
}

/**
 * @constructor
 */
function Counter() {
  /** @type {number} */
  this.value = 0;
}

Counter.prototype.increment = function increment() {
  this.value += 1;
};

module.exports = { Counter, attach };
