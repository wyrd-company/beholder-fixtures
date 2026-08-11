/// Documented backend compiler pragmas used across this project's compiled
/// targets, matching DART-CAN-PLAT-010. This is not a complete pragma
/// catalog — the checklist does not require one — only a representative,
/// documented sample. Pragma names and effects are backend contracts:
/// `vm:*` pragmas are documented by the Dart VM's pragma reference and
/// source, `dart2js:*` pragmas by the dart2js compiler. An unrecognized or
/// misspelled pragma name is silently ignored by the compiler rather than
/// rejected.
library;

/// Requests inlining at VM JIT and native AOT call sites where the backend
/// judges it profitable; the backend may still decline.
@pragma('vm:prefer-inline')
int _preferInlinedAdd(int a, int b) => a + b;

/// Forbids inlining at VM JIT and native AOT call sites, keeping this
/// function separately visible in stack traces and profiles.
@pragma('vm:never-inline')
int _neverInlinedMultiply(int a, int b) => a * b;

/// The dart2js analogue of `vm:never-inline`, forbidding inlining when
/// compiling to JavaScript.
@pragma('dart2js:noInline')
int _dart2jsNoInlineSubtract(int a, int b) => a - b;

/// Exercises every pragma-annotated function above under whichever backend
/// compiled this code, so each stays reachable rather than tree-shaken.
int combinePragmaExamples(int a, int b) =>
    _preferInlinedAdd(a, b) +
    _neverInlinedMultiply(a, b) -
    _dart2jsNoInlineSubtract(a, b);
