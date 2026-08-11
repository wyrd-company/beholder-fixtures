// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const constValue = "atlas";

export let letValue = "atlas";

export const constAssertionValue = "atlas" as const;

export const annotatedValue: string = "atlas";

export const readonlyContainer: { readonly label: "atlas" } = {
  label: "atlas",
};

export function wideningContrast(): {
  letKind: string;
  constKind: string;
  assertionKind: string;
  annotatedKind: string;
  readonlyKind: string;
} {
  let localLet = "atlas";
  const localConst = "atlas";
  const localAssertion = "atlas" as const;
  const localAnnotated: string = "atlas";
  const localReadonly = { label: "atlas" } as const;

  localLet = "ledger";

  return {
    letKind: localLet,
    constKind: localConst,
    assertionKind: localAssertion,
    annotatedKind: localAnnotated,
    readonlyKind: localReadonly.label,
  };
}

export function letVsConstAssignment(): string {
  let dynamic = "seed";
  const fixed = "atlas";
  dynamic = "ledger";
  return `${dynamic}:${fixed}`;
}

export function constAssertionPreservesLiteral(): "atlas" {
  const token = "atlas" as const;
  return token;
}

export function readonlyPropertyRetainsLiteral(): string {
  const holder: { readonly label: "atlas" } = { label: "atlas" };
  return holder.label;
}
