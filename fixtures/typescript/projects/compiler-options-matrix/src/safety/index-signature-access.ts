// noPropertyAccessFromIndexSignature: dot access on index signature is gated.
// With flag true, bracket access is required; dot access is valid only when flag is off.

export interface IndexCatalog {
  [key: string]: string;
}

export function readViaBracket(catalog: IndexCatalog, key: string): string {
  return catalog[key];
}

export function writeViaBracket(
  catalog: IndexCatalog,
  key: string,
  value: string,
): void {
  catalog[key] = value;
}

export function readKnownBracket(catalog: IndexCatalog): string {
  return catalog["known"];
}

// This file satisfies the flag by using bracket access; under lax mode dot access would also be valid
// but is not used here so the file remains valid in both modes while demonstrating the required style.
