export class SensitiveToken {
  constructor(value) {
    this.value = value;
    this.brand = "v2";
  }
  getValue() {
    return this.value;
  }
  getVersion() {
    return 2;
  }
}
export const tokenV2 = new SensitiveToken("v2");
