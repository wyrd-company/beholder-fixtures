//! Proc-macro derive helpers for attribute fixture coverage.

use proc_macro::TokenStream;

/// Derive macro with registered helper attribute namespace `demo_helper`.
#[proc_macro_derive(DemoDerive, attributes(demo_helper))]
pub fn demo_derive(input: TokenStream) -> TokenStream {
    let type_name =
        extract_type_name(&input.to_string()).unwrap_or_else(|| "FixtureType".to_string());
    format!(
        "impl {type_name} {{ pub fn demo_marker(&self) -> &'static str {{ \"demo_derive\" }} }}"
    )
    .parse()
    .unwrap_or_else(|_| TokenStream::new())
}

/// Registered tool attribute namespace for the fixture proc-macro crate.
#[proc_macro_attribute]
pub fn fixture_tool(_attr: TokenStream, item: TokenStream) -> TokenStream {
    item
}

fn extract_type_name(input: &str) -> Option<String> {
    let tokens: Vec<&str> = input.split_whitespace().collect();
    for index in 0..tokens.len().saturating_sub(1) {
        if matches!(tokens[index], "struct" | "enum" | "union") {
            let name = tokens[index + 1];
            let cleaned = name.trim_end_matches(|character: char| {
                !character.is_ascii_alphanumeric() && character != '_'
            });
            return Some(cleaned.to_string());
        }
    }
    None
}
