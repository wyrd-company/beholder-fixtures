// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard decorator ordering and Symbol.metadata coverage.
 * Ordering is evaluated bottom-up at application time and left-to-right
 * for initializers where specified by the spec.
 */

export const orderingLog: string[] = [];
export const metadataLog: string[] = [];

function orderTag(tag: string) {
  return function (value: any, context: unknown): any {
    const ctx = context as {
      name?: string | symbol;
      kind: string;
      addInitializer(fn: () => void): void;
    };
    orderingLog.push(`apply:${tag}:${String(ctx.name ?? "class")}:${ctx.kind}`);
    ctx.addInitializer(function (this: unknown) {
      orderingLog.push(
        `init:${tag}:${String(ctx.name ?? "class")}:${ctx.kind}`,
      );
    });
    return value;
  };
}

function metaTag(key: string, value: unknown) {
  return function (target: any, context: unknown): any {
    const ctx = context as {
      name?: string | symbol;
      metadata: Record<string, unknown>;
    };
    if (ctx.metadata) ctx.metadata[key] = value;
    metadataLog.push(
      `meta:${String(ctx.name ?? "class")}:${key}=${String(value)}`,
    );
    return target;
  };
}

@orderTag("class-outer")
@orderTag("class-inner")
@metaTag("classMeta", "root")
export class OrderedAndTagged {
  @orderTag("field-outer")
  @orderTag("field-inner")
  @metaTag("fieldMeta", 1)
  field = 1;

  @orderTag("method-outer")
  @orderTag("method-inner")
  method(): string {
    return "method";
  }

  @orderTag("accessor-outer")
  @orderTag("accessor-inner")
  accessor entry = "entry";

  @orderTag("getter-outer")
  @orderTag("getter-inner")
  get label(): string {
    return "label";
  }

  @orderTag("setter-outer")
  @orderTag("setter-inner")
  set label(value: string) {
    void value;
  }

  @orderTag("static-field-outer")
  @orderTag("static-field-inner")
  static staticField = 2;

  @orderTag("static-method-outer")
  @orderTag("static-method-inner")
  static staticMethod(): void {}
}

export function getOrderingLog(): string[] {
  return [...orderingLog];
}

export function getMetadataLog(): string[] {
  return [...metadataLog];
}

export function readOrderedMetadata(): unknown {
  return (OrderedAndTagged as unknown as Record<symbol, unknown>)[
    Symbol.metadata
  ];
}

export function hasSymbolMetadata(): boolean {
  return (
    typeof Symbol !== "undefined" &&
    typeof (Symbol as unknown as Record<string, symbol>).metadata === "symbol"
  );
}
