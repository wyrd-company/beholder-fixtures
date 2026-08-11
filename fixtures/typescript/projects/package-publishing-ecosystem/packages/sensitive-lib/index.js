export class SensitiveToken {
  constructor(value) {
    this.value = value;
    this.brand = "v1";
  }
  getValue() {
    return this.value;
  }
}
export const tokenV1 = new SensitiveToken("v1");
