// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export async function fetchValue(input: string): Promise<string> {
  return `value:${input}`;
}

export class LedgerService {
  async getEntry(id: string): Promise<{ id: string; label: string }> {
    const value = await fetchValue(id);
    return { id, label: value };
  }

  async failsToFetch(): Promise<string> {
    throw new Error("fetch failed");
  }
}

export async function rejectionDemo(): Promise<string> {
  try {
    await Promise.reject(new Error("rejected"));
    return "unreachable";
  } catch (error) {
    return `caught:${(error as Error).message}`;
  }
}
