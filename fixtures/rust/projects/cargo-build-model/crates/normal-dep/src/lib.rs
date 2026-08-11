pub fn normal_fn() -> u32 {
    10
}
pub struct NormalType(pub u32);

// RS-CAN-PROJ-009: transitive graph-wide patch effect. `vendored-crate` is
// requested here (a second, non-root edge) as if from crates-io; the root
// workspace's `[patch.crates-io]` redirects it to `vendor/vendored-crate` for
// every edge in the graph, not only the root package's own direct dependency.
pub fn normal_dep_vendored() -> u32 {
    vendored_crate::vendored_fn()
}

// RS-CAN-PROJ-005 / RS-CAN-PROJ-022: same package compiled simultaneously in two
// roles. The root manifest depends on `normal-dep` normally (target role, this
// function returns "target") and again as a build-dependency with
// `features = ["host-only"]` (host role, returns "host"), producing two distinct
// crate instances of identical source in one build.
#[cfg(feature = "host-only")]
pub fn role() -> &'static str {
    "host"
}

#[cfg(not(feature = "host-only"))]
pub fn role() -> &'static str {
    "target"
}
