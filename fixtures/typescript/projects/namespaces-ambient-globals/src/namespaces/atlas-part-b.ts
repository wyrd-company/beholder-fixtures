// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { Atlas } from "./atlas-part-a.js";

declare module "./atlas-part-a.js" {
  namespace Atlas {
    export function label(region: Atlas.Region): string;
  }

  namespace Atlas.Inner {
    export function midpoint(
      left: Atlas.Inner.Coordinate,
      right: Atlas.Inner.Coordinate,
    ): Atlas.Inner.Coordinate;
  }
}

Atlas.label = (region) => `region:${region}`;

Atlas.Inner.midpoint = (left, right) => ({
  x: (left.x + right.x) / 2,
  y: (left.y + right.y) / 2,
});

import InnerPath = Atlas.InnerAlias;

export function describeAtlas(): {
  label: string;
  grid: string;
  midpoint: Atlas.Inner.Coordinate;
} {
  const label = Atlas.label(Atlas.regionCode);
  const grid = InnerPath.readGrid();
  const midpoint = Atlas.Inner.midpoint({ x: 0, y: 0 }, { x: 4, y: 6 });

  return { label, grid, midpoint };
}
