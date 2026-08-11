// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface RelayCard {
  channel: string;
}

export namespace RelayCard {
  export function format(card: RelayCard): string {
    return card.channel;
  }
}

export function readRelay(card: RelayCard): string {
  return RelayCard.format(card);
}
