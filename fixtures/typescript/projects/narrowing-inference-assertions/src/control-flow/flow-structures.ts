// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function earlyReturnNarrowing(value: string | null | undefined): string {
  if (value === null || value === undefined) {
    return "absent";
  }
  return value.trim().toUpperCase();
}

export function capturedVariableNarrowing(
  values: Array<string | null>,
): string[] {
  let captured = "seed";
  const results: string[] = [];
  for (const value of values) {
    if (value === null) {
      continue;
    }
    captured = value;
    results.push(captured.toUpperCase());
  }
  return results;
}

export function loopNarrowing(
  items: Array<{ kind: "a"; count: number } | { kind: "b"; tag: string }>,
): string[] {
  const output: string[] = [];
  for (const item of items) {
    if (item.kind === "a") {
      output.push(`a:${item.count}`);
    } else {
      output.push(`b:${item.tag}`);
    }
  }

  let index = 0;
  while (index < items.length) {
    const current = items[index];
    if (current.kind === "a") {
      output.push(`loop-a:${current.count}`);
    }
    index += 1;
  }

  return output;
}

export function reachabilityAfterNarrowing(input: string | number): string {
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  return input.toFixed(1);
}
