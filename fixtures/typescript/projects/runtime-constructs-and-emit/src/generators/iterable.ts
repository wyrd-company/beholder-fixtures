// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class LedgerIterable implements Iterable<string> {
  constructor(private readonly items: string[]) {}

  *[Symbol.iterator](): Iterator<string> {
    for (const item of this.items) {
      yield item.toUpperCase();
    }
  }
}

export class CounterIterator implements Iterator<number> {
  private index = 0;
  constructor(private readonly limit: number) {}

  next(): IteratorResult<number> {
    if (this.index < this.limit) {
      return { value: this.index++, done: false };
    }
    return { value: undefined, done: true };
  }
}

export class CounterIterable implements Iterable<number> {
  constructor(private readonly limit: number) {}

  [Symbol.iterator](): Iterator<number> {
    return new CounterIterator(this.limit);
  }
}

export function consumeIterable(iterable: Iterable<string>): string {
  let result = "";
  for (const value of iterable) {
    result += value + "|";
  }
  return result;
}
