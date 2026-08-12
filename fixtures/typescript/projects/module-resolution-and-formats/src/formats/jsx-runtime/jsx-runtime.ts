export function jsx(
  type: unknown,
  props: Record<string, unknown> | null,
  key?: string,
): unknown {
  return { type, props: props ?? {}, key: key ?? null, __jsx: true };
}

export function jsxs(
  type: unknown,
  props: Record<string, unknown> | null,
  key?: string,
): unknown {
  return jsx(type, props, key);
}

export const Fragment = Symbol.for("jsx.fragment");

export function jsxDEV(
  type: unknown,
  props: Record<string, unknown> | null,
  key?: string,
): unknown {
  return jsx(type, props, key);
}
