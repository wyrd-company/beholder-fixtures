/// <reference no-default-lib="true"/>
/// <reference lib="es5" />
/// <reference lib="es2015.collection" />
/// <reference lib="es2015.iterable" />
/// <reference lib="es2022" />
/// <reference lib="dom" />

// noLib: project has noLib true and supplies needed libs via per-file references.
// Only the referenced libs are available; default lib set is not injected.

export function createElementWithText(tag: string, text: string): Element {
  const element = document.createElement(tag);
  element.textContent = text;
  return element;
}

export function sumValues(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0);
}

export function describeNoLibToken(token: string): string {
  return `no-lib:${token}`;
}
