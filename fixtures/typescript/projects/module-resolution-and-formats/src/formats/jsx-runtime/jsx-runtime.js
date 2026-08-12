export function jsx(type, props, key) {
  return { type, props: props ?? {}, key: key ?? null, __jsx: true };
}
export function jsxs(type, props, key) {
  return jsx(type, props, key);
}
export const Fragment = Symbol.for("jsx.fragment");
export function jsxDEV(type, props, key) {
  return jsx(type, props, key);
}
