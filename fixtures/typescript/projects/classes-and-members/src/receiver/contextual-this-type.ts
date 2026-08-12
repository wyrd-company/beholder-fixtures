// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Contextual ThisType for object-literal methods. */

export type Labeled = {
  label: string;
  describe(): string;
};

export function createLabeled(label: string): Labeled {
  const labeled: Labeled & ThisType<Labeled> = {
    label,
    describe() {
      return this.label;
    },
  };
  return labeled;
}

export function exerciseContextualThisType(): void {
  const labeled = createLabeled("sample");
  const text: string = labeled.describe();
  void text;

  // ThisType supplies contextual `this` without an explicit `this` parameter.
  type Container = {
    items: string[];
    add(item: string): void;
  };

  const container: Container & ThisType<Container> = {
    items: [],
    add(item) {
      this.items.push(item);
    },
  };
  container.add("hello");
}
