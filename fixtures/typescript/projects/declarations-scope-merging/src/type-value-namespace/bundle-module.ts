// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface BundleOptions {
  size: number;
}

export class Bundle {
  constructor(public options: BundleOptions) {}
}

export enum BundleKind {
  Flat = 0,
  Nested = 1,
}

export namespace Bundle {
  export function flatten(options: BundleOptions): BundleOptions {
    return { size: options.size };
  }
}

export function createBundle(options: BundleOptions): Bundle {
  return new Bundle(options);
}
