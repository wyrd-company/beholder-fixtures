// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { Labeled, Sized } from "./record-base.js";

declare module "./record-base.js" {
  interface RecordShape {
    revision: number;
  }
}

import type { RecordShape } from "./record-base.js";

export interface CompositeRecord extends RecordShape, Sized, Labeled {
  format(value: string): string;
}

export interface CompositeRecord {
  format(value: number): number;
  describe(): string;
  tag(value: "draft"): "DRAFT";
}

export interface CompositeRecord {
  tag(value: "final"): "FINAL";
}

export class CompositeRecordImpl implements CompositeRecord {
  id = "rec-1";
  revision = 1;
  width = 10;
  height = 20;
  label = "sample";

  format(value: string): string;
  format(value: number): number;
  format(value: string | number): string | number {
    return typeof value === "string" ? value.toUpperCase() : value * 2;
  }

  describe(): string {
    return `${this.label}:${this.id}`;
  }

  tag(value: "draft"): "DRAFT";
  tag(value: "final"): "FINAL";
  tag(value: "draft" | "final"): "DRAFT" | "FINAL" {
    return value === "draft" ? "DRAFT" : "FINAL";
  }
}

export function formatLiteral(record: CompositeRecord, value: "draft"): "DRAFT";
export function formatLiteral(record: CompositeRecord, value: "final"): "FINAL";
export function formatLiteral(
  record: CompositeRecord,
  value: "draft" | "final",
): "DRAFT" | "FINAL" {
  if (value === "draft") {
    return record.tag("draft");
  }

  return record.tag("final");
}
