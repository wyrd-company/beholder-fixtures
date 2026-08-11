export interface EventEmitter {
  handle(event: string): void;
}

export class EmitterHost implements EventEmitter {
  handle(event: string): void {
    void event;
  }
}

export interface NarrowEventHost {
  handle(event: "click" | "hover"): void;
}

export function bivariantMethod(host: NarrowEventHost): EventEmitter {
  return host;
}

export interface FunctionPropertyHost {
  run: (input: string) => number;
}

export function functionPropertyDeclaration(
  host: FunctionPropertyHost,
): FunctionPropertyHost["run"] {
  return host.run;
}

export function methodVersusProperty(
  emitter: EventEmitter,
  runner: FunctionPropertyHost,
): { method: EventEmitter["handle"]; property: FunctionPropertyHost["run"] } {
  return {
    method: emitter.handle.bind(emitter),
    property: runner.run,
  };
}
