// noFallthroughCasesInSwitch: switch fallthrough is gated. Valid file has no fallthrough.

export type CrateSize = "small" | "medium" | "large";

export function describeSize(size: CrateSize): string {
  switch (size) {
    case "small":
      return "S";
    case "medium":
      return "M";
    case "large":
      return "L";
  }
}

export function handleSize(size: CrateSize): number {
  switch (size) {
    case "small":
      return 1;
    case "medium":
      return 2;
    case "large":
      return 3;
  }
}
