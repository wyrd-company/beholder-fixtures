interface PropertyBagExport {
  ownMarker: string;
  inheritedMarker: string;
  readOwn(): string;
}

declare const exportBag: PropertyBagExport;

export = exportBag;
