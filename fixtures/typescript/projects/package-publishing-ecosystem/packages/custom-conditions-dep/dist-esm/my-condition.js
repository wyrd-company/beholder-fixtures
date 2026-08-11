export function read(value) {
  return `myCondition:${value}`;
}
export const marker = "myCondition";
export function myConditionOnly(value) {
  return `myCondition-only:${value}`;
}
