// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const topLevelValue = await Promise.resolve("top-level");

export async function getTopLevel(): Promise<string> {
  return topLevelValue;
}
