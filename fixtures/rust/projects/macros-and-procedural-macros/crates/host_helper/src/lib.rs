//! Host-only helper used exclusively by the procedural-macro crate.
//! Demonstrates RS-CAN-PROJ-013 host-only dependency isolation.

/// Validate DSL record syntax deterministically.
pub fn is_valid_record_line(line: &str) -> bool {
    let trimmed = line.trim();
    if trimmed.is_empty() || trimmed.starts_with('#') {
        return false;
    }
    let parts: Vec<&str> = trimmed.split_whitespace().collect();
    if parts.len() != 2 {
        return false;
    }
    parts[1].parse::<u32>().is_ok()
}

/// Parse a record line into name and value.
pub fn parse_record_line(line: &str) -> Option<(&str, u32)> {
    let trimmed = line.trim();
    if trimmed.is_empty() || trimmed.starts_with('#') {
        return None;
    }
    let mut parts = trimmed.split_whitespace();
    let name = parts.next()?;
    let value_str = parts.next()?;
    if parts.next().is_some() {
        return None;
    }
    let value = value_str.parse::<u32>().ok()?;
    Some((name, value))
}

/// Format helper for $crate demonstration.
pub fn helper_value() -> u32 {
    42
}
