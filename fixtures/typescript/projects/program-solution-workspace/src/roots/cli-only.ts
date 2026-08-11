// Root selected by command-line argument — not listed in any tsconfig files/include; built via Taskfile cli invocation.
export const cliOnlyValue = "cli";
export function describeCli(): string {
  return `cli:${cliOnlyValue}`;
}
