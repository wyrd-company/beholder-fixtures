// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * @satisfies {{ label: string; count: number }}
 */
export const jsdocSatisfiesRecord = { label: "atlas", count: 3 };

/**
 * @satisfies {Record<string, string>}
 */
export const jsdocSatisfiesMap = { atlas: "ledger", ledger: "atlas" };

/**
 * JSDoc satisfies preserves literal check while retaining widened contextual type.
 * @satisfies {{ tag: string }}
 */
export const jsdocTagRecord = { tag: "atlas" };

export function consumeJsdocSatisfies(): string {
  return jsdocSatisfiesRecord.label.toUpperCase();
}

export function consumeJsdocMap(): string {
  return jsdocSatisfiesMap.atlas;
}
