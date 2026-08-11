//! RS-CAN-MAC-004: macro-generated named entities.

// Declarative family generation
decl_provider::define_family!(AlphaItem, BetaItem, GammaItem);

// Procedural item generation via macro_host
macro_host::make_item!(ProcGeneratedStruct);

// Procedural concat_idents demonstration - stable identifier concatenation
macro_host::make_item!(Hello);
macro_host::make_item!(World);
macro_host::make_item!(HelloWorld);
type ViaConcat = macro_host::concat_idents!(Hello, World);
pub fn concat_demo() -> u32 {
    let hw: ViaConcat = ViaConcat { value: 7 };
    hw.get()
}

// Reference generated items from ordinary code
pub fn family_demo() -> u32 {
    let a = AlphaItem::new(1);
    let b = BetaItem::new(2);
    let c = GammaItem::new(3);
    a.id() + b.id() + c.id() + FAMILY_COUNT
}

// Procedural struct usage
pub fn proc_item_demo() -> u32 {
    let s = ProcGeneratedStruct::new(10);
    s.get()
}

// Module generation via declarative macro
macro_rules! gen_module {
    ($name:ident) => {
        pub mod $name {
            pub fn value() -> u32 {
                42
            }
            pub static MODULE_STATIC: u32 = 99;
        }
    };
}

gen_module!(generated_mod);

pub fn module_demo() -> u32 {
    generated_mod::value() + generated_mod::MODULE_STATIC
}

// Static generation
macro_rules! gen_static {
    ($name:ident = $val:expr) => {
        pub static $name: u32 = $val;
    };
}

gen_static!(GENERATED_STATIC = 123);

pub fn static_demo() -> u32 {
    GENERATED_STATIC
}

// Companion items via derive-generated companion type (RS-CAN-MAC-005 companion)
// The derive Describe generates impl, but companion type example uses proc make_item as companion
macro_host::make_item!(CompanionItem);

pub fn companion_demo() -> u32 {
    let c = CompanionItem { value: 5 };
    c.get()
}

// Hidden $crate::__private support API counterexample documented in docs

// Duplicate output collision documented as invalid: `define_family!(AlphaItem, AlphaItem)` would duplicate

pub fn generated_summary() -> u32 {
    family_demo()
        + proc_item_demo()
        + concat_demo()
        + module_demo()
        + static_demo()
        + companion_demo()
}
