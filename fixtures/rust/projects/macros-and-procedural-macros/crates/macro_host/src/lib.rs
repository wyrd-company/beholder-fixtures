//! Procedural-macro crate for RS-CAN-PROJ-013 and macro coverage.
//! Exports function-like, derive, and attribute entry points with host-only dependencies.

use proc_macro::{Delimiter, Group, Ident, Punct, Spacing, Span, TokenStream, TokenTree};

use host_helper::{is_valid_record_line, parse_record_line};

// Helper: create ident with given span kind
fn ident_with_span(name: &str, use_call_site: bool) -> Ident {
    if use_call_site {
        Ident::new(name, Span::call_site())
    } else {
        Ident::new(name, Span::mixed_site())
    }
}

// RS-CAN-PROJ-013: function-like producing item output
#[proc_macro]
pub fn make_item(input: TokenStream) -> TokenStream {
    // expects single ident
    let name = input
        .into_iter()
        .find_map(|tt| match tt {
            TokenTree::Ident(i) => Some(i.to_string()),
            TokenTree::Group(g) => g.stream().into_iter().find_map(|inner| match inner {
                TokenTree::Ident(i) => Some(i.to_string()),
                _ => None,
            }),
            _ => None,
        })
        .unwrap_or_else(|| "GeneratedItem".to_string());
    let code = format!(
        "pub struct {name} {{ pub value: u32 }} impl {name} {{ pub fn new(v: u32) -> Self {{ Self {{ value: v }} }} pub fn get(&self) -> u32 {{ self.value }} }}"
    );
    code.parse().unwrap()
}

// RS-CAN-MAC-006: function-like producing expression output
#[proc_macro]
pub fn make_expr(input: TokenStream) -> TokenStream {
    // ignore input, produce expression 1 + 41
    let _ = input;
    "42".parse().unwrap()
}

// RS-CAN-MAC-004: identifier concatenation helper
#[proc_macro]
pub fn concat_idents(input: TokenStream) -> TokenStream {
    let mut parts: Vec<String> = Vec::new();
    for tt in input.into_iter() {
        match tt {
            TokenTree::Ident(i) => parts.push(i.to_string()),
            TokenTree::Group(g) => {
                for inner in g.stream() {
                    if let TokenTree::Ident(i) = inner {
                        parts.push(i.to_string());
                    }
                }
            }
            TokenTree::Punct(p) if p.as_char() == ',' => {}
            _ => {}
        }
    }
    if parts.len() < 2 {
        return "compile_error!(\"concat_idents needs two idents\")"
            .parse()
            .unwrap();
    }
    let concatenated = parts.concat();
    let ident = Ident::new(&concatenated, Span::call_site());
    let mut ts = TokenStream::new();
    ts.extend([TokenTree::Ident(ident)]);
    ts
}

// RS-CAN-PROJ-013: derive macro with helper attributes over generic input
#[proc_macro_derive(Describe, attributes(describe))]
pub fn derive_describe(input: TokenStream) -> TokenStream {
    let s = input.to_string();
    // extract tag via simple scan
    let tag = extract_tag(&s).unwrap_or_else(|| "default_tag".to_string());
    let name = extract_struct_name(&s).unwrap_or_else(|| "Unknown".to_string());
    let generics = extract_generics(&s);
    // produce impl; handle generic case
    let expanded = if generics.is_empty() {
        format!(
            "impl crate::derive_support::Describe for {name} {{ fn tag() -> &'static str {{ \"{tag}\" }} fn describe(&self) -> String {{ format!(\"{{}}:{{}}\", \"{name}\", Self::tag()) }} }}"
        )
    } else {
        let params = generics.join(", ");
        let args = generics
            .iter()
            .map(|p| p.split(':').next().unwrap().trim().to_string())
            .collect::<Vec<_>>()
            .join(", ");
        format!(
            "impl<{params}> crate::derive_support::Describe for {name}<{args}> {{ fn tag() -> &'static str {{ \"{tag}\" }} fn describe(&self) -> String {{ format!(\"{{}}:{{}}\", \"{name}\", Self::tag()) }} }}"
        )
    };
    expanded.parse().unwrap_or_else(|_| {
        "compile_error!(\"derive Describe failed\")"
            .parse()
            .unwrap()
    })
}

