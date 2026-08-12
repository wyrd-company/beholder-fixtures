// useUnknownInCatchVariables: catch variable is unknown versus any.
// With the flag true, the compiler supplies unknown and requires narrowing;
// with false it supplies any. This file uses unannotated catch variables
// so the option determines the type.

export function parseArchiveJson(input: string): unknown {
  try {
    return JSON.parse(input) as unknown;
  } catch (error) {
    if (error instanceof Error) {
      return `error:${error.message}`;
    }
    return "unknown-error";
  }
}

export function handleCatchWithUnknown(input: string): string {
  try {
    JSON.parse(input);
    return "ok";
  } catch (caught) {
    const message = caught instanceof Error ? caught.message : String(caught);
    return `caught:${message}`;
  }
}
