//! RS-CAN-MAC-001: declarative matching, fragments, and repetition.

// Multiple arms demonstration (already via decl_provider::multi_arm, but local variant)
macro_rules! local_multi_arm {
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

// Fragment families: ident, path, ty, vis, literal, block, stmt, pat, meta, tt
macro_rules! local_fragment_demo {
    (ident $n:ident) => { stringify!($n) };
    (ty $t:ty) => { stringify!($t) };
    (vis $v:vis fn f()) => { $v fn f() {} };
    (lit $l:literal) => { $l };
    (block $b:block) => { $b };
    (path $p:path) => { stringify!($p) };
    (pat $p:pat) => { stringify!($p) };
    (meta $m:meta) => { stringify!($m) };
    (tt $($t:tt)*) => { stringify!($($t)*) };
}

// Nested repetitions with separators, item/expr/stmt/pat output
macro_rules! define_pairs {
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

macro_rules! gen_item_local {
    (struct $name:ident { $($field:ident : $ty:ty),* $(,)? } ) => {
        pub struct $name { $( pub $field: $ty, )* }
    };
}

macro_rules! gen_expr_local {
    ($e:expr) => {
        $e
    };
}

macro_rules! gen_stmt_local {
    (let $name:ident = $val:expr) => {
        let $name = $val;
    };
}

macro_rules! gen_pat_local {
    ($pat:pat => $expr:expr) => {
        match 5u32 {
            $pat => $expr,
            _ => 0,
        }
    };
}

// Define items via macro for code-graph
gen_item_local!(
    struct SampleStruct {
        id: u32,
        label: String,
    }
);

pub fn multi_arm_demo() -> u32 {
    local_multi_arm!() + local_multi_arm!(1) + local_multi_arm!(1, 2) + local_multi_arm!(1, 2, 3)
}

pub fn fragment_demo() -> u32 {
    let _ = local_fragment_demo!(ident demo);
    let _ = local_fragment_demo!(ty u32);
    let _ = local_fragment_demo!(lit 42);
    let _ = local_fragment_demo!(block { 1 + 2 });
    let _ = local_fragment_demo!(path std::vec::Vec);
    let _ = local_fragment_demo!(pat x);
    let _ = local_fragment_demo!(meta allow(dead_code));
    let _ = local_fragment_demo!(tt hello world);
    // Use decl_provider fragment demo across crate
    let _ = decl_provider::fragment_demo!(ident hello);
    let _ = decl_provider::fragment_demo!(expr 1 + 2);
    let _ = decl_provider::fragment_demo!(ty Vec<u32>);
    let _ = decl_provider::fragment_demo!(lit "text");
    1
}

pub fn nested_repeat_demo() -> u32 {
    define_pairs!(a => 1, b => 2; c => 3, d => 4;)
}

pub fn output_kinds_demo() -> u32 {
    gen_stmt_local!(let value = 10);
    let expr_val = gen_expr_local!(value + 5);
    let pat_val = gen_pat_local!(5 => 100);
    // Use provider item generation (item output, not expression)
    decl_provider::gen_item!(
        struct ProviderItem {
            field: u32,
        }
    );
    let _provider_field = ProviderItem { field: 7 };
    decl_provider::nested_pairs!(x => 1, y => 2; z => 3;) + expr_val + pat_val
}

// Cross-edition fragment grammar differences (2015 expr, 2021 pat_param, 2024 expr_2021)
// 2024 edition: `expr` includes new syntax, `expr_2021` captures the 2021 fragment grammar
#[macro_export]
macro_rules! expr_2024_demo {
    ($e:expr) => {
        $e
    };
}
#[macro_export]
macro_rules! expr_2021_demo {
    ($e:expr_2021) => {
        $e
    };
}

pub fn expr_2024_demo() -> u32 {
    expr_2024_demo!(1 + 2) + expr_2021_demo!(1 + 2)
}

// Counterexamples (invalid, not compiled) documented in docs/counterexamples.md:
// - no matching arm: `multi_arm!(1, 2, 3, 4)` has no 4-arg arm
// - follow-set violation: `nested_pairs!(a => )` missing expr after =>
// - recursion limit violation: deeply recursive macro exceeding recursion_limit

pub fn declarative_summary() -> u32 {
    multi_arm_demo()
        + fragment_demo()
        + nested_repeat_demo()
        + output_kinds_demo()
        + expr_2024_demo()
}
