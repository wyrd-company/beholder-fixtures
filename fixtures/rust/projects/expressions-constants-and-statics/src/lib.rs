//! Fixture for Rust expressions, constants, and statics.
//! Covers RS-CAN-EXPR-001 through RS-CAN-EXPR-009 and RS-CAN-CONST-001 through RS-CAN-CONST-003.

pub mod blocks;
pub mod conditionals;
pub mod const_fn;
pub mod const_static;
pub mod divergence;
pub mod evaluation_order;
pub mod literals;
pub mod loops;
pub mod place_contexts;
pub mod promotion_tls;
pub mod question_mark;
pub mod ranges_indexing;

/// Aggregated demonstration entry that touches each module so that
/// build and lint observe reachable valid code.
pub fn fixture_overview() -> &'static str {
    let _ = place_contexts::demonstrate();
    let _ = blocks::demonstrate();
    let _ = conditionals::demonstrate();
    let _ = loops::demonstrate();
    let _ = divergence::demonstrate();
    let _ = question_mark::demonstrate();
    let _ = ranges_indexing::demonstrate();
    let _ = evaluation_order::demonstrate();
    let _ = literals::demonstrate();
    let _ = const_static::demonstrate();
    let _ = const_fn::demonstrate();
    let _ = promotion_tls::demonstrate();
    "expressions-constants-and-statics"
}
