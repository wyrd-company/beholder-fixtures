use hyphen_crate_lib::{HyphenType, library_fn};

fn main() {
    let v: HyphenType = library_fn();
    println!("hyphen-executable v02: {}", v.0);
}
