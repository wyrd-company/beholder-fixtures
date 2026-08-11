//! Fixture for Rust macros and procedural macros (RS-CAN-PROJ-013, RS-CAN-PROJ-018, RS-CAN-MAC-001..008, RS-CAN-ECO-009).

// Re-export proc macros for $crate usage
pub use macro_host;

pub mod builtins;
pub mod declarative;
pub mod derive_support;
pub mod dsl_support;
pub mod entry_points;
pub mod generated;
pub mod hygiene;
pub mod proc_transform;
pub mod scope;
pub mod spans;

pub use builtins::builtins_summary;
pub use declarative::declarative_summary;
pub use dsl_support::dsl_summary;
pub use entry_points::entry_points_summary;
pub use generated::generated_summary;
pub use hygiene::hygiene_summary;
pub use proc_transform::proc_transform_summary;
pub use scope::scope_summary;
pub use spans::spans_summary;

// Shared helper for $crate demonstration
pub mod hygiene_helper {
    pub fn helper_value() -> u32 {
        42
    }
    pub const HELPER_CONST: u32 = 100;
}

// Cross-edition invocation demonstration (RS-CAN-PROJ-016 style but for macros)
pub fn cross_edition_summary() -> Vec<u32> {
    vec![
        edition_2015::cross_from_2015!(),
        edition_2018::cross_from_2018!(),
        edition_2021::cross_from_2021!(),
        cross_from_2024!(),
    ]
}

#[macro_export]
macro_rules! cross_from_2024 {
    () => {
        2024u32
    };
}

pub fn fixture_summary() -> &'static str {
    "macros-and-procedural-macros"
}

// RS-CAN-PROJ-018: generated test main coverage via libtest harness
// Single planned test target whose existence proves libtest-generated main.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generated_main_smoke() {
        assert_eq!(fixture_summary(), "macros-and-procedural-macros");
    }
}
