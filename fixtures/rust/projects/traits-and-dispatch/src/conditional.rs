//! RS-CAN-TRAIT-003 — conditional and blanket implementations.

/// Wrapper whose trait impl is conditional on the inner type.
pub struct Wrap<T>(pub T);

/// Conditional trait implemented only when `T: Clone`.
pub trait Replicate {
    fn replicate(&self) -> Self;
}

impl<T: Clone> Replicate for Wrap<T> {
    fn replicate(&self) -> Self {
        Wrap(self.0.clone())
    }
}

/// Blanket extension trait for all types implementing `Display`.
pub trait ExtLabel {
    fn ext_label(&self) -> String;
}

impl<T: std::fmt::Display> ExtLabel for T {
    fn ext_label(&self) -> String {
        format!("ext:{self}")
    }
}

/// A type that satisfies `Display`, therefore gets the blanket impl.
pub struct Displayable(pub i32);

impl std::fmt::Display for Displayable {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Displayable({})", self.0)
    }
}

/// A type that does not satisfy `Display` and thus does not obtain `ExtLabel`.
pub struct Opaque(pub i32);

pub fn conditional_summary() -> String {
    let w = Wrap(42_i32);
    let replicated = w.replicate();
    let d = Displayable(5);
    let label = d.ext_label();
    let also_string = "hello".ext_label();
    let _ = replicated;
    format!("{label}|{also_string}")
}

/// Non-satisfying site is valid because the conditional bound is not met:
///
/// ```rust,ignore
/// let opaque_wrap = Wrap(Opaque(1));
/// // let _ = opaque_wrap.replicate(); // error: Opaque does not implement Clone
/// ```
///
/// Similarly for blanket extension:
///
/// ```rust,ignore
/// let o = Opaque(2);
/// // let _ = o.ext_label(); // error: Opaque does not implement Display
/// ```
pub fn conditional_counterexample_docs() -> &'static str {
    "see docs/counterexamples.md for non-satisfying sites"
}
