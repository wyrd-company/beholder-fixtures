// JavaScript CJS counterpart (.cjs)
module.exports.marker = "cjs-helper";

module.exports.describeCjs = function describeCjs(value) {
  return `cjs:${value}`;
};
