// Empty suffix fallback for moduleSuffixes ["",".ios",".native"] — selected when no platform suffix matches.
export const serviceLabel = "generic";
export function describeService(): string {
  return `service:${serviceLabel}`;
}
