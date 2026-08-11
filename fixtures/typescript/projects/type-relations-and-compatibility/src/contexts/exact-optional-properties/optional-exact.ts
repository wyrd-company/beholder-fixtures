export interface ExactProfile {
  name: string;
  nickname?: string;
  alias?: string;
}

export function exactOptionalAssignment(): ExactProfile {
  const withMissing: ExactProfile = { name: "anchor" };
  const withPresent: ExactProfile = { name: "anchor", nickname: "north" };
  return withPresent ?? withMissing;
}

export function exactUndefinedWrite(profile: ExactProfile): ExactProfile {
  const next: ExactProfile = { name: profile.name };
  if (profile.nickname !== undefined) {
    next.nickname = profile.nickname;
  }
  return next;
}

export interface ExactSpreadSource {
  title: string;
  subtitle?: string;
}

export function exactSpreadOptional(
  source: ExactSpreadSource,
): ExactSpreadSource {
  return { ...source };
}

export type ExactMappedOptional<T> = {
  [Key in keyof T]?: T[Key];
};

export function exactMappedOptional(base: {
  a: number;
  b: string;
}): ExactMappedOptional<typeof base> {
  return { b: base.b };
}

export interface ExactWeakTarget {
  theme?: string;
  density?: number;
}

export function exactWeakTarget(candidate: ExactWeakTarget): ExactWeakTarget {
  return candidate;
}

export interface ExactOptionalNote {
  title: string;
  subtitle?: string;
}

export function exactExplicitUndefinedWrite(
  profile: ExactOptionalWithUndefined,
): ExactOptionalWithUndefined {
  return { subtitle: undefined };
}

export interface ExactOptionalWithUndefined {
  subtitle?: string | undefined;
}
