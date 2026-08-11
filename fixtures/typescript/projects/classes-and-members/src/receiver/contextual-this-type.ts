// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Contextual ThisType for object-literal methods. */

export type Labeled = {
  label: string;
  describe(this: Labeled): string;
};

export function createLabeled(label: string): Labeled & ThisType<Labeled> {
  return {
    label,
    describe(this: Labeled) {
      return this.label;
    },
  } as Labeled & ThisType<Labeled>;
}

export function exerciseContextualThisType(): void {
  const labeled = createLabeled("sample");
  const text: string = labeled.describe();
  void text;

  // ThisType allows methods inside an object literal to see `this` as the host type.
  const container: {
    items: string[];
    add(this: { items: string[] }, item: string): void;
  } & ThisType<{ items: string[] }> = {
    items: [],
    add(this: { items: string[] }, item: string) {
      this.items.push(item);
    },
  };
  container.add("hello");
}
