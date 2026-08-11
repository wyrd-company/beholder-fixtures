declare function packValue(value: string): { value: string };

declare const fakeEsm: {
  __esModule: true;
  default: typeof packValue;
  packValue: typeof packValue;
};

export = fakeEsm;
