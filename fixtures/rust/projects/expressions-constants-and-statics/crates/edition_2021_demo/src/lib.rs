//! Edition 2021 contrast: temporary scope and `if let` / let-chain availability.
//!
//! On edition 2021, let chains are not available (require edition 2024).
//! This crate documents the 2021 behavior and provides a valid analogue.

use std::cell::RefCell;

thread_local! {
    static IF_LET_LOG: RefCell<Vec<&'static str>> = RefCell::new(Vec::new());
}

struct IfLetScrutinee(&'static str);
impl Drop for IfLetScrutinee {
    fn drop(&mut self) {
        IF_LET_LOG.with(|l| l.borrow_mut().push(self.0));
    }
}

/// `if let` with temporary scope as handled in edition 2021.
///
/// Identical code to the 2024 `if_let_temporary_scope` above, but compiled as
/// edition 2021 the `Scrutinee("scrutinee")` temporary is dropped immediately
/// after the condition, before the then-branch body. The log order differs from
/// the 2024 crate, exposing the rescoping contrast.
pub fn if_let_temporary_scope_2021() -> Vec<&'static str> {
    IF_LET_LOG.with(|l| l.borrow_mut().clear());
    let result = if let Some(s) = Some(IfLetScrutinee("scrutinee")).as_ref() {
        IF_LET_LOG.with(|l| l.borrow_mut().push("then"));
        Some(s.0.len())
    } else {
        IF_LET_LOG.with(|l| l.borrow_mut().push("else"));
        None
    };
    let _ = result;
    IF_LET_LOG.with(|l| l.borrow_mut().push("after"));
    IF_LET_LOG.with(|l| l.borrow().clone())
}

/// Traditional `if let` chain alternative without `&&` let chain syntax.
///
/// On edition 2021, the let-chain `if let Some(x) = a && let Some(y) = b` is not valid.
/// Equivalent nesting is used instead.
pub fn nested_if_let_alternative(a: Option<i32>, b: Option<i32>) -> Option<i32> {
    if let Some(x) = a {
        if let Some(y) = b {
            return Some(x + y);
        }
    }
    None
}

use std::cell::RefCell as TailRefCell;

thread_local! {
    static TAIL_DROP_LOG: TailRefCell<Vec<&'static str>> = TailRefCell::new(Vec::new());
}

struct TailGuard(&'static str);
impl Drop for TailGuard {
    fn drop(&mut self) {
        TAIL_DROP_LOG.with(|l| l.borrow_mut().push(self.0));
    }
}

struct TempString2021 {
    content: &'static str,
    label: &'static str,
}
impl TempString2021 {
    fn new(content: &'static str, label: &'static str) -> Self {
        Self { content, label }
    }
}
impl Drop for TempString2021 {
    fn drop(&mut self) {
        TAIL_DROP_LOG.with(|l| l.borrow_mut().push(self.label));
    }
}
impl std::ops::Deref for TempString2021 {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        self.content
    }
}

/// Tail temporary scope analogue in edition 2021.
///
/// Identical structure to `blocks::tail_temporary_scope` but compiled as edition 2021.
/// The `TempString2021("tail_temp")` tail temporary is destroyed at a different point
/// than in the 2024 crate, so the returned log order exposes the edition-specific drop scope.
pub fn tail_temporary_2021() -> Vec<&'static str> {
    TAIL_DROP_LOG.with(|l| l.borrow_mut().clear());
    let len = {
        let _local = TailGuard("local");
        let s: &str = &TempString2021::new("harvest", "tail_temp");
        s.len()
    };
    let _ = len;
    TAIL_DROP_LOG.with(|l| l.borrow().clone())
}

pub fn demonstrate() -> i32 {
    let _ = if_let_temporary_scope_2021();
    let _ = nested_if_let_alternative(Some(1), Some(2));
    let _ = tail_temporary_2021();
    1
}
