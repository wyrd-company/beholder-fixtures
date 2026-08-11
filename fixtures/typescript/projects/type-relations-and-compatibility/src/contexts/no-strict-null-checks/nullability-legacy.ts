export interface LegacyProfile {
  name: string;
  nickname?: string;
}

export function legacyPresence(
  profile: LegacyProfile | null | undefined,
): string {
  if (profile == null) {
    return "missing";
  }
  return profile.nickname ?? profile.name;
}

export function legacyCollapse(value: string | null | undefined): string {
  const collapsed: string = value;
  return collapsed ?? "fallback";
}

export function legacyOptionalParameter(value?: number): number {
  return value ?? 0;
}

export function legacyDefaultParameter(value = 3): number {
  return value;
}

export type LegacyOptionalTuple = [string, number?];

export function legacyOptionalTuple(
  tuple: LegacyOptionalTuple,
): number | string {
  const second = tuple[1];
  return second === undefined ? tuple[0] : second;
}

export function legacyUndefinedWrite(profile: LegacyProfile): LegacyProfile {
  return { name: profile.name, nickname: undefined };
}
