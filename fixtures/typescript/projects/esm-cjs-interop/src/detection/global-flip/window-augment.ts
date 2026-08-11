// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

declare global {
  interface WindowLike {
    paneTitle: string;
  }

  var windowLike: WindowLike;
}

export {};
