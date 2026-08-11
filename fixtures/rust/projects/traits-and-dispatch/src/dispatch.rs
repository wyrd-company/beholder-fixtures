//! RS-CAN-TRAIT-008 — static and dynamic dispatch.

pub trait Drawable {
    fn draw(&self) -> String;
}

pub struct Circle(pub f64);
pub struct Square(pub f64);
pub struct Triangle;

impl Drawable for Circle {
    fn draw(&self) -> String {
        format!("Circle({})", self.0)
    }
}

impl Drawable for Square {
    fn draw(&self) -> String {
        format!("Square({})", self.0)
    }
}

impl Drawable for Triangle {
    fn draw(&self) -> String {
        "Triangle".to_owned()
    }
}

/// Generic static dispatch (monomorphized).
pub fn draw_generic<T: Drawable>(item: &T) -> String {
    item.draw()
}

/// `impl Trait` argument position (static dispatch).
pub fn draw_impl_trait(item: impl Drawable) -> String {
    item.draw()
}

/// `&dyn Trait` dynamic dispatch.
pub fn draw_dyn(item: &dyn Drawable) -> String {
    item.draw()
}

/// Boxed trait object dynamic dispatch.
pub fn draw_boxed(item: Box<dyn Drawable>) -> String {
    item.draw()
}

/// Heterogeneous collection of boxed trait objects.
pub fn draw_collection(items: Vec<Box<dyn Drawable>>) -> Vec<String> {
    items.iter().map(|i| i.draw()).collect()
}

pub fn dispatch_summary() -> Vec<String> {
    let c = Circle(1.0);
    let s = Square(2.0);
    let generic = draw_generic(&c);
    let impl_trait = draw_impl_trait(Square(3.0));
    let dyned: &dyn Drawable = &s;
    let dyn_result = draw_dyn(dyned);
    let boxed = draw_boxed(Box::new(Circle(4.0)));
    let collection = draw_collection(vec![
        Box::new(Circle(5.0)),
        Box::new(Square(6.0)),
        Box::new(Triangle),
    ]);
    let mut out = vec![generic, impl_trait, dyn_result, boxed];
    out.extend(collection);
    out
}
