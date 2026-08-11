export declare class SensitiveToken {
  private readonly brand: "v2";
  constructor(value: string);
  getValue(): string;
  getVersion(): 2;
}
export declare const tokenV2: SensitiveToken;
