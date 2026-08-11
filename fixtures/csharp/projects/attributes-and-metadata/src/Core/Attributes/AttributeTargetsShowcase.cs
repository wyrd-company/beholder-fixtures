namespace Fixture.AttributesAndMetadata.Core.Attributes;

/// <summary>
/// Applies <see cref="ShowcaseAttribute"/> to every ordinary declaration
/// target reachable from a single class: the type itself, a field, an
/// auto-property and its backing field, a constructor and its parameter, a
/// method, its return value and parameter, an event and its add/remove
/// accessors, an indexer and its get/set accessors, and a generic method
/// with a generic parameter.
/// </summary>
[Showcase("class-target")]
public class AttributeTargetShowcase
{
    [Showcase("field-target")]
    private readonly int _value;

    [field: Showcase("backing-field-target")]
    public int AutoProperty { get; set; }

    [Showcase("property-target")]
    public string Name { get; set; } = string.Empty;

    [Showcase("constructor-target")]
    public AttributeTargetShowcase([Showcase("parameter-target")] int value)
    {
        _value = value;
    }

    [return: Showcase("return-target")]
    [Showcase("method-target", Tags = new[] { "math", "pure" }, Correlate = typeof(AttributeTargetShowcase))]
    public int Compute([Showcase("parameter-target-secondary")] int input) => input + _value;

    public event EventHandler? Updated
    {
        [Showcase("add-accessor-target")]
        add => _updated += value;
        [Showcase("remove-accessor-target")]
        remove => _updated -= value;
    }

    private EventHandler? _updated;

    public int Indexed
    {
        [Showcase("get-accessor-target")]
        get => _value;
        [Showcase("set-accessor-target")]
        set { }
    }

    [Showcase("generic-method-target")]
    public T Identity<[Showcase("generic-parameter-target")] T>(T input) => input;
}

[Showcase("generic-class-target")]
public class ShowcaseGeneric<[Showcase("class-generic-parameter-target")] T>
{
    public T? Value { get; set; }
}

[Showcase("interface-target")]
public interface IShowcaseContract
{
    [Showcase("interface-method-target")]
    void Act();
}

[Showcase("struct-target")]
public struct ShowcaseStruct
{
    [Showcase("struct-field-target")]
    public int Number;
}

[Showcase("enum-target")]
public enum ShowcaseEnum
{
    [Showcase("enum-member-target")]
    First,
    Second,
}

[Showcase("delegate-target")]
public delegate void ShowcaseDelegate([Showcase("delegate-parameter-target")] int value);

/// <summary>
/// Applies the generic <see cref="AssociatedTypeAttribute{T}"/> (a C# 11+
/// generic attribute) to a type.
/// </summary>
[AssociatedType<ShowcaseStruct>(Note = "generic-attribute-target")]
public class GenericAttributeConsumer
{
}

/// <summary>
/// Applies attribute target specifiers to a record's primary-constructor
/// parameter, forwarding one written attribute application to three distinct
/// synthesized/declared targets: the constructor parameter, the generated
/// property, and the generated backing field.
/// </summary>
public record ShowcaseRecord(
    [property: Showcase("record-property-target")]
    [field: Showcase("record-field-target")]
    [param: Showcase("record-param-target")]
    int Value);

/// <summary>
/// Applies <see cref="InheritedMarkerAttribute"/> and
/// <see cref="NonInheritedMarkerAttribute"/> to a base class so reflection
/// can contrast inherited-vs-non-inherited custom attribute lookup on a
/// derived class.
/// </summary>
[InheritedMarker]
[NonInheritedMarker]
public class InheritanceMarkerBase
{
}

public class InheritanceMarkerDerived : InheritanceMarkerBase
{
}
