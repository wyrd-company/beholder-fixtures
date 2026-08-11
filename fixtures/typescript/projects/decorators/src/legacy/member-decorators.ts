// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Legacy member decorators (property and method) with descriptor mutation
 * and design:type / design:returntype emission.
 */

export const legacyMemberLog: string[] = [];

function readonlyProperty(target: Object, propertyKey: string | symbol): void {
  legacyMemberLog.push(`readonly:${String(propertyKey)}`);
}

function readonlyMember(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
): void {
  legacyMemberLog.push(`readonly:${String(propertyKey)}`);
  descriptor.writable = false;
}

function enumerableMember(
  value: boolean,
): (
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
) => void {
  return function (
    _target: Object,
    propertyKey: string | symbol,
    descriptor: PropertyDescriptor,
  ): void {
    legacyMemberLog.push(`enumerable:${String(propertyKey)}=${String(value)}`);
    descriptor.enumerable = value;
  };
}

function loggedMember(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
): PropertyDescriptor {
  legacyMemberLog.push(`logged:${String(propertyKey)}`);
  const original = descriptor.value as (...args: unknown[]) => unknown;
  descriptor.value = function (this: unknown, ...args: unknown[]): unknown {
    legacyMemberLog.push(`call:${String(propertyKey)}`);
    return original.apply(this, args);
  };
  return descriptor;
}

function outerMember(
  _target: Object,
  propertyKey: string | symbol,
  _descriptor: PropertyDescriptor,
): void {
  legacyMemberLog.push(`apply:outerMember:${String(propertyKey)}`);
}

function innerMember(
  _target: Object,
  propertyKey: string | symbol,
  _descriptor: PropertyDescriptor,
): void {
  legacyMemberLog.push(`apply:innerMember:${String(propertyKey)}`);
}

export class MemberGallery {
  @readonlyProperty
  title: string = "member-title";

  @readonlyProperty
  hiddenNote: string = "hidden";

  @loggedMember
  describe(label: string): string {
    return `member:${label}`;
  }

  @readonlyMember
  @enumerableMember(true)
  annotated(value: string): string {
    return value;
  }

  @outerMember
  @innerMember
  ordered(value: string): string {
    return value;
  }

  @loggedMember
  static create(id: string): MemberGallery {
    return new MemberGallery();
  }
}

export function getLegacyMemberLog(): string[] {
  return [...legacyMemberLog];
}
