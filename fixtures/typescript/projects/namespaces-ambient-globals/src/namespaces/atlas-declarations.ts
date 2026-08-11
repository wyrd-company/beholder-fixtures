// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

namespace Atlas {
  export type MarkerOnly = "marker-only";

  export interface LedgerFacet {
    id: string;
  }
}

namespace Atlas {
  export function readMarker(): Atlas.MarkerOnly {
    return "marker-only";
  }
}

export { Atlas };
