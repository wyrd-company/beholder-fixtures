// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Numeric {
  Alpha = 0,
  Beta = 1,
  Gamma = 2,
}

export enum NumericWithStart {
  First = 10,
  Second,
  Third,
}

export function numericReverseMap(value: Numeric): string | undefined {
  return Numeric[value];
}

export function numericReverseLookup(): number | string {
  const byValue = Numeric[1];
  const byName = Numeric["Beta"];
  return `${byValue}:${byName}`;
}

export function consumeNumeric(value: Numeric): string {
  return `numeric:${value}:${Numeric[value]}`;
}
