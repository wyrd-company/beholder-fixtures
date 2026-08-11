export type MutableRecord<T> = {
  -readonly [Key in keyof T]: T[Key];
};

export type ReadonlyRecord<T> = {
  readonly [Key in keyof T]: T[Key];
};

export function mappedReadonlyAdd<T extends object>(
  value: T,
): ReadonlyRecord<T> {
  return value as ReadonlyRecord<T>;
}

export function mappedReadonlyRemove<T extends object>(
  value: ReadonlyRecord<T>,
): MutableRecord<T> {
  return value as MutableRecord<T>;
}
