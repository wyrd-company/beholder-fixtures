export interface VersionedMarker {
  version: "fallback";
  legacy: true;
}
export declare function readVersioned(): VersionedMarker;
