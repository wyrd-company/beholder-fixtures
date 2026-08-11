function read(value) {
  return `myCondition-cjs:${value}`;
}
function myConditionOnly(value) {
  return `myCondition-only-cjs:${value}`;
}
module.exports = { read, marker: "myCondition", myConditionOnly };
