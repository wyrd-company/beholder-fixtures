pub use unify_shared::active_features;
pub fn consumer_b_feature() -> &'static str {
    unify_shared::active_features()
}
