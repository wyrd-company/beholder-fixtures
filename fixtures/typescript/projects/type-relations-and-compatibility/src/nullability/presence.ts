export interface Profile {
  name: string;
  nickname?: string;
  alias: string | undefined;
}

export function buildProfile(name: string, nickname?: string): Profile {
  return { name, nickname, alias: undefined };
}

export function explicitUndefinedWrite(profile: Profile): Profile {
  return { ...profile, alias: undefined };
}

export function optionalParameter(value?: number): number {
  return value ?? 0;
}

export function defaultParameter(value = 5): number {
  return value;
}

export type OptionalTuple = [string, number?];

export function optionalTupleElement(
  tuple: OptionalTuple,
): string | number | undefined {
  return tuple[1];
}

export function presenceTests(profile: Profile | null | undefined): string {
  if (profile == null) {
    return "missing";
  }
  if (profile.nickname === undefined) {
    return profile.name;
  }
  return `${profile.name} (${profile.nickname})`;
}

export function optionalChaining(
  profile: Profile | null | undefined,
): string | undefined {
  return profile?.nickname?.toUpperCase();
}

export type MappedOptional<T> = {
  [Key in keyof T]?: T[Key];
};

export function mappedOptionalModifier(base: {
  a: number;
  b: string;
}): MappedOptional<typeof base> {
  return { a: base.a };
}
