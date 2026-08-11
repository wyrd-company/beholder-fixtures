export type Circle = { kind: "circle"; radius: number };
export type Square = { kind: "square"; edge: number };
export type Shape = Circle | Square;

export function areaTagged(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.edge ** 2;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}

export type TextPayload = { text: string };
export type CountPayload = { count: number };
export type LoosePayload = TextPayload | CountPayload;

export function readLoosePayload(payload: LoosePayload): string | number {
  if ("text" in payload) {
    return payload.text;
  }
  return payload.count;
}

export type OptionalTag = { tag?: "alpha" | "beta"; value: number };
export type MutableTag = { tag: "alpha" | "beta"; value: number };

export function normalizeOptionalTag(record: OptionalTag): number {
  if (record.tag === "alpha") {
    return record.value;
  }
  if (record.tag === "beta") {
    return -record.value;
  }
  return record.value;
}

export function mutateDiscriminant(record: MutableTag): MutableTag {
  record.tag = "beta";
  return record;
}

export type AbsorbingUnion = string | string | number;

export function absorbUnion(value: AbsorbingUnion): string | number {
  return value;
}

export type LiteralUnion = { mode: "on" } | { mode: "off" };

export function literalUnionBranch(record: LiteralUnion): string {
  if (record.mode === "on") {
    return "enabled";
  }
  return "disabled";
}

export type Distributed<T> = T extends string ? `tag:${T}` : never;

export type DistributedSample = Distributed<"alpha" | "beta" | number>;

export function distributeOverUnion(tag: "alpha" | "beta"): DistributedSample {
  const narrowed: Distributed<"alpha" | "beta"> = `tag:${tag}`;
  return narrowed;
}
