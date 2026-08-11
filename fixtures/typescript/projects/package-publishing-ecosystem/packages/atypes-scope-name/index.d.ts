declare module "@scope/name" {
  export function readScoped(value: string): string;
  export interface ScopedMarker {
    source: "scoped-atypes";
  }
}
