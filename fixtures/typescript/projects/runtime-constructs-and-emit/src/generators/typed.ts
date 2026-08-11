// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function* countGenerator(
  start: number,
  end: number,
): Generator<number, string, string> {
  for (let i = start; i < end; i++) {
    const input: string = yield i;
    if (input === "stop") {
      return "stopped";
    }
  }
  return "done";
}

export function* stringGenerator(): Generator<string, number, unknown> {
  yield "atlas";
  yield "ledger";
  return 42;
}

export function exerciseTypedGenerator(): string {
  const gen = countGenerator(0, 3);
  const first = gen.next();
  const second = gen.next("continue");
  const stopped = gen.next("stop");
  return `${first.value}:${second.value}:${stopped.value}:${stopped.done}`;
}
