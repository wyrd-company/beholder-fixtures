// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Ambient overloads without implementation. */
export declare function ambientRender(value: string): string;
export declare function ambientRender(value: number): number;
export declare function ambientRender(value: string, tag: string): string;

export declare function ambientJoin(a: string, b: string): string;
export declare function ambientJoin(
  a: string,
  b: string,
  ...rest: string[]
): string;
