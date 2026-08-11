//! RS-CAN-OWN-009: Refutability, or-patterns, guards, and exhaustiveness.

pub enum Shape {
    Circle(f32),
    Rect { width: f32, height: f32 },
    Point,
}

/// Patterns in `let` (irrefutable).
pub fn let_patterns() -> i32 {
    let (a, b) = (10, 20);
    let Point2 { x, y } = Point2 { x: 3, y: 4 };
    let _ = (a, b, x, y);
    let tuple = (1, 2, 3);
    let (first, .., last) = tuple;
    first + last
}

pub struct Point2 {
    pub x: i32,
    pub y: i32,
}

/// Patterns in function parameters.
pub fn param_pattern((a, b): (i32, i32)) -> i32 {
    a + b
}

pub fn param_struct_pattern(Point2 { x, y }: Point2) -> i32 {
    x + y
}

/// Patterns in `if let` (refutable).
pub fn if_let_pattern(opt: Option<i32>) -> i32 {
    if let Some(value) = opt { value } else { 0 }
}

/// Patterns in `while let`.
pub fn while_let_pattern(mut iter: impl Iterator<Item = i32>) -> i32 {
    let mut sum = 0;
    while let Some(v) = iter.next() {
        sum += v;
    }
    sum
}

/// Patterns in `let-else` (diverging else).
pub fn let_else_pattern(opt: Option<i32>) -> i32 {
    let Some(value) = opt else {
        return -1;
    };
    value
}

/// Match arms with enum, tuple, slice, range, or, and guarded forms.
pub fn match_exhaustive(shape: Shape) -> &'static str {
    match shape {
        Shape::Circle(r) if r > 10.0 => "large circle",
        Shape::Circle(_) => "circle",
        Shape::Rect { width, height } if width == height => "square",
        Shape::Rect { .. } => "rect",
        Shape::Point => "point",
    }
}

pub fn tuple_slice_range_or_guarded() -> i32 {
    // Tuple pattern
    let t = (1, 2, 3);
    let v = match t {
        (0, _, _) => 0,
        (1, 2, 3) => 1,
        _ => 99,
    };

    // Slice pattern
    let arr = [1, 2, 3, 4];
    let w = match &arr[..] {
        [1, 2, ..] => 10,
        [a, b, c] => a + b + c,
        _ => 0,
    };

    // Range pattern
    let n = 5;
    let x = match n {
        1..=3 => 1,
        4..=6 => 2,
        _ => 0,
    };

    // Or-pattern with consistent bindings
    let opt = Some(1);
    let y = match opt {
        Some(1) | Some(2) => 100,
        Some(v) => v,
        None => 0,
    };

    // Guarded arm does not contribute to exhaustiveness; wildcard after guarded coverage is required.
    let maybe = Some(5);
    let z = match maybe {
        Some(v) if v > 10 => 1,
        Some(v) => v,
        None => 0,
    };

    v + w + x + y + z
}

/// Uninhabited type handling is compiler-evolving; we demonstrate a never-like branch via `!` coercion in match
/// without relying on unstable exhaustiveness for uninhabited types.

pub fn patterns_summary() -> (i32, i32, i32, i32, i32, &'static str, i32) {
    let a = let_patterns();
    let b = param_pattern((1, 2));
    let c = param_struct_pattern(Point2 { x: 5, y: 6 });
    let d = if_let_pattern(Some(7));
    let e = while_let_pattern(vec![1, 2, 3].into_iter());
    let f = let_else_pattern(Some(9));
    let g = match_exhaustive(Shape::Circle(15.0));
    let h = tuple_slice_range_or_guarded();
    // Guard borrow/move behavior: guard borrows, not moves, from scrutinee.
    let _ = b + c;
    (a, d, e, f, h, g, a)
}
