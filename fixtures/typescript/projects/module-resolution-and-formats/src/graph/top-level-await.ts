// Top-level await (valid under bundler / nodenext with esnext target)
export const ready = await Promise.resolve("awaited");

export async function getReady(): Promise<string> {
  return ready;
}
