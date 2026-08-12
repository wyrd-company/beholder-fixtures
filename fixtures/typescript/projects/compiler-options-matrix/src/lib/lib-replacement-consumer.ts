// libReplacement: tsconfig has libReplacement true with WebWorker.
// The bundled webworker lib is replaced by @typescript/lib-webworker.

export function readWorkerMarker(scope: DedicatedWorkerGlobalScope): string {
  return scope.replacementWorkerMarker;
}

export function describeWorkerScope(scope: DedicatedWorkerGlobalScope): string {
  return `worker:${scope.replacementWorkerMarker}`;
}
