// noImplicitThis off: implicit any this is allowed.
// Under noImplicitThis true, the this reference without annotation is an error.

export function getTitle() {
  return this.title;
}

export const archive = {
  title: "archive",
  getTitle() {
    return this.title;
  },
};