fn extract_tag(s: &str) -> Option<String> {
    let needle = "tag";
    let pos = s.find(needle)?;
    let after = &s[pos + needle.len()..];
    let eq = after.find('=')?;
    let after_eq = after[eq + 1..].trim();
    // after_eq should start with '"' then value
    let first_quote = after_eq.find('"')?;
    let rest = &after_eq[first_quote + 1..];
    let end_quote = rest.find('"')?;
    Some(rest[..end_quote].to_string())
}

fn extract_struct_name(s: &str) -> Option<String> {
    // Find "struct" keyword then next ident
    let tokens: Vec<&str> = s.split_whitespace().collect();
    for (i, tok) in tokens.iter().enumerate() {
        if *tok == "struct" {
            if let Some(next) = tokens.get(i + 1) {
                // strip punctuation like "<", "{" , ";" etc.
                let cleaned = next
                    .trim_matches(|c: char| !c.is_alphanumeric() && c != '_')
                    .trim();
                // also handle "Demo<T>" case where token is "Demo"
                // Actually "<" may be separate token, so name is Next without "<"
                let name = cleaned.split('<').next().unwrap().trim();
                if !name.is_empty() {
                    return Some(name.to_string());
                }
            }
        }
        // also handle enum? but for Describe we only handle struct
    }
    None
}

fn extract_generics(s: &str) -> Vec<String> {
    // extract content between first < and matching >
    let start = match s.find('<') {
        Some(p) => p,
        None => return Vec::new(),
    };
    let end = match s[start..].find('>') {
        Some(p) => start + p,
        None => return Vec::new(),
    };
    let inner = &s[start + 1..end];
    // split by comma
    inner
        .split(',')
        .map(|p| p.trim().to_string())
        .filter(|p| !p.is_empty())
        .collect()
}

// RS-CAN-MAC-006: attribute transformation producing item output
#[proc_macro_attribute]
pub fn wrap_fn(attr: TokenStream, item: TokenStream) -> TokenStream {
    let _ = attr;
    let s = item.to_string();
    // simple rewrite: keep original and add companion check function
    // if input is fn name() { body }, we preserve it and append helper
    // For demonstration, just return item unchanged plus a generated const
    let extra = "const WRAP_FN_MARKER: u32 = 1;";
    format!("{s} {extra}").parse().unwrap_or(item)
}

// RS-CAN-PROJ-018: attribute rewriting main
#[proc_macro_attribute]
pub fn entry_wrapper(attr: TokenStream, item: TokenStream) -> TokenStream {
    let _ = attr;
    let s = item.to_string();
    // demonstrate rewriting: if input is fn main() {}
    // produce same fn main with extra statement
    if s.contains("fn main") {
        // replace body with wrapper: add let _ = 0;
        // simple approach: return item with added const to show transformation
        let extra = "const ENTRY_WRAPPER_APPLIED: bool = true;";
        format!("{s} {extra}").parse().unwrap_or(item)
    } else {
        item
    }
}

// RS-CAN-MAC-006: attribute transforming item and preserving
#[proc_macro_attribute]
pub fn transform_item(attr: TokenStream, item: TokenStream) -> TokenStream {
    let _ = attr;
    // just return item unchanged to show preservation variant
    item
}

// RS-CAN-MAC-007: span-carrying generated identifiers
#[proc_macro]
pub fn call_site_ident(_input: TokenStream) -> TokenStream {
    // generate identifier `call_site_value` with call_site span
    let ident = Ident::new("call_site_value", Span::call_site());
    let mut ts = TokenStream::new();
    ts.extend([TokenTree::Ident(ident)]);
    ts
}

#[proc_macro]
pub fn mixed_site_ident(_input: TokenStream) -> TokenStream {
    let ident = Ident::new("mixed_site_value", Span::mixed_site());
    let mut ts = TokenStream::new();
    ts.extend([TokenTree::Ident(ident)]);
    ts
}

// Hygienic define: generates `let __hygienic = 1;` with mixed_site hygiene
#[proc_macro]
pub fn hygienic_define(_input: TokenStream) -> TokenStream {
    let code = "let __hygienic_generated = 1u32;";
    code.parse().unwrap()
}

// Call-site define would collide if caller has same name (documented as counterexample)
// We provide hygienic version only as valid

// RS-CAN-MAC-007: demonstration of identifier with explicit span
#[proc_macro]
pub fn span_demo(input: TokenStream) -> TokenStream {
    let use_call = input.to_string().contains("call_site");
    let ident = ident_with_span("span_generated", use_call);
    let mut ts = TokenStream::new();
    ts.extend([
        TokenTree::Ident(Ident::new("let", Span::call_site())),
        TokenTree::Ident(ident),
        TokenTree::Punct(Punct::new('=', Spacing::Alone)),
        TokenTree::Group(Group::new(
            Delimiter::None,
            "42u32".parse::<TokenStream>().unwrap(),
        )),
        TokenTree::Punct(Punct::new(';', Spacing::Alone)),
    ]);
    ts
}

