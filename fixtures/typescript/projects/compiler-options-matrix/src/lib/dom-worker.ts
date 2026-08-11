// DOM and WebWorker lib overlap: lib set includes ["ES2022", "DOM", "WebWorker"].
// Overlapping globals (fetch, Request, Response, structuredClone) are available from either lib,
// while distinct globals (window vs self/DedicatedWorkerGlobalScope) remain separate.

export function fetchWithFallback(url: string): Promise<Response> {
  return fetch(url);
}

export function handleWorkerMessage(event: MessageEvent<string>): string {
  return `worker:${event.data}`;
}

export function describeDomAndWorker(): string {
  const hasWindow = typeof window !== "undefined";
  const hasSelf = typeof self !== "undefined";
  return `window:${hasWindow},self:${hasSelf}`;
}

export function useStructuredClone<T>(value: T): T {
  return structuredClone(value);
}
