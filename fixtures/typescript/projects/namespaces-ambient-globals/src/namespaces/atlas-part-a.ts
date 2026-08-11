// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

namespace Atlas {
  export const regionCode = "north";

  export namespace Inner {
    export type Coordinate = { x: number; y: number };
    const hiddenGrid = "grid-secret";

    export function readGrid(): string {
      return hiddenGrid;
    }
  }

  export type Region = typeof regionCode;

  export import InnerAlias = Atlas.Inner;
}

export { Atlas };