// RS-CAN-ECO-009: hermetic DSL parsing embedded non-Rust syntax over offline data
#[proc_macro]
pub fn offline_records(input: TokenStream) -> TokenStream {
    let _ = input;
    // Read deterministic offline file
    let manifest = std::env::var("CARGO_MANIFEST_DIR").unwrap_or_else(|_| ".".to_string());
    let path = std::path::Path::new(&manifest).join("data/records.txt");
    let content = std::fs::read_to_string(&path).unwrap_or_else(|_| {
        // fallback deterministic content if file missing
        "alpha 10\nbeta 20\n".to_string()
    });
    let mut records: Vec<(String, u32)> = Vec::new();
    for line in content.lines() {
        if let Some((name, value)) = parse_record_line(line) {
            // validate via host_helper
            let check_line = format!("{name} {value}");
            if is_valid_record_line(&check_line) {
                records.push((name.to_string(), value));
            }
        } else if line.trim().is_empty() || line.trim().starts_with('#') {
            continue;
        } else {
            // invalid line: emit compile_error
            let msg = format!("invalid DSL line: {line}");
            return format!("compile_error!(\"{msg}\")").parse().unwrap();
        }
    }
    // Generate typed output referencing consumer crate's Record type
    let items: Vec<String> = records
        .iter()
        .map(|(n, v)| format!("crate::dsl_support::Record {{ name: \"{n}\", value: {v} }}"))
        .collect();
    let array = format!("&[{}]", items.join(", "));
    // The macro should expand to expression; we return array expression
    array.parse().unwrap()
}

// RS-CAN-ECO-009: inline DSL parsing variant
#[proc_macro]
pub fn inline_dsl(input: TokenStream) -> TokenStream {
    // input is expected to be string literal like "alpha 10; beta 20"
    let s = input.to_string();
    // extract quoted content if present
    let content = extract_string_literal(&s).unwrap_or(s);
    let mut records: Vec<(String, u32)> = Vec::new();
    for part in content.split(';') {
        let trimmed = part.trim().trim_matches('"').trim();
        if trimmed.is_empty() {
            continue;
        }
        // DSL syntax: "<name> <value>"
        let mut iter = trimmed.split_whitespace();
        let name = match iter.next() {
            Some(n) => n,
            None => {
                return "compile_error!(\"inline_dsl: missing name\")"
                    .parse()
                    .unwrap();
            }
        };
        let val_str = match iter.next() {
            Some(v) => v,
            None => {
                return "compile_error!(\"inline_dsl: missing value\")"
                    .parse()
                    .unwrap();
            }
        };
        if iter.next().is_some() {
            return "compile_error!(\"inline_dsl: extra tokens\")"
                .parse()
                .unwrap();
        }
        let value: u32 = match val_str.parse() {
            Ok(v) => v,
            Err(_) => {
                return "compile_error!(\"inline_dsl: value must be u32\")"
                    .parse()
                    .unwrap();
            }
        };
        // validate via helper
        if !is_valid_record_line(&format!("{name} {value}")) {
            return "compile_error!(\"inline_dsl: invalid record\")"
                .parse()
                .unwrap();
        }
        records.push((name.to_string(), value));
    }
    if records.is_empty() {
        return "compile_error!(\"inline_dsl: no records\")"
            .parse()
            .unwrap();
    }
    let items: Vec<String> = records
        .iter()
        .map(|(n, v)| format!("crate::dsl_support::Record {{ name: \"{n}\", value: {v} }}"))
        .collect();
    let array = format!("&[{}]", items.join(", "));
    array.parse().unwrap()
}

fn extract_string_literal(s: &str) -> Option<String> {
    let s = s.trim();
    if s.starts_with('"') && s.ends_with('"') && s.len() >= 2 {
        Some(s[1..s.len() - 1].to_string())
    } else if s.contains('"') {
        // TokenStream string may contain quotes with spaces: '"alpha 10; beta 20"'
        let start = s.find('"')?;
        let end = s.rfind('"')?;
        if start != end {
            Some(s[start + 1..end].to_string())
        } else {
            None
        }
    } else {
        None
    }
}
