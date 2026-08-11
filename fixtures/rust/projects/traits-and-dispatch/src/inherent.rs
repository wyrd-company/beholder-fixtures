//! RS-CAN-TRAIT-001 — inherent impls split across modules and private trait impl.

/// Nominal type for inherent and trait impl demonstration.
pub struct Widget {
    pub id: u32,
    pub name: String,
}

/// Global trait for widget description. Defined at crate root via re-export
/// so the private impl module can implement it.
pub trait WidgetDescribe {
    fn describe(&self) -> String;
    fn label(&self) -> String;
}

mod inherent_primary {
    use super::Widget;

    impl Widget {
        /// First inherent block, defined in its own module.
        pub fn new(id: u32, name: &str) -> Self {
            Self {
                id,
                name: name.to_owned(),
            }
        }

        pub fn id(&self) -> u32 {
            self.id
        }

        /// Inherent method that shares a name with a trait method.
        pub fn label(&self) -> String {
            format!("widget#{}:{}", self.id, self.name)
        }
    }
}

mod inherent_secondary {
    use super::Widget;

    impl Widget {
        /// Second inherent block in a separate module.
        pub fn with_suffix(mut self, suffix: &str) -> Self {
            self.name.push_str(suffix);
            self
        }

        pub fn name_len(&self) -> usize {
            self.name.len()
        }
    }
}

mod private_trait_impl {
    use super::{Widget, WidgetDescribe};

    impl WidgetDescribe for Widget {
        fn describe(&self) -> String {
            format!("Describe({},{})", self.id, self.name)
        }

        fn label(&self) -> String {
            format!("trait-label:{}:{}", self.id, self.name)
        }
    }

    pub fn private_impl_used_locally(widget: &Widget) -> String {
        widget.describe()
    }
}

pub use private_trait_impl::private_impl_used_locally;

/// Demonstrates that the trait impl in a private module is globally available
/// without importing that module.
pub fn inherent_summary(widget: &Widget) -> (u32, String, String, String) {
    let id = widget.id();
    let inherent_label = widget.label();
    let trait_describe = widget.describe();
    let trait_label = WidgetDescribe::label(widget);
    (id, inherent_label, trait_describe, trait_label)
}

/// Validates that inherent and trait methods with the same spelling coexist.
pub fn same_spelling_demo() -> String {
    let w = Widget::new(7, "demo");
    let inherent = w.label();
    let via_trait = <Widget as WidgetDescribe>::label(&w);
    format!("{inherent}|{via_trait}")
}
