/// <reference lib="es2020.promise" />
/// <reference lib="es2020.string" />
/// <reference lib="dom" />

// Per-file lib augmentation via triple-slash reference lib.
// This file brings Promise and modern string APIs without relying on the project lib set.

export function waitForLabel(label: string): Promise<string> {
  return Promise.resolve(label);
}

export function checkIncludes(source: string, search: string): boolean {
  return source.includes(search);
}

export function readDomNodeText(node: Element): string {
  return node.textContent ?? "";
}
