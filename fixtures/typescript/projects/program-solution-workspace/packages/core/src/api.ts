import { hiddenTransform } from "./internal.js";

// Public declaration surface exported across composite boundary.
export type RelayPayload = {
  id: string;
  count: number;
};

export interface RelayResult {
  label: string;
  value: number;
}

// Implementation-only helper change would not alter this .d.ts shape.
export function computeResult(payload: RelayPayload): RelayResult {
  return {
    label: payload.id.toUpperCase(),
    value: hiddenTransform(payload.count),
  };
}

// Public declaration edit — changing this signature alters the emit.
export function formatResult(result: RelayResult): string {
  return `${result.label}:${result.value}`;
}
