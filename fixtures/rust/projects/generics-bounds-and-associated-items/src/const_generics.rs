// RS-CAN-GEN-003: const parameters of integer, boolean, and character types
// with distinct instantiations and compile-time use.

/// Integer const generic (usize, stable).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Buffer<const N: usize> {
    pub data: [u8; N],
}

impl<const N: usize> Buffer<N> {
    pub fn new(value: u8) -> Self {
        Self { data: [value; N] }
    }

    pub fn len(&self) -> usize {
        N
    }

    /// Compile-time use of N in const context.
    pub const fn capacity() -> usize {
        N
    }
}

/// Boolean const generic.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Flag<const ENABLED: bool>;

impl<const ENABLED: bool> Flag<ENABLED> {
    pub fn describe() -> &'static str {
        if ENABLED { "enabled" } else { "disabled" }
    }

    pub const fn is_enabled() -> bool {
        ENABLED
    }
}

/// Character const generic (stable since 1.97? char as const param is stable).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Tag<const C: char>;

impl<const C: char> Tag<C> {
    pub fn char_value() -> char {
        C
    }

    pub const fn as_char() -> char {
        C
    }
}

/// Function parameterized by integer const.
pub fn repeat<const N: usize>(value: u8) -> [u8; N] {
    [value; N]
}

/// Function with boolean const generic.
pub fn gated<const B: bool>(value: u32) -> u32 {
    if B { value * 2 } else { value }
}

/// Function with character const generic.
pub fn char_identity<const C: char>() -> char {
    C
}

/// Distinct instantiations show different types.
pub fn distinct_instantiations() {
    let a: Buffer<4> = Buffer::new(1);
    let b: Buffer<8> = Buffer::new(2);
    let _c: Flag<true> = Flag;
    let _d: Flag<false> = Flag;
    let _e: Tag<'A'> = Tag;
    let _f: Tag<'Z'> = Tag;
    let _ = (a.len(), b.len());
    let _ = (Flag::<true>::describe(), Flag::<false>::describe());
    let _ = (Tag::<'A'>::char_value(), Tag::<'Z'>::char_value());
    let arr4: [u8; 4] = repeat::<4>(7);
    let arr8: [u8; 8] = repeat::<8>(7);
    let enabled = gated::<true>(10);
    let disabled = gated::<false>(10);
    let ch_a = char_identity::<'A'>();
    let ch_z = char_identity::<'Z'>();
    let _ = (arr4, arr8, enabled, disabled, ch_a, ch_z);
}

/// Inferred const arguments and explicit braces.
pub fn const_inference_demo() {
    // Inferred from expected type.
    let buf: Buffer<2> = Buffer::new(5);
    let _ = buf;
    // Explicit turbofish.
    let _explicit = Buffer::<3>::new(9);
    // Braces form for const expression (uses generic const expr in type).
    let _braced: Buffer<4> = Buffer::<{ 2 + 2 }>::new(1);
}

/// Compile-time use: const generic in const evaluation and array length.
pub const fn doubled<const N: usize>() -> usize {
    N * 2
}

pub fn compile_time_use<const N: usize>() -> [u8; N] {
    [0u8; N]
}

pub fn compile_time_doubled<const N: usize>() -> usize {
    doubled::<N>()
}

/// Demonstrates explicit vs inferred and braces usage together.
pub fn brace_form_demo() {
    let _a: [u8; 3] = compile_time_use::<3>();
    let doubled = compile_time_doubled::<3>();
    let _ = doubled;
    let _b: Buffer<{ 1 + 3 }> = Buffer::new(0);
}

/// Array parameterized by const with equality check via const fn.
pub fn const_equality<const N: usize, const M: usize>() -> bool
where
    [(); N]: Sized,
    [(); M]: Sized,
{
    // Use const equality indirectly; distinct N and M produce distinct types.
    N == M
}

pub fn const_generics_summary() -> &'static str {
    "const_generics"
}
