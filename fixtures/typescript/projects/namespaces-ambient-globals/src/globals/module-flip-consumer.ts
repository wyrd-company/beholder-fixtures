// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function readHostFromModule(): HostMode {
  return HostMode.Active;
}

declare global {
  interface ModuleHostMarker {
    scope: "module-global-augment";
  }
}

export function readModuleHostMarker(): ModuleHostMarker {
  return { scope: "module-global-augment" };
}
