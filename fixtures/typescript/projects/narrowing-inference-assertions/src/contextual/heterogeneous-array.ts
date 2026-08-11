// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function heterogeneousBestCommonTypeChanges(): [
  Array<string | number>,
  string[],
] {
  const mixedInferred = ["atlas", 1];
  const stringsInferred = ["atlas", "ledger"];
  return [mixedInferred, stringsInferred];
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
  const invoke = (handler: (label: string) => undefined): void => {
    void handler("atlas");
  };
  invoke((label) => {
    if (label.length === 0) {
      return;
    }
    consumeLabel(label);
  });
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
