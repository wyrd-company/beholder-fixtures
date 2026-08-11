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
  // parentheses terminate the optional chain; .city is a regular access on the result of profile?.address
  // contrast with profile?.address?.city where both accesses are optional
  return (profile?.address as unknown as { city: string }).city;
}

export function groupingTerminatesChain(profile?: Profile): string | undefined {
  // (profile?.address) ends the chain – the following .city would access undefined if profile is missing
  const chained = profile?.address?.city;
  void chained;
  return (profile?.address as unknown as { city: string }).city;
}

export function chainedOptional(profile?: Profile): string | undefined {
  return profile?.address?.city?.toUpperCase();
}
