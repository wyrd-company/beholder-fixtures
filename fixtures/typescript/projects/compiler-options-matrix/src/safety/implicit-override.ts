// noImplicitOverride: overriding members must be marked with `override`.

export class BaseArchive {
  title: string = "base";
  describe(): string {
    return this.title;
  }
}

export class DerivedArchive extends BaseArchive {
  override title = "derived";
  override describe(): string {
    return `derived:${super.describe()}`;
  }
}

export class FurtherDerived extends DerivedArchive {
  override describe(): string {
    return `further:${super.describe()}`;
  }
}
