// strictFunctionTypes: method bivariance versus function-property contravariance.
// Method syntax remains bivariant; function-property syntax becomes contravariant under strictFunctionTypes.

export interface MethodHost {
  handle(payload: string): void;
}

export interface FunctionHost {
  handle: (payload: string) => void;
}

export function provideStringHandler(handler: (value: string) => void): void {
  handler("sample");
}

export function provideUnionHandler(handler: (value: "a" | "b") => void): void {
  handler("a");
}

// Valid assignments that remain valid under strictFunctionTypes true:
// - Method host can accept a handler with narrower payload via bivariance.
export const methodHost: MethodHost = {
  handle(payload: string) {
    void payload;
  },
};

// Function-property host requires contravariant-compatible assignment.
// This explicit string handler satisfies contravariance.
export const functionHost: FunctionHost = {
  handle: (payload: string) => {
    void payload;
  },
};

export function acceptsMethodHost(host: MethodHost): void {
  host.handle("token");
}

export function acceptsFunctionHost(host: FunctionHost): void {
  host.handle("token");
}
