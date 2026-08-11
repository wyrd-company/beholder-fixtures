/// <reference lib="es2015.promise" />
/// <reference lib="es2018.asynciterable" />
// Demonstrates syntax lowering across target ES5 vs ES2022.
// Same source emits helper-dispatched code under ES5 and native syntax under ES2022.

export interface ArchiveItem {
  id: string;
  tag?: string;
}

export async function fetchArchiveLabel(
  item: ArchiveItem | null | undefined,
): Promise<string> {
  const label = item?.tag ?? "untagged";
  return label;
}

export function combineLabels(items: ArchiveItem[]): string[] {
  return items.map((item) => item.tag ?? item.id);
}

export function readOptionalChain(
  container: { nested?: { value?: string } } | null,
): string {
  return container?.nested?.value ?? "fallback";
}

export async function loadWithAwait(value: Promise<string>): Promise<string> {
  const resolved = await value;
  return resolved.toUpperCase();
}
