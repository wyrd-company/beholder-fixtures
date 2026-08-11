// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare var HostCounter: number;
declare let HostMutable: string;
declare const HostFrozen: string;

declare function hostGreeting(name: string): string;

declare class HostBeacon {
  constructor(token: string);
  readonly token: string;
  ping(): string;
}

declare enum HostMode {
  Idle = "idle",
  Active = "active",
}

declare namespace HostShelf {
  export const shelfId: string;
  export type Slot = { id: string };
}

declare const HostImportedMarker: import("./host-marker-module.js").HostMarkerToken;

type HostMarkerToken = import("./host-marker-module.js").HostMarkerToken;

declare interface HostBeacon {
  ping(): string;
}

interface Window {
  hostPaneRevision: number;
}

interface Object {
  hostDescribe(this: object): string;
}

interface ImportMeta {
  hostFixtureTag: string;
}
