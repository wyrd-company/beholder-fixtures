export type PermissiveBroad = (value: string | number) => void;
export type PermissiveNarrow = (value: string) => void;

export function permissiveBroaderParameter(
  handler: PermissiveBroad,
): PermissiveNarrow {
  return handler;
}

export type PermissiveMethodHost = {
  handle(event: string): void;
};

export function permissiveBivariantMethod(host: PermissiveMethodHost): {
  handle(event: string | number): void;
} {
  return host;
}

export interface PermissivePropertyHost {
  onEvent: (detail: string) => void;
}

export function permissiveContravariantProperty(host: PermissivePropertyHost): {
  onEvent: (detail: string | number) => void;
} {
  return host;
}

export type PermissiveReturning = (input: string) => number;
export type PermissiveVoidTarget = (input: string) => void;

export function permissiveDiscardReturn(
  handler: PermissiveReturning,
): PermissiveVoidTarget {
  return handler;
}

export function permissiveGenericCallback<T>(
  value: T,
  project: (item: T) => string,
): string {
  return project(value);
}
