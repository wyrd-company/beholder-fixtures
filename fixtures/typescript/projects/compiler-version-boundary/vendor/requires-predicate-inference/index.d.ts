export type PredicateGuard<T> = (value: unknown) => value is T;
export declare function wrapGuard<T>(guard: PredicateGuard<T>): PredicateGuard<T>;
