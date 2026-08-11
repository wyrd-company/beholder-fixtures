// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

export type Status = "idle" | "running" | "done";

export enum LedgerState {
  Draft = 0,
  Sealed = 1,
  Archived = 2,
}

export function exhaustiveShape(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return `circle:${shape.radius}`;
    case "square":
      return `square:${shape.side}`;
    case "triangle":
      return `tri:${shape.base}`;
    default: {
      const neverValue: never = shape;
      return `never:${String(neverValue)}`;
    }
  }
}

export function incompleteShape(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return "circle";
    case "square":
      return "square";
    default: {
      const _exhaustive: never = shape as never;
      void _exhaustive;
      return "triangle-or-unknown";
    }
  }
}

export function exhaustiveEnum(state: LedgerState): string {
  switch (state) {
    case LedgerState.Draft:
      return "draft";
    case LedgerState.Sealed:
      return "sealed";
    case LedgerState.Archived:
      return "archived";
    default: {
      const n: never = state;
      return `never:${String(n)}`;
    }
  }
}

export function switchFallthrough(value: number): string {
  let result = "";
  switch (value) {
    case 1:
      result += "one";
    // fallthrough
    case 2:
      result += "two";
      break;
    case 3:
      result += "three";
      break;
    default:
      result += "other";
  }
  return result;
}
