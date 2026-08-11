// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function demonstrateBindings(
  input: { items: string[]; count?: number } = { items: ["a"] },
): string {
  var sharedCounter = 0;
  var sharedCounter = 1;

  let blockScoped = "outer";

  {
    let blockScoped = "inner";
    const frozen = 10;
    void frozen;
    void blockScoped;
  }

  function innerHelper(
    first: string,
    second = "fallback",
    ...rest: string[]
  ): string {
    return [first, second, ...rest].join("-");
  }

  class LocalToken {
    readonly value: string;
    constructor(value: string) {
      this.value = value;
    }
  }

  const token = new LocalToken("token");
  let captured = "";

  for (const item of input.items) {
    const alias = item;
    captured = innerHelper(alias, String(input.count ?? 0));
    sharedCounter += 1;
  }

  try {
    throw new Error("sample");
  } catch (error) {
    const message = error instanceof Error ? error.message : "unknown";
    return `${token.value}:${captured}:${message}:${sharedCounter}`;
  }
}

export function demonstrateDestructuring({
  pair: { left, right: aliasRight = 2, ...remaining } = {
    left: 1,
    right: 2,
    extra: 0,
  },
}: {
  pair: { left: number; right?: number; extra?: number };
}): { head: string; tailSum: number } {
  const tailSum = left + aliasRight + (remaining.extra ?? 0);

  return { head: `pair-${left}`, tailSum };
}

export function demonstrateSwitchScope(value: number): string {
  let outcome = "none";

  switch (value) {
    case 1:
    case 2:
      const sharedTag = value === 1 ? "one" : "two";
      outcome = sharedTag;
      break;
    default:
      outcome = "other";
  }

  return outcome;
}

export function captureInClosure(): number[] {
  const results: number[] = [];

  for (let index = 0; index < 3; index += 1) {
    results.push(
      (function () {
        return index;
      })(),
    );
  }

  return results;
}
