// noImplicitAny off: unannotated parameter is valid and inferred as any.
// Under noImplicitAny true this file would be an error; it is isolated to the off context.

export function unannotatedParam(x) {
  return x;
}

export function unannotatedHandler(value) {
  return String(value);
}
