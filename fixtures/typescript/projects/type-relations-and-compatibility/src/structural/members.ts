export interface CallableSurface {
  (input: string): number;
}

export interface ConstructibleSurface {
  new (seed: number): ConstructedSurface;
}

export interface ConstructedSurface {
  optional?: number;
}

export interface IndexedSurface {
  [key: string]: string | number | boolean | undefined;
}

export interface CapabilitySurface
  extends CallableSurface,
    ConstructibleSurface,
    IndexedSurface {
  required: string;
  optional?: number;
  readonly frozen: boolean;
}

export class CapabilityHost implements ConstructedSurface {
  readonly frozen = true;
  required = "host";
  optional?: number;

  constructor(public seed: number) {}
}

export function makeCapability(seed: number): CapabilitySurface {
  const callable = ((input: string) =>
    input.length + seed) as CapabilitySurface;
  callable.required = "host";
  callable.optional = seed;
  callable[seed.toString()] = seed;
  return callable;
}

export function useCapability(surface: CapabilitySurface): number {
  const created = new surface(3);
  return surface("lane") + (created.optional ?? 0);
}

export type MutableFlags = {
  -readonly [Key in "alpha" | "beta"]: boolean;
};

export type ReadonlyFlags = {
  readonly [Key in "alpha" | "beta"]: boolean;
};

export function mappedModifierRoundTrip(flags: ReadonlyFlags): MutableFlags {
  const mutable: MutableFlags = { alpha: flags.alpha, beta: flags.beta };
  const locked: ReadonlyFlags = { alpha: mutable.alpha, beta: mutable.beta };
  return { alpha: locked.alpha, beta: locked.beta };
}
