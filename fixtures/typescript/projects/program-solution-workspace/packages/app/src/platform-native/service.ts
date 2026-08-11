// Empty suffix fallback — generic service when no platform suffix matches.
export const serviceLabel = "generic-native";
export function describeService(): string {
  return `service:${serviceLabel}`;
}
