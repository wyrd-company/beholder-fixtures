// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function connect(endpoint: string): string {
  return `connected:${endpoint}`;
}

export namespace connect {
  export function retry(endpoint: string, attempts: number): string {
    return `retry:${endpoint}:${attempts}`;
  }

  export type Options = {
    timeoutMs: number;
  };
}

export class Vector {
  x = 0;
}

export namespace Vector {
  export function zero(): Vector {
    return new Vector();
  }
}

export interface Vector {
  y: number;
}

export enum Palette {
  Warm,
}

export enum Palette {
  Cool = 2,
}

export namespace Palette {
  export function label(value: Palette): string {
    return value === Palette.Warm ? "warm" : "cool";
  }
}

function helper(value: number): number {
  return value + 1;
}

namespace helper {
  export type Transform = (value: number) => number;
  export const identity: Transform = (value) => value;
}

namespace exportedFacet {
  export const visible = "exported";
  const hidden = "block-private";

  export function readPrivate(): string {
    return hidden;
  }
}

namespace exportedFacet {
  export function readSummary(): string {
    return `${visible}:${readPrivate()}`;
  }
}

export function demonstrateCrossKind(): {
  connection: string;
  retried: string;
  point: Vector;
  paletteValue: number;
  paletteLabel: string;
  transformed: number;
  exportedMember: string;
  privateMember: string;
  summaryMember: string;
} {
  const connection = connect("api");
  const retried = connect.retry("api", 2);
  const point = Vector.zero();
  point.y = 5;

  const paletteValue = Palette.Cool;
  const paletteLabel = Palette.label(paletteValue);
  const transformed = helper(4);

  return {
    connection,
    retried,
    point,
    paletteValue,
    paletteLabel,
    transformed,
    exportedMember: exportedFacet.visible,
    privateMember: exportedFacet.readPrivate(),
    summaryMember: exportedFacet.readSummary(),
  };
}

export { helper };
