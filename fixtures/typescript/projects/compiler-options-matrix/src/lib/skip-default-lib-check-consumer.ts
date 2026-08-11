// skipDefaultLibCheck: tsconfig has skipDefaultLibCheck true with skipLibCheck true.
// Default lib bodies are not checked, while project source and non-default declarations remain checked.

export interface ArchiveDescriptor {
  id: string;
  title: string;
}

export function describeArchive(descriptor: ArchiveDescriptor): string {
  return `${descriptor.id}:${descriptor.title}`;
}

export function useDomApiWithSkipCheck(node: Element): string {
  return node.getAttribute("data-token") ?? "missing";
}
