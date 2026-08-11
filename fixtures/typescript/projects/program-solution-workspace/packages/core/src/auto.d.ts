// Automatic declaration inclusion — .d.ts picked up without explicit import via program include.
declare type AutoIncludedCard = {
  cardId: string;
  weight: number;
};

declare const autoCardRegistry: Map<string, AutoIncludedCard>;
