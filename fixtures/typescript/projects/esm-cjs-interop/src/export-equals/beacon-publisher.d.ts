// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

declare function Beacon(this: { signal: string }): void;

declare namespace Beacon {
  function pulse(): string;
}

export = Beacon;
