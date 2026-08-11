// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Explicit this parameters, this: void, and callback receiver declarations. */

export function forEachWithThis(
  this: void,
  items: string[],
  cb: (this: void, item: string) => void,
): void {
  for (const item of items) cb(item);
}

export function greet(this: { label: string }, suffix: string): string {
  return `${this.label}:${suffix}`;
}

export interface ReceiverHost {
  label: string;
  run(cb: (this: ReceiverHost) => string): string;
}

export class ReceiverHostImpl implements ReceiverHost {
  label = "host";
  run(cb: (this: ReceiverHost) => string): string {
    return cb.call(this);
  }
}

export function exerciseThisParameters(): void {
  // this: void ensures no this is used inside; valid under noImplicitThis
  forEachWithThis(["a", "b"], function (item) {
    void item;
  });

  const obj = { label: "node" };
  const result: string = greet.call(obj, "ok");
  // greet.call with wrong this type would be rejected; valid call above proves checking.

  const host = new ReceiverHostImpl();
  const fromCallback: string = host.run(function (this: ReceiverHost) {
    return this.label;
  });
  void result;
  void fromCallback;
}
