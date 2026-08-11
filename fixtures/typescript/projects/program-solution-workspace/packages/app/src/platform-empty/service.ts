// Empty suffix only — selected when .ios and .native are absent.
export const serviceLabel = "generic-empty";
export function describeService(): string {
  return `service:${serviceLabel}`;
}
