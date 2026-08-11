//! RS-CAN-TRAIT-004 — supertrait hierarchy with inherited and overridden defaults.

pub trait Base {
    fn base_value(&self) -> i32;
    fn defaulted(&self) -> i32 {
        self.base_value() + 10
    }
    fn combined(&self) -> i32 {
        self.base_value() + self.defaulted()
    }
}

pub trait Derived: Base {
    fn derived_value(&self) -> i32;
    fn derived_default(&self) -> i32 {
        self.derived_value() * 2
    }
}

pub struct InheritAll {
    pub base: i32,
    pub derived: i32,
}

impl Base for InheritAll {
    fn base_value(&self) -> i32 {
        self.base
    }
}

impl Derived for InheritAll {
    fn derived_value(&self) -> i32 {
        self.derived
    }
}

pub struct OverrideDefault {
    pub base: i32,
    pub derived: i32,
}

impl Base for OverrideDefault {
    fn base_value(&self) -> i32 {
        self.base
    }

    fn defaulted(&self) -> i32 {
        self.base_value() * 100
    }
}

impl Derived for OverrideDefault {
    fn derived_value(&self) -> i32 {
        self.derived
    }

    fn derived_default(&self) -> i32 {
        self.derived_value() + self.base_value()
    }
}

pub fn supertrait_summary() -> (i32, i32, i32, i32) {
    let a = InheritAll {
        base: 3,
        derived: 4,
    };
    let b = OverrideDefault {
        base: 3,
        derived: 4,
    };
    (
        a.defaulted(),
        b.defaulted(),
        a.derived_default(),
        b.derived_default(),
    )
}

/// Qualified call demonstrates that supertrait defaults are distinct bodies.
pub fn qualified_default_demo(obj: &OverrideDefault) -> i32 {
    <OverrideDefault as Base>::defaulted(obj)
}
