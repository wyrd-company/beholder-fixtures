// RS-CAN-GEN-006: function and method lifetime elision, '_ inference,
// and trait-object default lifetime bounds.

// Elided free function: single input lifetime is output lifetime.
pub fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}

// Explicit counterpart.
pub fn first_word_explicit<'a>(text: &'a str) -> &'a str {
    text.split_whitespace().next().unwrap_or("")
}

// Two inputs, one output requires explicit annotation (elision would be ambiguous).
pub fn longer<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() > b.len() { a } else { b }
}

// '_ inference: inferred lifetime placeholder in reference type.
pub fn inferred_placeholder(value: &str) -> &str {
    // Type ascription with '_ requests inference.
    let borrowed: &'_ str = value;
    borrowed
}

// Explicit '_ placeholder in type path.
pub fn borrowed_with_placeholder(value: &str) -> &str {
    let inferred: &'_ str = value;
    inferred
}

// Function returning reference with inferred '_ in return position via argument.
pub fn borrow_with_inferred(value: &String) -> &str {
    value.as_str()
}

// Methods demonstrating elision with receiver.
pub struct Document {
    pub content: String,
}

impl Document {
    // Elided: &self input lifetime is output lifetime.
    pub fn as_str(&self) -> &str {
        &self.content
    }

    // Explicit equivalent.
    pub fn as_str_explicit<'a>(&'a self) -> &'a str {
        &self.content
    }

    // Mutable elision.
    pub fn as_mut(&mut self) -> &mut String {
        &mut self.content
    }

    // Receiver elision with additional reference parameter: elided rules apply.
    pub fn prefer_content<'a>(&'a self, fallback: &'a str) -> &'a str {
        if self.content.is_empty() {
            fallback
        } else {
            &self.content
        }
    }
}

// Impl header with lifetime parameter (distinct from elision).
pub struct Wrapper<'a, T> {
    pub inner: &'a T,
}

impl<'a, T> Wrapper<'a, T> {
    pub fn inner_ref(&self) -> &'a T {
        self.inner
    }
}

// Trait object default lifetime bounds.
// Without annotation, Box<dyn Trait> defaults to 'static.
pub trait Summary: Send {
    fn summary(&self) -> String;
}

impl Summary for Document {
    fn summary(&self) -> String {
        self.content.clone()
    }
}

impl Summary for String {
    fn summary(&self) -> String {
        self.clone()
    }
}

// Box<dyn Trait> defaults to Box<dyn Trait + 'static>.
pub fn boxed_static_summary(value: String) -> Box<dyn Summary> {
    Box::new(value)
}

/// Borrowed implementor holding a non-static reference.
#[derive(Debug)]
pub struct BorrowedSummary<'a>(pub &'a str);

impl<'a> Summary for BorrowedSummary<'a> {
    fn summary(&self) -> String {
        self.0.to_owned()
    }
}

// Box<dyn Trait + 'a> carries the borrowed lifetime; contrast with default 'static.
pub fn borrowed_summary<'a>(value: &'a str) -> Box<dyn Summary + 'a> {
    Box::new(BorrowedSummary(value))
}

// Accepting trait object with inferred lifetime.
pub fn accept_borrowed_summary(obj: Box<dyn Summary + '_>) -> String {
    obj.summary()
}

// Function item vs closure inference contrast: closures infer lifetimes
// per call site, function items have fixed signature.
pub fn function_item_inference() {
    let closure = |s: &str| s.len();
    let from_closure: usize = closure("hello");
    fn function_item(s: &str) -> usize {
        s.len()
    }
    let from_fn: usize = function_item("hello");
    let _ = (from_closure, from_fn);
}

// Demonstrates inferred '_ path vs explicit.
pub fn inferred_vs_explicit(value: &String) -> &str {
    let explicit: &str = value.as_str();
    let inferred: &str = value;
    let _ = explicit.len() + inferred.len();
    value.as_str()
}

pub fn elision_summary() -> &'static str {
    "elision"
}
