// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Interface merging overloads: reopened interface contributes additional call signatures. */
export interface MergedFormatter {
  format(value: string): string;
  format(value: number): string;
}

export interface MergedFormatter {
  format(value: string, locale: string): string;
}

export const mergedFormatter: MergedFormatter = {
  format(value: string | number, locale?: string): string {
    if (typeof value === "number") return String(value);
    return locale ? `${value}@${locale}` : value;
  },
};

export function exerciseMergedOverloads(): void {
  const a: string = mergedFormatter.format("hi");
  const b: string = mergedFormatter.format(10);
  const c: string = mergedFormatter.format("hi", "en");
  void a;
  void b;
  void c;
}
