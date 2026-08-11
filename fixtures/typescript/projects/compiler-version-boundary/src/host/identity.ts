// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Host identity is part of program identity. The corpus default host is
// Node.js on 64-bit x86 Linux with the pinned TypeScript toolchain. This module
// surfaces host observables without affecting the boundary inference.

export const hostKind = "node" as const;

declare const process: {
  platform: string;
  arch: string;
  version: string;
};

export function getHostIdentity() {
  return {
    runtime: hostKind,
    platform: process.platform,
    arch: process.arch,
    nodeVersion: process.version,
  };
}

export function getCompilerHostProbe(): string {
  return `${hostKind}:${process.platform}:${process.arch}:${process.version}`;
}
