export interface Named {
  label: string;
}

export interface Sized {
  size: number;
}

export type NamedAndSized = Named & Sized;

export function intersectObjects(left: Named, right: Sized): NamedAndSized {
  return { ...left, ...right };
}

export interface Callable {
  (input: string): number;
}

export interface Described {
  describe(): string;
}

export type CallableAndDescribed = Callable & Described;

export function intersectCallables(
  call: Callable,
  described: Described,
): CallableAndDescribed {
  const merged = Object.assign(call, described);
  return merged as CallableAndDescribed;
}

export type Contradictory = { mode: "on" } & { mode: "off" };
export type ContradictoryMode = Contradictory["mode"];

export function impossibleIntersection(): ContradictoryMode {
  const mode = "on" as ContradictoryMode;
  return mode;
}

export type CollapsedIntersection = string & number;

export function collapsedToNever(): CollapsedIntersection {
  const value = undefined as unknown as CollapsedIntersection;
  return value;
}
