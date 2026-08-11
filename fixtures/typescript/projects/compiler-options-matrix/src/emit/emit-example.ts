export interface EmitSample {
  id: string;
  value: number;
}

export function createEmitSample(id: string, value: number): EmitSample {
  return { id, value };
}

export function describeEmitSample(sample: EmitSample): string {
  return `${sample.id}:${sample.value}`;
}

export const emitMarker = "emit-valid";
