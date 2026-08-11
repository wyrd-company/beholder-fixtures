// Inside package with "type": "commonjs" — .js is CJS, nearest lookup is CJS
export const cjsValue = "cjs-type-cjs";

export function describeCjs(): string {
  return cjsValue;
}
