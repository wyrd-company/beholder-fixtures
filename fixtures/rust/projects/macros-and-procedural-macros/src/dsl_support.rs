//! RS-CAN-ECO-009: hermetic DSL support types and offline data usage.

// Typed output for DSL macros
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Record {
    pub name: &'static str,
    pub value: u32,
}

// Const records generated via offline file (hermetic, deterministic)
pub static RECORDS: &[Record] = &[
    Record {
        name: "alpha",
        value: 10,
    },
    Record {
        name: "beta",
        value: 20,
    },
    Record {
        name: "gamma",
        value: 30,
    },
    Record {
        name: "delta",
        value: 40,
    },
];

// Generated via macro_host offline_records!()
pub fn offline_records_demo() -> &'static [Record] {
    macro_host::offline_records!()
}

// Generated via inline_dsl parsing embedded non-Rust syntax
pub fn inline_dsl_demo() -> &'static [Record] {
    macro_host::inline_dsl!("alpha 10; beta 20; gamma 30")
}

// Determinism: same macro invocation always produces same typed output offline
pub fn dsl_count() -> usize {
    offline_records_demo().len() + inline_dsl_demo().len()
}

// Counterexample (invalid, not compiled) expansion-time invalid input:
// `inline_dsl!("alpha not_a_number")` would emit `compile_error!` at expansion time
// `offline_records!()` with malformed data file would also emit compile_error!

pub fn dsl_summary() -> usize {
    dsl_count()
}
