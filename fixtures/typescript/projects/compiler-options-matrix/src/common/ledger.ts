export interface LedgerEntry {
  token: string;
  amount: number;
  note?: string;
}

export function summarizeEntries(entries: LedgerEntry[]): number {
  return entries.reduce((sum, entry) => sum + entry.amount, 0);
}

export function formatEntry(entry: LedgerEntry): string {
  return `${entry.token}=${entry.amount}${entry.note ? `:${entry.note}` : ""}`;
}
