// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/// <reference path="./global-script-reader.ts" />

export function readHostGlobals(): {
  counter: number;
  mutable: string;
  frozen: string;
  greeting: string;
  beacon: string;
  mode: HostMode;
  shelf: HostShelf.Slot;
  paneRevision: number;
  describe: string;
  fixtureTag: string;
  importedMarker: HostMarkerToken;
} {
  const scriptGlobals = readHostGlobalsFromScript();
  const mutable = HostMutable;
  const frozen = HostFrozen;
  const greeting = hostGreeting("pane");
  const beacon = new HostBeacon("beacon").ping();
  const mode = HostMode.Active;
  const shelf: HostShelf.Slot = { id: HostShelf.shelfId };
  const paneRevision = window.hostPaneRevision;
  const describe = ({} as object).hostDescribe();
  const fixtureTag = import.meta.hostFixtureTag;

  return {
    counter: scriptGlobals.counter,
    mutable,
    frozen,
    greeting,
    beacon,
    mode,
    shelf,
    paneRevision,
    describe,
    fixtureTag,
    importedMarker: scriptGlobals.importedMarker,
  };
}
