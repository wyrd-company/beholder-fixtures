// import.meta is valid in ESM contexts (nodenext / bundler / preserve)
export const metaUrl: string = import.meta.url;

export function describeMeta(): string {
  return `meta:${metaUrl}`;
}
