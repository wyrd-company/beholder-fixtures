// RS-CAN-MOD-012: item and local scopes, forward reference, shadowing with changed type, nested items vs closure capture.

// Forward reference: call item before its textual declaration.
pub fn forward_caller() -> u32 {
    forward_declared_fn()
}

pub fn forward_declared_fn() -> u32 {
    123
}

// Item scope: declarations cover enclosing module regardless of order.
pub struct ForwardType;

impl ForwardType {
    pub fn uses_later_item() -> u32 {
        later_const()
    }
}

pub fn later_const() -> u32 {
    456
}

// Local shadowing with changed type.
pub fn shadowing_demo() -> u32 {
    let x = 10u32;
    let x = "hello"; // shadows with different type
    let x = x.len() as u32; // again shadowing with new type
    x
}

// Shadowing in nested blocks.
pub fn shadowing_block() -> u32 {
    let v = 1;
    {
        let v = 2.5f64;
        assert!((v - 2.5).abs() < f64::EPSILON);
    }
    v
}

// Guard/arm binding scope demonstration.
pub fn guard_scope_demo(opt: Option<u32>) -> u32 {
    match opt {
        Some(x) if x > 5 => x,
        Some(x) => x,
        None => 0,
    }
}

pub trait BodyLocalTrait {
    fn body_method(&self) -> u32;
}

pub struct BodyLocalType(pub u32);

// Nested items vs closure capture.
pub fn nested_items_vs_closure() -> u32 {
    let outer_value = 10;

    fn nested_function(param: u32) -> u32 {
        param + 5
    }

    let _from_fn = nested_function(7);

    let captured = outer_value;
    let closure = |x: u32| x + captured;

    struct InnerType {
        v: u32,
    }

    // Nested impl for `InnerType` inside function body.
    impl InnerType {
        fn inner_method(&self) -> u32 {
            self.v + 1
        }
    }

    // Body-local trait impl – coherence is crate-global despite textual locality.
    impl BodyLocalTrait for BodyLocalType {
        fn body_method(&self) -> u32 {
            self.0 + 100
        }
    }

    trait LocalInnerTrait {
        fn local_trait_fn(&self) -> u32;
    }

    impl LocalInnerTrait for InnerType {
        fn local_trait_fn(&self) -> u32 {
            self.v + 2
        }
    }

    mod inner_body_mod {
        pub fn body_mod_fn() -> u32 {
            77
        }
    }

    use crate::scopes_shadowing::forward_declared_fn as aliased_import;

    let inner = InnerType { v: 20 };
    let from_inner = inner.inner_method();
    let from_trait = inner.local_trait_fn();
    let from_mod = inner_body_mod::body_mod_fn();
    let from_import = aliased_import();
    // Body-local impl for `BodyLocalType` is visible here and also outside the function (crate-global).
    let body_local = BodyLocalType(5).body_method();

    closure(3) + from_inner + from_trait + from_mod + from_import + body_local
}

pub fn body_local_impl_visible_outside() -> u32 {
    // `BodyLocalTrait` impl for `BodyLocalType` was defined inside `nested_items_vs_closure`, yet visible here – coherence is not limited to textual scope.
    BodyLocalType(10).body_method()
}

// Body-local import does not leak beyond function.
pub fn body_local_import_leakage() -> u32 {
    {
        use crate::scopes_shadowing::forward_declared_fn;
        return forward_declared_fn();
    }
}

// Generic scope and label scope.
pub fn generic_and_label_scope() -> u32 {
    fn generic_fn<T>(x: T) -> T
    where
        T: Clone,
    {
        x.clone()
    }

    let y = generic_fn(42u32);

    let mut result = 0;
    'outer: loop {
        'inner: loop {
            result = 1;
            break 'outer;
        }
    }

    let _ = result;
    y
}
