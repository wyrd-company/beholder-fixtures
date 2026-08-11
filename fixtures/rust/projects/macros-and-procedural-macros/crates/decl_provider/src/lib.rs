//! RS-CAN-MAC-001, MAC-002, MAC-003 declarative provider.
//! Demonstrates fragment families, scope, export, and hygiene.

// RS-CAN-MAC-001: fragment families and multiple arms
#[macro_export]
macro_rules! fragment_demo {
    // ident fragment
    (ident $name:ident) => {
        stringify!($name)
    };
    // expr fragment
    (expr $e:expr) => {
        $e
    };
    // ty fragment
    (ty $t:ty) => {
        stringify!($t)
    };
    // vis fragment
    (vis $v:vis fn demo_fn()) => {
        $v fn demo_fn() {}
    };
    // literal fragment
    (lit $l:literal) => {
        $l
    };
    // block fragment
    (block $b:block) => {
        $b
    };
    // path fragment
    (path $p:path) => {
        $p
    };
    // meta fragment
    (meta $m:meta) => {
        stringify!($m)
    };
    // tt fragment
    (tt $($t:tt)*) => {
        stringify!($($t)*)
    };
}

#[macro_export]
macro_rules! multi_arm {
    () => {
        0u32
    };
    ($a:expr) => {
        $a
    };
    ($a:expr, $b:expr) => {
        $a + $b
    };
    ($a:expr, $b:expr, $c:expr) => {
        $a + $b + $c
    };
}

// RS-CAN-MAC-001: nested repetitions with separators, item/expression/statement/pattern output
#[macro_export]
macro_rules! nested_pairs {
    ( $( $( $k:ident => $v:expr ),* ; )* ) => {
        {
            let mut sum = 0u32;
            $(
                $(
                    sum += $v;
                )*
            )*
            sum
        }
    };
}

// Item output: generates struct
#[macro_export]
macro_rules! gen_item {
    (struct $name:ident { $($field:ident : $ty:ty),* $(,)? } ) => {
        pub struct $name {
            $(
                pub $field: $ty,
            )*
        }
    };
}

// Expression output
#[macro_export]
macro_rules! gen_expr {
    ($e:expr) => {
        $e
    };
}

// Statement output
#[macro_export]
macro_rules! gen_stmt {
    (let $name:ident = $val:expr) => {
        let $name = $val;
    };
}

// Pattern output: generates match arm pattern
#[macro_export]
macro_rules! gen_pat {
    ($pat:pat => $expr:expr) => {
        match 42u32 {
            $pat => $expr,
            _ => 0u32,
        }
    };
}

// RS-CAN-MAC-002: scope, export, shadowing foundation
// This macro is exported and appears at crate root via #[macro_export]
#[macro_export]
macro_rules! scope_demo {
    () => {
        99u32
    };
}

// Local inner macro for textual scope demonstration
pub mod inner_scope {
    macro_rules! textual_macro {
        () => {
            10u32
        };
    }

    // Use before later shadowing: this call resolves to first definition
    pub fn before_shadow() -> u32 {
        textual_macro!()
    }

    macro_rules! textual_macro {
        () => {
            20u32
        };
    }

    pub fn after_shadow() -> u32 {
        textual_macro!()
    }
}

// RS-CAN-MAC-002: re-exported macro path
pub use scope_demo as reexported_scope_demo;

// RS-CAN-MAC-003: hygiene and $crate
pub mod hygiene_helper {
    pub fn helper_value() -> u32 {
        42
    }

    pub const HELPER_CONST: u32 = 100;
}

#[macro_export]
macro_rules! hygiene_demo {
    // generates noncolliding local (hygienic)
    (local) => {{
        let __hygiene_local = 1u32;
        __hygiene_local + 1
    }};
    // accepts explicit identifier that becomes caller-visible
    (bind $var:ident = $val:expr) => {
        let $var = $val;
    };
    // references invocation-site item via hygiene (caller provides `caller_item`)
    (use_caller) => {
        caller_item + 1
    };
    // $crate through re-export: calls public helper via $crate
    (use_crate_helper) => {
        $crate::hygiene_helper::helper_value()
    };
    // $crate variant for downstream re-export
    (use_crate_const) => {
        $crate::hygiene_helper::HELPER_CONST
    };
}

// Re-export for downstream $crate demonstration
pub use hygiene_demo as reexported_hygiene;

#[macro_export]
macro_rules! crate_helper_macro {
    () => {
        $crate::hygiene_helper::helper_value()
    };
}

// RS-CAN-MAC-004: macro-generated named entities family
#[macro_export]
macro_rules! define_family {
    ( $( $name:ident ),* $(,)? ) => {
        $(
            pub struct $name {
                pub id: u32,
            }
            impl $name {
                pub fn new(id: u32) -> Self {
                    Self { id }
                }
                pub fn id(&self) -> u32 {
                    self.id
                }
            }
        )*
        pub static FAMILY_COUNT: u32 = 0 $( + { let _ = stringify!($name); 1 } )*;
        pub mod generated_family_mod {
            pub fn value() -> u32 { 1 }
        }
    };
}

// Helper for cross-crate macro_use demonstration
#[macro_export]
macro_rules! legacy_provider_macro {
    () => {
        "legacy"
    };
}
