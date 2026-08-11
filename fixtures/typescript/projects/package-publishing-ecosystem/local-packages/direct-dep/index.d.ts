import type { TransitiveMarker } from "@fixtures/transitive-dep";

export declare function readDirect(value: string): string;
export declare function readTransitive(value: string): string;
export interface DirectMarker {
  source: "direct";
  transitive: TransitiveMarker;
}
