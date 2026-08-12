declare namespace JSX {
  interface IntrinsicElements {
    section: { title: string; children?: unknown };
    div: Record<string, unknown>;
  }
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface Element {}
}
