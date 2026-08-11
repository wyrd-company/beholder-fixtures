// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function switchTrueNarrowing(value: string | number | boolean): string {
  switch (true) {
    case typeof value === "string":
      return `string:${value.toUpperCase()}`;
    case typeof value === "number":
      return `number:${value.toFixed(1)}`;
    case value === true:
      return "boolean-true";
    case value === false:
      return "boolean-false";
    default:
      return "unknown";
  }
}

export function switchTrueWithDiscriminant(
  shape: { kind: "a"; count: number } | { kind: "b"; tag: string },
): string {
  switch (true) {
    case shape.kind === "a":
      return `a:${shape.count}`;
    case shape.kind === "b":
      return `b:${shape.tag}`;
    default:
      return "none";
  }
}
