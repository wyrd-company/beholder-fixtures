//! Fixture for Rust trait system and dispatch.

pub mod ambiguity;
pub mod auto_traits;
pub mod coherence;
pub mod conditional;
pub mod conversion;
pub mod derive_traits;
pub mod dispatch;
pub mod drop_semantics;
pub mod inherent;
pub mod lookup;
pub mod operator_traits;
pub mod receivers;
pub mod supertrait;

pub use ambiguity::{Resolver, alpha::Alpha, beta::Beta};
pub use auto_traits::{
    AllSend, GenericHolder, NotSend, SafeRaw, WithMarker, WithRawPointer, auto_traits_summary,
};
pub use coherence::{
    LocalTrait, LocalType, Wrapper, coherence_summary, display_summary, fundamental_summary,
    orphan_order_summary,
};
pub use conditional::{ExtLabel, Replicate, Wrap, conditional_summary};
pub use conversion::{CheckedId, ConversionError, UserId, conversion_summary};
pub use derive_traits::{
    DerivedEnum, DerivedGeneric, DerivedPhantom, DerivedWithCustomDefault, ManualPhantom,
    NeedsCopy, derive_summary,
};
pub use dispatch::{Circle, Drawable, Square, Triangle, dispatch_summary};
pub use drop_semantics::{Copyable, NonCopy, drop_summary};
pub use inherent::{Widget, WidgetDescribe, inherent_summary, same_spelling_demo};
pub use lookup::{Leaf, Mid, Outer, lookup_summary};
pub use operator_traits::{Buffer, Count, Displayed, operator_summary};
pub use receivers::{ReceiverDemo, ReceiverTrait, receivers_summary};
pub use supertrait::{Base, Derived, InheritAll, OverrideDefault, supertrait_summary};

/// Marks `Alpha::Output` associated type usage for ambiguity coverage.
pub type AmbiguitySummary = <Resolver as Alpha>::Output;

/// Aggregated summary tying all trait fixture modules together.
pub fn fixture_summary() -> String {
    let mut parts = Vec::new();
    parts.push(inherent::same_spelling_demo());
    parts.push(coherence::display_summary());
    parts.push(conditional::conditional_summary());
    let (a, b, c, d) = supertrait::supertrait_summary();
    parts.push(format!("{a}|{b}|{c}|{d}"));
    parts.push(receivers::receivers_summary().to_string());
    let (leaf, mid, outer, shadowed, g1, g2, choice, len) = lookup::lookup_summary();
    parts.push(format!(
        "{leaf}|{mid}|{outer}|{shadowed}|{g1}|{g2}|{choice}|{len}"
    ));
    let (via_alpha_trait, via_alpha_fqs, via_beta_trait, via_beta_fqs, ac, bc, am, bm) =
        ambiguity::ambiguity_summary();
    parts.push(format!(
        "{via_alpha_trait}|{via_alpha_fqs}|{via_beta_trait}|{via_beta_fqs}|{ac}|{bc}|{am}|{bm}"
    ));
    parts.extend(dispatch::dispatch_summary());
    parts.push(auto_traits::auto_traits_summary().to_owned());
    parts.push(operator_traits::operator_summary());
    parts.push(conversion::conversion_summary());
    parts.push(drop_semantics::drop_summary());
    parts.push(derive_traits::derive_summary());
    parts.push(coherence::fundamental_summary());
    parts.push(coherence::orphan_order_summary());
    parts.join("|")
}
