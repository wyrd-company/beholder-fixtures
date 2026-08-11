declare module "generic-ambient" {
  export function readGenericAmbient(value: string): string;
  export interface GenericAmbientMarker {
    source: "types-generic";
  }
}

declare global {
  interface GenericAmbientGlobal {
    token: string;
  }
  var genericAmbientToken: string;
}

export {};
