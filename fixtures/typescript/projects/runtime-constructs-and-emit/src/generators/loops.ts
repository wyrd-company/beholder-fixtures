// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function forOfDemo(values: string[]): string[] {
  const result: string[] = [];
  for (const value of values) {
    result.push(value.toUpperCase());
  }
  return result;
}

export function earlyCleanupDemo(values: string[]): string[] {
  const seen: string[] = [];
  for (const value of values) {
    seen.push(value);
    if (value === "stop") {
      break;
    }
  }
  return seen;
}

export async function forAwaitDemo(
  iterable: AsyncIterable<string>,
): Promise<string[]> {
  const result: string[] = [];
  for await (const value of iterable) {
    result.push(value);
  }
  return result;
}

export async function asyncFromSyncDemo(values: string[]): Promise<string[]> {
  const result: string[] = [];
  for await (const value of values) {
    result.push(value.toUpperCase());
  }
  return result;
}

export function downlevelForOfSpread(values: number[]): number[] {
  return [...values];
}

export async function iterateLedgerIterable(): Promise<string> {
  const ledger = { items: ["atlas", "ledger"] };
  class SimpleIterable implements Iterable<string> {
    *[Symbol.iterator](): Iterator<string> {
      for (const item of ledger.items) {
        yield item;
      }
    }
  }
  return consume(new SimpleIterable());
}

function consume(iterable: Iterable<string>): string {
  let out = "";
  for (const value of iterable) {
    out += value + ",";
  }
  return out;
}
