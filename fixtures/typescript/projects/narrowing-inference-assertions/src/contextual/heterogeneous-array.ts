// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function heterogeneousBestCommonTypeChanges(): string {
  const strings = ["atlas", "ledger"];
  const numbers = [1, 2, 3];
  const mixed: Array<string | number> = [...strings, ...numbers];
  const narrowed = mixed.filter(
    (value): value is string => typeof value === "string",
  );
  return narrowed.join("-");
}

export function homogeneousThenHeterogeneous(): Array<string | number> {
  const items: string[] = ["atlas"];
  const combined: Array<string | number> = [...items, 42];
  return combined;
}

export function contextualReturnInference(): string {
  const produce = (value: string): string => value.toUpperCase();
  const result: string = produce("atlas");
  return result;
}

export function undefinedReturnInference(): void {
  const handler = (label: string) => {
    if (label.length === 0) {
      return;
    }
    consumeLabel(label);
  };
  handler("atlas");
}

function consumeLabel(value: string): void {
  void value;
}

export function alreadyWidenedVariable(): string {
  let label: string | null = Math.random() > 0.5 ? "atlas" : null;
  if (label === null) {
    return "empty";
  }
  return label.toUpperCase();
}
