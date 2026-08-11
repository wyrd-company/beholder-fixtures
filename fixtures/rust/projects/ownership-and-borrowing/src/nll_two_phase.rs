//! RS-CAN-OWN-003: Non-lexical lifetimes and two-phase borrows.

/// NLL: mutate after last borrow use in one block.
pub fn nll_mutate_after_last_use() -> Vec<i32> {
    let mut data = vec![1, 2, 3];
    let r = &data;
    let first = r[0];
    let _ = first;
    // Last use of `r` was above; NLL ends borrow before this mutation.
    data.push(4);
    data
}

/// Branch keeping borrow live: in one branch the borrow is used after mutation point,
/// so mutation is not allowed in that path. We demonstrate the valid path where borrow
/// ends before mutation, and the live branch as a separate valid scope.
pub fn nll_branch_live() -> i32 {
    let mut data = vec![10, 20];
    let r = &data;
    let cond = true;
    if cond {
        // Borrow used inside this branch.
        let _ = r[0];
        // Cannot mutate `data` here while `r` is still live in this branch;
        // we avoid mutation in this branch and return instead.
        return r[1];
    }
    // Outside the branch where borrow was not extended, mutation is allowed after NLL.
    // In this function `cond` is true so this path is not taken, but the valid
    // mutation-after-use pattern is shown in `nll_mutate_after_last_use`.
    data.push(30);
    data[0]
}

/// Two-phase borrow: `collection.push(collection.len())` style.
/// The compiler inserts a reserved mutable borrow for `push`'s receiver,
/// evaluates `len()` with a shared borrow, then activates the mutable borrow.
pub fn two_phase_push_len() -> Vec<i32> {
    let mut vec = vec![1, 2, 3];
    // Two-phase: `&mut vec` reserved before `vec.len()` shared borrow, then activated.
    vec.push(vec.len() as i32);
    vec
}

/// Explicit mutable borrowing would be rejected, so we show the accepted
/// two-phase form and the valid explicit workaround.
pub fn two_phase_vs_explicit() -> Vec<i32> {
    let mut vec = vec![5, 6];
    // Valid two-phase autoref:
    vec.push(vec.len() as i32);
    // Valid explicit workaround: evaluate len first, then borrow mutably.
    let len = vec.len() as i32;
    vec.push(len);
    vec
}

/// Explicit `&mut` in argument evaluation is documented as counterexample.
/// The invalid `vec.push(&mut vec)` style or `let r = &mut vec; vec.push(r.len())` pattern
/// would conflict; see `docs/counterexamples.md`.

pub fn nll_two_phase_summary() -> (Vec<i32>, Vec<i32>) {
    let a = nll_mutate_after_last_use();
    let _ = nll_branch_live();
    let b = two_phase_push_len();
    let _ = two_phase_vs_explicit();
    (a, b)
}
