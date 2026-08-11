// Inside package with "type": "module" — .js is ESM, .ts nearest lookup is ESM
export const esmValue = "esm-type-esm";

export const esmMeta = import.meta.url;

export function describeEsm(): string {
  return esmValue;
}
