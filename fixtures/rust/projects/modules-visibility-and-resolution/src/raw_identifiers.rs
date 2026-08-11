// RS-CAN-MOD-013: raw identifiers for keyword spellings and non-ASCII identifier.

// Older-edition keyword `try` (keyword in 2018+) exported to newer edition consumer using raw identifier.
pub fn r#try() -> u32 {
    999
}

pub struct r#type {
    pub value: u32,
}

impl r#type {
    pub fn new(v: u32) -> Self {
        Self { value: v }
    }
}

// Raw identifier allowing keyword as field name.
pub struct WithKeywordField {
    pub r#match: u32,
    pub r#async: u32,
}

// Non-ASCII identifier.
pub fn naïve_café() -> u32 {
    42
}

pub struct Café {
    pub déjà_vu: u32,
}

impl Café {
    pub fn naïve_method(&self) -> u32 {
        self.déjà_vu
    }
}

// Variable with non-ASCII name.
pub fn unicode_identifier_demo() -> u32 {
    let café = 10u32;
    let naïve = café + 5;
    let delta = naïve + 2;
    delta
}

// Raw identifier for `async` keyword in different position.
pub fn call_raw_identifiers() -> u32 {
    let t = r#type::new(5);
    let s = WithKeywordField {
        r#match: 1,
        r#async: 2,
    };
    t.value + s.r#match + s.r#async + r#try() + naïve_café() + unicode_identifier_demo()
}

// `gen` keyword handling: `r#gen` required where `gen` is reserved (edition 2024 context).
pub fn r#gen() -> u32 {
    777
}
