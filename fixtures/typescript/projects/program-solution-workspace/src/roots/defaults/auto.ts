// Defaults root — included via default discovery when no files/include is specified (tsconfig.roots-defaults.json has no files/include).
export const defaultSeen = "yes";
export function describeDefault(): string {
  return `default:${defaultSeen}`;
}
