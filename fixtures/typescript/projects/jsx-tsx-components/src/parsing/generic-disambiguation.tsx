// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const wrapValue = <T,>(value: T): T => value;

export const renderIntrinsicInTsx = (
  <atlas-panel label="tsx-parsing" priority={1} />
);

export function buildTsxMapper<T>() {
  const identity = <U,>(item: U): U => item;
  return { identity, wrapValue };
}
