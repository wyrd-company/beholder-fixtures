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

use std::cell::RefCell;

thread_local! {
    static DROP_LOG: RefCell<Vec<&'static str>> = RefCell::new(Vec::new());
}

struct TailGuard(&'static str);
impl Drop for TailGuard {
    fn drop(&mut self) {
        DROP_LOG.with(|l| l.borrow_mut().push(self.0));
    }
}

struct TempString {
    content: &'static str,
    label: &'static str,
}
impl TempString {
    fn new(content: &'static str, label: &'static str) -> Self {
        Self { content, label }
    }
}
impl Drop for TempString {
    fn drop(&mut self) {
        DROP_LOG.with(|l| l.borrow_mut().push(self.label));
    }
}
impl std::ops::Deref for TempString {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        self.content
    }
}

/// Tail temporary destruction: a temporary created in a block's tail expression has an
/// edition-sensitive drop scope relative to that block's locals.
///
/// The tail temporary is *not* bound to a `let`, so no temporary lifetime extension applies:
/// `TempString::new(..)` is a genuine tail-expression temporary. In edition 2024 the tail
/// temporary is scoped to the block's tail and is dropped *before* the block's locals, so the
/// log is `["tail_temp", "local"]`. In edition 2021 the tail temporary is extended to the end
/// of the enclosing statement and is dropped *after* the block's locals, so the log is
/// `["local", "tail_temp"]`. The 2021 companion crate demonstrates the contrast with identical
/// code compiled under edition 2021.
pub fn tail_temporary_scope() -> Vec<&'static str> {
    DROP_LOG.with(|l| l.borrow_mut().clear());
    let len = {
        let _local = TailGuard("local");
        TempString::new("harvest", "tail_temp").len()
    };
    let _ = len;
    DROP_LOG.with(|l| l.borrow().clone())
}

/// Nested tail-scope (edition 2024): the inner block's tail temporary is dropped before the
/// inner block's own local, producing `["plot_temp", "inner", "outer"]`. As above, the tail
/// temporary is unbound so it is not lifetime-extended.
pub fn tail_scope_2024_demo() -> Vec<&'static str> {
    DROP_LOG.with(|l| l.borrow_mut().clear());
    let outer_len = {
        let _outer = TailGuard("outer");
        let inner_len = {
            let _inner = TailGuard("inner");
            TempString::new("plot", "plot_temp").len()
        };
        inner_len
    };
    let _ = outer_len;
    DROP_LOG.with(|l| l.borrow().clone())
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
