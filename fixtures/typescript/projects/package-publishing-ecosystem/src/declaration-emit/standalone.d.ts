// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface StandaloneBeacon {
  beaconId: string;
  revision: number;
}

export declare function readStandalone(beacon: StandaloneBeacon): string;
