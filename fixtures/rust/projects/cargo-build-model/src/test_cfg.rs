//! RS-CAN-PROJ-021: cfg(test), cfg(doc), cfg(doctest) entities.
//! This module exists only under test compilation via `#[cfg(test)]`.
//! It is the planned single test for the fixture.

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_test_for_cfg_test() {
        // This test only compiles under `cargo test` via `cfg(test)`.
        assert_eq!(crate::normal_api(), 1);
        assert_eq!(test_helper(), 42);
    }

    fn test_helper() -> u32 {
        42
    }
}

// RS-CAN-PROJ-021: cfg(doc) entity mapped to `cargo doc` command.
#[cfg(doc)]
pub struct DocOnlyItem {
    pub docs: &'static str,
}

// RS-CAN-PROJ-021: cfg(doctest) entity mapped to rustdoc doctest compilation.
#[cfg(doctest)]
pub fn doctest_item() -> u32 {
    123
}

// An `#[ignore]`d test still compiles under `cargo test` (only its execution is
// skipped); it is documented here rather than added as a second test, since the
// accepted brief plans exactly one test (`tests::unit_test_for_cfg_test` above):
// `#[test] #[ignore] fn ignored_test_still_compiles() { ... }` would compile
// under `cfg(test)` and be reported as "ignored" by the test harness without
// running.
