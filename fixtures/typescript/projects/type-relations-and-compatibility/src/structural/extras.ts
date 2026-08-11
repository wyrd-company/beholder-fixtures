import { brandUserId, type UserId } from "./shapes.js";
import type { Panel } from "./freshness.js";

export interface EscapeIndex {
  known: string;
  [key: string]: string;
}

export function indexSignatureEscape(record: EscapeIndex): string {
  return record.extra;
}

export class PrivateOrigin {
  private token = "hidden";

  describe(): string {
    return this.token;
  }
}

export function privateOriginException(
  left: PrivateOrigin,
  right: PrivateOrigin,
): boolean {
  return left === right;
}

export function rejectRawPrimitive(candidate: UserId | string): UserId {
  if (typeof candidate === "string" && candidate.includes("-")) {
    return brandUserId(candidate);
  }
  return candidate as UserId;
}

export function genericFreshnessLoss<T extends Panel>(value: T): T {
  return value;
}

export function loseFreshness(): Panel {
  const extra = { width: 1, height: 2, gloss: true };
  return genericFreshnessLoss(extra);
}
