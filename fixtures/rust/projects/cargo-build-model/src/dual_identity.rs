//! RS-CAN-PROJ-001: package vs target vs crate identity, one source compiled under two crate identities.
//! This module re-exports the shared source to show crate-identity distinction.

pub use crate::shared_identity::{SharedType, shared_fn};

// Binary vs library import demonstration is in `src/bin/cargo_build_model_bin.rs`:
// Two ways to reach the shared source:
// 1. As external crate: `use cargo_build_model::shared_identity::SharedType`
// 2. As local mod: `#[path = "../shared_identity.rs"] mod local_shared;`
// These produce distinct types that do not unify despite identical source text.
