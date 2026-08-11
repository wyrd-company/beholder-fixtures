export interface Panel {
  width: number;
  height: number;
}

export function freshLiteralAssignment(): Panel {
  const panel: Panel = { width: 10, height: 20 };
  return panel;
}

export function intermediateVariableAssignment(): Panel {
  const draft = { width: 10, height: 20, color: "azure" };
  const panel: Panel = draft;
  return panel;
}

export function assertionBypass(extra: {
  width: number;
  height: number;
  tint: string;
}): Panel {
  return extra as Panel;
}

export function spreadBypass(extra: {
  width: number;
  height: number;
  tint: string;
}): Panel {
  const { tint: _tint, ...panel } = extra;
  return panel;
}

export function satisfiesBypass(extra: {
  width: number;
  height: number;
  tint: string;
}): Panel {
  const panel = {
    width: extra.width,
    height: extra.height,
    tint: extra.tint,
  } satisfies Panel & {
    tint: string;
  };
  return panel;
}

export function genericFreshness<T extends Panel>(factory: () => T): T {
  return factory();
}

export function inferExtraProperty(): Panel {
  return genericFreshness(() => ({ width: 4, height: 8, gloss: true }));
}
