// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Legacy parameter decorators and design:paramtypes.
 * Parameter decorators are valid only under experimentalDecorators.
 */

export const legacyParamLog: string[] = [];

function required(
  target: Object,
  propertyKey: string | symbol | undefined,
  parameterIndex: number,
): void {
  legacyParamLog.push(
    `required:${String(propertyKey ?? "constructor")}:${parameterIndex}`,
  );
}

function inject(token: string) {
  return function (
    target: Object,
    propertyKey: string | symbol | undefined,
    parameterIndex: number,
  ): void {
    legacyParamLog.push(
      `inject:${token}:${String(propertyKey ?? "constructor")}:${parameterIndex}`,
    );
  };
}

function loggedParam(
  target: Object,
  propertyKey: string | symbol | undefined,
  parameterIndex: number,
): void {
  legacyParamLog.push(
    `loggedParam:${String(propertyKey ?? "constructor")}:${parameterIndex}`,
  );
}

import { CatalogItem, LedgerEntry } from "./catalog-item.js";

export class ParamGallery {
  constructor(
    @inject("CatalogItem") public readonly item: CatalogItem,
    @required public readonly count: number,
    @inject("LedgerEntry") public readonly entry: LedgerEntry,
  ) {}

  handle(
    @required value: string,
    @inject("trace") @loggedParam traceId: string,
  ): string {
    return `${value}:${traceId}:${this.count}`;
  }

  static build(
    @required label: string,
    @inject("count") count: number,
  ): ParamGallery {
    return new ParamGallery(
      new CatalogItem("sku-1", "sample"),
      count,
      new LedgerEntry("e1", 100),
    );
  }
}

export function getLegacyParamLog(): string[] {
  return [...legacyParamLog];
}
