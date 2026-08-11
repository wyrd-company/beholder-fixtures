export interface SpreadSource {
  title: string;
  subtitle?: string;
}

export function spreadOptional(source: SpreadSource): SpreadSource {
  const merged: SpreadSource = { ...source, title: source.title.toUpperCase() };
  return merged;
}

export function spreadWithUndefined(source: SpreadSource): SpreadSource {
  const merged = { ...source, subtitle: undefined };
  return merged;
}
