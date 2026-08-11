// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-080: function-reflection, this utilities, applied to overloads, optional properties, any, never

export function sampleBeacon(label: string, count?: number): string {
  return `${label}:${count ?? 0}`;
}

export function reflectedOverloaded(value: string): number;
export function reflectedOverloaded(value: number): string;
export function reflectedOverloaded(value: string | number): string | number {
  return typeof value === "string" ? value.length : String(value);
}

// Parameters, ReturnType
export type SampleParams = Parameters<typeof sampleBeacon>; // [string, number?]
export type SampleReturn = ReturnType<typeof sampleBeacon>; // string

// Last-overload extraction via conditional infer (last signature wins)
export type ReflectedLastOverloadReturn<T> = T extends {
  (...args: infer _A): infer R;
}
  ? R
  : never;

export type ReflectedOverloadedLastReturn = ReflectedLastOverloadReturn<
  typeof reflectedOverloaded
>; // string (last overload)

// ConstructorParameters, InstanceType
export class ReflectHarbor {
  constructor(
    public label: string,
    public count: number,
  ) {}
}

export type ReflectHarborParams = ConstructorParameters<typeof ReflectHarbor>; // [string, number]
export type ReflectHarborInstance = InstanceType<typeof ReflectHarbor>;

// ThisParameterType, OmitThisParameter
export function withThis(this: { label: string }, value: string): string {
  return `${this.label}:${value}`;
}

export type ThisParam = ThisParameterType<typeof withThis>; // { label: string }
export type WithoutThis = OmitThisParameter<typeof withThis>; // (value: string) => string

// ThisType for contextual this
export type HarborThis = ThisType<{ label: string }>;

export const paramsExample: SampleParams = ["atlas", 3];
export const reflectHarborInstance: ReflectHarborInstance = new ReflectHarbor(
  "atlas",
  3,
);

// Applied to any and never
export type ParamsAny = Parameters<any>; // any
export type ReturnNever = ReturnType<never>; // never (via conditional)
export type AwaitedAny = Awaited<any>; // any
export type AwaitedNever = Awaited<never>; // never
