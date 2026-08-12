// strictFunctionTypes: method bivariance versus function-property contravariance.
// Method syntax remains bivariant; function-property syntax becomes contravariant under strictFunctionTypes.

export interface MethodHost {
  handle(payload: string): void;
}

export interface FunctionHost {
  handle: (payload: string) => void;
}

type NarrowPayload = "a";
type BroadPayload = string | number;

declare const narrowHandler: (payload: NarrowPayload) => void;
declare const broadHandler: (payload: BroadPayload) => void;
declare const exactHandler: (payload: string) => void;

// Method host is bivariant: accepts narrower payload handler.
export const methodHostWithNarrow: MethodHost = {
  handle: narrowHandler,
};

// Method host also accepts exact handler.
export const methodHostWithExact: MethodHost = {
  handle: exactHandler,
};

// Function-property host is contravariant under strictFunctionTypes:
// it accepts broader payload handler (string | number) but not narrower.
// Broad assignment is valid; narrow would be an error if assigned to FunctionHost.
export const functionHostWithBroad: FunctionHost = {
  handle: broadHandler,
};

export const functionHostWithExact: FunctionHost = {
  handle: exactHandler,
};

export function acceptsMethodHost(host: MethodHost): void {
  host.handle("token");
}

export function acceptsFunctionHost(host: FunctionHost): void {
  host.handle("token");
}
