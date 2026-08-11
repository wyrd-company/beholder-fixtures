//! Fixture for Rust type forms, layout, and conversions.
//! Covers RS-CAN-TYPE-001 through RS-CAN-TYPE-016.

pub mod alias_newtype;
pub mod casts;
pub mod coercions;
pub mod dst;
pub mod enum_forms;
pub mod fn_closure;
pub mod impl_trait;
pub mod impl_trait_in_traits;
pub mod inference;
pub mod primitive_tuple_array;
pub mod recursive;
pub mod references_pointers;
pub mod repr_layout;
pub mod struct_forms;
pub mod trait_objects;
pub mod unions;

pub use types_layout_downstream as downstream;

/// Aggregated demonstration entry that touches each module so that
/// build and lint observe reachable valid code.
pub fn fixture_overview() -> &'static str {
    // Struct forms.
    let _ = struct_forms::named_example();
    let _ = struct_forms::tuple_example();
    struct_forms::update_examples();
    struct_forms::destructure_examples();
    struct_forms::constructor_as_value();
    struct_forms::zst_and_phantom();
    struct_forms::cross_crate_visibility();

    // Enum forms.
    enum_forms::construction_and_import();
    let _ = enum_forms::discriminant_observation();
    let _ = enum_forms::exhaustive_matching(enum_forms::Shaped::Unit);
    let _ = enum_forms::cross_crate_exhaustive(downstream::ExternalChoice::Alpha);

    // Unions.
    unions::safe_writes();
    let _ = unions::unsafe_reads();
    let _ = unions::union_pattern_match();

    // Alias vs newtype.
    let _ = alias_newtype::alias_coherence_and_methods();

    // Primitive/tuple/array.
    primitive_tuple_array::tuple_forms();
    primitive_tuple_array::array_and_slice_coercion();
    primitive_tuple_array::string_and_byte_forms();
    let _ = primitive_tuple_array::diverging_branch(true);

    // References.
    references_pointers::shared_and_mutable_refs();
    references_pointers::raw_formation_and_deref();

    // Function items / closures.
    fn_closure::function_items_and_pointers();
    fn_closure::closures_and_coercions();

    // DST.
    dst::unsizing_examples();
    dst::pointer_metadata_examples();
    dst::trailing_slice_access();

    // Trait objects.
    trait_objects::trait_object_bindings();
    trait_objects::upcasting_demo();

    // Impl Trait.
    let _ = impl_trait::takes_impl("demo");
    let _ = impl_trait::takes_generic("demo");
    let _ = impl_trait::make_iter().count();

    // Impl Trait in traits.
    let field = impl_trait_in_traits::Field {
        rows: vec!["a".to_string()],
    };
    let _ = impl_trait_in_traits::generic_calls(&field);

    // Recursive.
    recursive::recursive_examples();

    // Repr/layout.
    repr_layout::layout_observations();
    repr_layout::packed_access_examples();
    repr_layout::ffi_crossing_example();

    // Inference.
    inference::explicit_and_turbofish();
    inference::numeric_fallback();

    // Coercions.
    coercions::function_and_closure_coercions();
    coercions::deref_and_unsizing();

    // Casts.
    casts::cast_coverage_probe();

    "types-and-layout"
}
