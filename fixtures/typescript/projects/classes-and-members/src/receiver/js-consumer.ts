// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { JsBox } from "./js-constructor.js";

/** Consume the JS constructor function and demonstrate static versus instance this. */
export function exerciseJsConstructor(): void {
  const box = new (JsBox as unknown as new (name: string) => {
    name: string;
    describe(): string;
  })("alpha");
  void box.describe();
}

export class StaticVsInstance {
  instanceLabel = "instance";

  static staticLabel = "static";

  instanceMethod(): string {
    // `this` here is the instance
    return this.instanceLabel;
  }

  static staticMethod(this: typeof StaticVsInstance): string {
    // `this` here is the static side (the constructor)
    return this.staticLabel;
  }

  static describeStaticThis(): string {
    return this.staticLabel;
  }
}

export function exerciseStaticVsInstanceThis(): void {
  const obj = new StaticVsInstance();
  const inst: string = obj.instanceMethod();
  const stat: string = StaticVsInstance.staticMethod();
  const stat2: string = StaticVsInstance.describeStaticThis();
  void inst;
  void stat;
  void stat2;
}
