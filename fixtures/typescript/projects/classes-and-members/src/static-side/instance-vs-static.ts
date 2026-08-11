// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Instance type `C` versus static `typeof C` and InstanceType utility. */
export class Widget {
  instanceTag = "widget";
  static kind = "widget-kind";
  static create(): Widget {
    return new Widget();
  }
}

// Instance type C
export type WidgetInstance = Widget;
// Static side typeof C
export type WidgetStatic = typeof Widget;
// InstanceType extracts instance from static
export type WidgetViaInstanceType = InstanceType<typeof Widget>;

export function consumeInstance(w: Widget): string {
  return w.instanceTag;
}
export function consumeStatic(ctor: typeof Widget): string {
  return ctor.kind;
}

export function exerciseInstanceVsStatic(): void {
  const w: Widget = new Widget();
  const w2: WidgetInstance = w;
  void w2;

  const ctor: WidgetStatic = Widget;
  const w3: WidgetViaInstanceType = new ctor();
  void w3;

  void consumeInstance(w);
  void consumeStatic(Widget);

  // Generic type param unavailable to statics – comment the restriction:
  // class GenericBox<T> { static bad: T; } would be invalid. Not included.
}
