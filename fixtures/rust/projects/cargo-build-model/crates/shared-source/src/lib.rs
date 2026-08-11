pub struct SharedType(pub u32);
pub fn shared_fn() -> SharedType {
    SharedType(99)
}
pub const SOURCE: &str = "shared-source";
