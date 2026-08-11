export function read(value) {
  return `workspace:${value}`;
}
export const marker = "workspace";
export function workspaceOnly(value) {
  return `workspace-only:${value}`;
}
