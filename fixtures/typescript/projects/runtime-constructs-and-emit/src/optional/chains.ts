// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type Profile = {
  name?: string;
  address?: { city?: string; code?: string };
  getLabel?(): string;
  tags?: string[];
  nested?: { value?: string };
};

export function optionalProperty(profile?: Profile): string | undefined {
  return profile?.name;
}

export function optionalElement(
  profile: Profile | undefined,
  key: string,
): unknown {
  return (profile as Record<string, unknown>)?.[key];
}

export function optionalCall(profile?: Profile): string | undefined {
  return profile?.getLabel?.();
}

export function receiverPreservingCall(
  container: { handler?: { run: () => string } } | undefined,
): string | undefined {
  return container?.handler?.run();
}

export class Counter {
  count = 0;
  inc(): number {
    this.count += 1;
    return this.count;
  }
}

export function optionalMethodPreservesReceiver(
  counter?: Counter,
): number | undefined {
  return counter?.inc();
}

export function groupingBreaksChain(profile?: Profile): string | undefined {
  const grouped = (profile as unknown as { name?: string })?.name;
  return grouped?.toString();
}

export function chainedOptional(profile?: Profile): string | undefined {
  return profile?.address?.city?.toUpperCase();
}
