use hyphen_crate_lib::{library_fn, HyphenType};

fn main() {
    let v: HyphenType = library_fn();
    println!("hyphen-executable v03: {}", v.0);
}
