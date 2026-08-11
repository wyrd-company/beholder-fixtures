// Genuinely unreachable file within core — excluded from its composite program and never imported.
export type OrphanSignal = {
  trace: string;
};

export function emitOrphan(signal: OrphanSignal): string {
  return `orphan:${signal.trace}`;
}
