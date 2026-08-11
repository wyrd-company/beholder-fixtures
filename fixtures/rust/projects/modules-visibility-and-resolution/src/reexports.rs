//! RS-CAN-MOD-007: pub use re-exports, renames, glob exports, re-exported dependency type.

pub mod implementation {
    pub struct InternalType {
        pub value: u32,
    }

    impl InternalType {
        pub fn new(v: u32) -> Self {
            Self { value: v }
        }
    }

    pub fn internal_fn() -> u32 {
        70
    }

    pub const INTERNAL_CONST: u32 = 700;

    #[macro_export]
    macro_rules! internal_macro {
        () => {
            701
        };
    }

    pub trait InternalTrait {
        fn method(&self) -> u32;
    }

    impl InternalTrait for InternalType {
        fn method(&self) -> u32 {
            self.value
        }
    }
}

// Private containing module `implementation` holds public items; we bypass via public re-exports at crate root or public module.
pub use crate::reexports::implementation::INTERNAL_CONST;
pub use crate::reexports::implementation::InternalType;
pub use crate::reexports::implementation::internal_fn;

// Rename re-export.
pub use crate::reexports::implementation::InternalType as RenamedType;

// Glob export selected items.
pub use crate::reexports::implementation::*;

// Dependency type re-export.
pub use fixture_direct::DirectType as ReexportedDirectType;
pub use fixture_direct::TransitiveType as ReexportedTransitiveType;

// Re-export chain: module re-exports then root re-exports again.
pub mod reexport_chain_mid {
    pub use crate::reexports::implementation::InternalType as ChainType;
}

pub use crate::reexports::reexport_chain_mid::ChainType;

// Multiple public paths to same entity: `InternalType` is reachable as:
// - `crate::reexports::implementation::InternalType` (original, private container but public item)
// - `crate::reexports::InternalType` (first re-export)
// - `crate::reexports::RenamedType` (rename)
// - `crate::reexports::ChainType` (chain)
// All share identity.

pub fn reexport_identity_demo() -> u32 {
    let a: InternalType = InternalType::new(1);
    let b: RenamedType = RenamedType::new(2);
    let c: ChainType = ChainType::new(3);
    let d: ReexportedDirectType = ReexportedDirectType::new(4);
    // Original path still reachable if implementation module were public, but it's public here.
    // All distinct variables hold same underlying definition identity.
    a.value + b.value + c.value + d.value + internal_fn() + INTERNAL_CONST
}

// Macro re-export.
pub use crate::internal_macro;

// Glob re-export variant already covered via `pub use implementation::*`.
