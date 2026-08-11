export interface VersionedMarker {
  version: "v4";
  legacy: true;
}
export declare function readVersioned(): VersionedMarker;
