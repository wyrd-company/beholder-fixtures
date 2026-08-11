// Automatic declaration inclusion — .d.ts discovered automatically when its .js or context is included.
declare type AutoRootCard = {
  id: string;
  label: string;
};

declare const autoRootHelper: (card: AutoRootCard) => string;
