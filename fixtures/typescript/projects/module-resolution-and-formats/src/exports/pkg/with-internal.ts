// Consumes #internal imports map inside the nested package
import { internalTag } from "#internal";

export const withInternal = internalTag;

export function describeWithInternal(): string {
  return `with-internal:${internalTag}`;
}
