//! RS-CAN-MAC-005: derive macros and helper attributes support trait.

// Trait that derive macro implements
pub trait Describe {
    fn tag() -> &'static str;
    fn describe(&self) -> String;
}

// Manual impl for comparison (shows generated vs handwritten)
pub struct ManualDescribe {
    pub field: u32,
}

impl Describe for ManualDescribe {
    fn tag() -> &'static str {
        "manual"
    }
    fn describe(&self) -> String {
        format!("ManualDescribe:{}", Self::tag())
    }
}

// Built-in derives comparison
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BuiltinDerives {
    pub x: u32,
}

// Generic consumption through bound (RS-CAN-MAC-005)
pub fn consume_describe<T: Describe>(value: &T) -> String {
    value.describe()
}

pub fn describe_summary() -> String {
    let m = ManualDescribe { field: 1 };
    consume_describe(&m)
}
