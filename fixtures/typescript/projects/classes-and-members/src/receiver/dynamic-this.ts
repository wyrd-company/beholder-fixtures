// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Dynamic this via method extraction and explicit binding checks. */
export class DynamicCounter {
  count = 0;

  increment(this: DynamicCounter): void {
    this.count += 1;
  }

  getCount(this: DynamicCounter): number {
    return this.count;
  }
}

export function exerciseDynamicThis(): void {
  const counter = new DynamicCounter();
  counter.increment();

  // Method extraction loses the receiver; rebinding restores it.
  const extracted = counter.getCount;
  // Calling without receiver would fail under noImplicitThis / strict this checking.
  // Valid call binds the instance:
  const value: number = extracted.call(counter);
  const bound: number = extracted.bind(counter)();

  void value;
  void bound;

  // .call checking ensures the first argument matches the this parameter type.
  const other = { count: 99, getCount: counter.getCount };
  void other;
}
