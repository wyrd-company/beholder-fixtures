//! RS-CAN-TRAIT-005 — receiver forms and stable self-type boundaries.

use std::pin::Pin;

/// Type demonstrating all stable receiver forms.
pub struct ReceiverDemo {
    pub value: i32,
}

impl ReceiverDemo {
    /// `self` by value (consuming).
    pub fn consume(self) -> i32 {
        self.value
    }

    /// `&self` shared borrow.
    pub fn borrow(&self) -> i32 {
        self.value
    }

    /// `&mut self` exclusive borrow.
    pub fn borrow_mut(&mut self) -> i32 {
        self.value += 1;
        self.value
    }

    /// `Box<Self>` self type.
    #[allow(clippy::boxed_local)]
    pub fn boxed(self: Box<Self>) -> i32 {
        self.value
    }

    /// `Pin<&mut Self>` self type.
    pub fn pinned(self: Pin<&mut Self>) -> i32 {
        self.value
    }

    /// No receiver (associated function).
    pub fn associated() -> &'static str {
        "associated"
    }

    /// Additional associated function to show multiple.
    pub fn with_value(value: i32) -> Self {
        Self { value }
    }
}

/// Trait with varied receiver forms, dyn-compatible where `Self: Sized` marks consuming methods.
pub trait ReceiverTrait {
    fn consume(self) -> i32
    where
        Self: Sized;
    fn borrow(&self) -> i32;
    fn borrow_mut(&mut self) -> i32;
    #[allow(clippy::boxed_local)]
    fn boxed(self: Box<Self>) -> i32
    where
        Self: Sized;
    fn pinned(self: Pin<&mut Self>) -> i32;
    fn associated() -> &'static str
    where
        Self: Sized;
}

impl ReceiverTrait for ReceiverDemo {
    fn consume(self) -> i32
    where
        Self: Sized,
    {
        self.value
    }

    fn borrow(&self) -> i32 {
        self.value
    }

    fn borrow_mut(&mut self) -> i32 {
        self.value += 10;
        self.value
    }

    #[allow(clippy::boxed_local)]
    fn boxed(self: Box<Self>) -> i32
    where
        Self: Sized,
    {
        self.value * 2
    }

    fn pinned(self: Pin<&mut Self>) -> i32 {
        self.value
    }

    fn associated() -> &'static str
    where
        Self: Sized,
    {
        "trait-associated"
    }
}

pub fn receivers_summary() -> i32 {
    let mut r = ReceiverDemo { value: 1 };
    let _ = r.borrow();
    let _ = r.borrow_mut();
    let boxed = Box::new(ReceiverDemo { value: 2 });
    let _ = boxed.boxed();
    let pinned_val = ReceiverDemo { value: 3 };
    let mut pinned = Box::pin(pinned_val);
    // Need mutable Pin borrow: get mutable ref to pinned data
    let _ = ReceiverDemo::pinned(Pin::as_mut(&mut pinned));
    let consumed = ReceiverDemo { value: 4 }.consume();
    let _ = ReceiverDemo::associated();
    let _ = <ReceiverDemo as ReceiverTrait>::associated();
    consumed
}
