// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Heterogeneous {
  NumericPart = 0,
  TextPart = "TEXT",
  NextNumeric = 1,
  AnotherText = "ANOTHER",
}

export function describeHeterogeneous(value: Heterogeneous): string {
  if (typeof value === "number") {
    return `number:${value}`;
  }
  return `string:${value}`;
}

export function heterogeneousMembers(): Array<string | number> {
  return [
    Heterogeneous.NumericPart,
    Heterogeneous.TextPart,
    Heterogeneous.NextNumeric,
    Heterogeneous.AnotherText,
  ];
}
