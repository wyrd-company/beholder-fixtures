//! Downstream crate exercising cross-crate visibility and non-exhaustiveness.

/// Non-exhaustive enum: cross-crate matches must include a wildcard.
#[non_exhaustive]
pub enum ExternalChoice {
    Alpha,
    Beta,
    Gamma,
}

/// Non-exhaustive struct: construction requires a constructor.
#[non_exhaustive]
pub struct ExternalRecord {
    pub visible: i32,
    hidden: i32,
}

impl ExternalRecord {
    pub fn new(visible: i32, hidden: i32) -> Self {
        Self { visible, hidden }
    }

    pub fn hidden(&self) -> i32 {
        self.hidden
    }
}

/// Struct with a private field that cannot be constructed externally via literal.
pub struct PrivateFields {
    pub public: i32,
    private: String,
}

impl PrivateFields {
    pub fn new(public: i32, private: String) -> Self {
        Self { public, private }
    }

    pub fn private(&self) -> &str {
        &self.private
    }
}

/// Trait used for cross-crate trait-object upcasting demonstration.
pub trait ExternalBase: Send + Sync {
    fn label(&self) -> &'static str;
}

/// Subtrait for upcasting; empty subtrait relies on supertrait.
pub trait ExternalDerived: ExternalBase {}

/// Concrete type used behind a downstream trait object.
pub struct ConcreteHolder {
    pub id: u32,
}

impl ExternalBase for ConcreteHolder {
    fn label(&self) -> &'static str {
        "concrete"
    }
}

impl ExternalDerived for ConcreteHolder {}
