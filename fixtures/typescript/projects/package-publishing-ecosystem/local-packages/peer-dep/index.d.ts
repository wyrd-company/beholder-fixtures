import type { TransitiveMarker } from "@fixtures/transitive-dep";

export declare function readPeer(value: string): string;
export interface PeerMarker {
  peer: true;
  transitive: TransitiveMarker;
}
