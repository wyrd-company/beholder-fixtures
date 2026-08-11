// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { Shape } from "./abstract-base.js";
import { Rectangle } from "./concrete-derived.js";

export class Circle extends Shape {
  constructor(
    tag: string,
    public radius: number,
  ) {
    super(tag);
  }

  override area(): number {
    return Math.PI * this.radius * this.radius;
  }
}

/** Base-typed polymorphic dispatch. */
export function totalArea(shapes: Shape[]): number {
  let sum = 0;
  for (const s of shapes) sum += s.area();
  return sum;
}

export function exercisePolymorphicCall(): void {
  const shapes: Shape[] = [new Rectangle("r1", 3, 4), new Circle("c1", 2)];
  const total: number = totalArea(shapes);
  void total;
}

/** Abstract construct signature. */
export abstract class AbstractVehicle {
  abstract drive(): string;
  constructor(public id: string) {}
}

export type AbstractVehicleCtor = abstract new (id: string) => AbstractVehicle;

export function createVehicle(
  ctor: AbstractVehicleCtor,
  id: string,
): AbstractVehicle {
  // Abstract construct is a type-only signature; runtime uses concrete subclass.
  return new (ctor as unknown as new (id: string) => AbstractVehicle)(id);
}

export class Car extends AbstractVehicle {
  override drive(): string {
    return `car:${this.id}`;
  }
}
