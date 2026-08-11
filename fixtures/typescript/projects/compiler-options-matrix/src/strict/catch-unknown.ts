// useUnknownInCatchVariables: catch variable is unknown versus any.
// With the flag true, catch variable is unknown and requires narrowing;
// with false it is any. Valid handling uses narrowing that satisfies both.

export function parseArchiveJson(input: string): unknown {
  try {
    return JSON.parse(input) as unknown;
  } catch (error: unknown) {
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
  } catch (caught: unknown) {
    const message = caught instanceof Error ? caught.message : String(caught);
    return `caught:${message}`;
  }
}
