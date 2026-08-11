//! RS-CAN-EXPR-002 — Blocks, statements, tails, and semicolons.

/// Value block: tail expression supplies the block's value.
pub fn value_block() -> i32 {
    let result = {
        let base: i32 = 10;
        base + 5
    };
    result
}

/// Unit block: semicolon discards tail value, block produces `()`.
pub fn unit_block() -> bool {
    let mut observed = false;
    {
        let _x: i32 = 40;
        observed = true;
        // Tail semicolon forces unit.
    };
    observed
}

/// Nested item statements: items declared inside a block are not executed at declaration.
pub fn nested_item_statement() -> i32 {
    {
        // Item statements inside block: struct and function definitions at block scope.
        struct Inner {
            value: i32,
        }
        fn helper(inner: Inner) -> i32 {
            inner.value * 2
        }
        enum LocalChoice {
            A,
            B,
        }
        const LOCAL_CONST: i32 = 6;
        let constructed = Inner { value: LOCAL_CONST };
        let chosen = LocalChoice::A;
        match chosen {
            LocalChoice::A => helper(constructed),
            LocalChoice::B => helper(Inner { value: 0 }),
        }
    }
}

/// Semicolon-sensitive return types: block tail type changes with semicolon.
pub fn semicolon_sensitive() -> (i32, ()) {
    let with_value: i32 = { 8 };
    let with_unit: () = {
        let _ = 8;
    };
    let _flow_semi: i32 = {
        if true {
            1
        } else {
            0
        };
        2
    };
    let _item_after_expr: i32 = {
        struct S;
        let _ = S;
        9
    };
    (with_value, with_unit)
}

/// Specialized blocks: const, unsafe, and async blocks.
pub fn specialized_blocks() -> i32 {
    // Const block (inline const context inside expression).
    let from_const_block: i32 = const { 3 + 4 };

    // Unsafe block.
    let from_unsafe_block: i32 = unsafe {
        let ptr: *const i32 = &from_const_block;
        *ptr
    };

    // Async block.
    let fut = async { 11_i32 };
    // Polling is not required for demonstration; just ensure the block creates a future.

    // Use `fut` to avoid unused warning, check it is Send-ish via size.
    let _ = std::mem::size_of_val(&fut);

    from_const_block + from_unsafe_block
}

/// Tail temporary destruction: temporary created in block tail lives until end of block.
pub fn tail_temporary_scope() -> usize {
    let len = {
        // `String` temporary extended to end of this block in edition 2024 tail scope.
        let s: &str = &String::from("harvest");
        s.len()
    };
    len
}

/// 2024 tail-scope contrast: in edition 2024, tail temporaries live longer than in earlier editions.
/// Demonstrated explicitly beside the 2021 crate which documents the prior behavior.
pub fn tail_scope_2024_demo() -> String {
    // Tail value lives through block; edition 2024 extends temporary lifetime for tail expressions.
    let value = {
        let owned = String::from("plot");
        owned.clone()
    };
    value
}

pub fn demonstrate() -> i32 {
    let _ = value_block();
    let _ = unit_block();
    let _ = nested_item_statement();
    let _ = semicolon_sensitive();
    let _ = specialized_blocks();
    let _ = tail_temporary_scope();
    let _ = tail_scope_2024_demo();
    1
}
