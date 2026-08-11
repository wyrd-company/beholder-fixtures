using System.Reflection;
using System.Runtime.CompilerServices;
using Fixture.AttributesAndMetadata.Core.Recognized;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

/// <summary>
/// Reflects over an auto-property's compiler-generated backing field and a
/// property's accessor methods. The backing field is identified only by the
/// presence of <see cref="CompilerGeneratedAttribute"/> and its declared
/// type, never by its synthesized name, per CS-CAN-125.
/// </summary>
public static class BackingFieldAndAccessorObservation
{
    public static string DescribeAutoPropertyBackingField()
    {
        var field = typeof(RequiredMembersShowcase)
            .GetFields(BindingFlags.NonPublic | BindingFlags.Instance)
            .SingleOrDefault(f => f.IsDefined(typeof(CompilerGeneratedAttribute), false) && f.FieldType == typeof(string));

        return field is null
            ? "no-compiler-generated-string-backing-field"
            : $"backing-field-present field-type={field.FieldType.Name}";
    }

    public static string DescribePropertyAccessors()
    {
        var property = typeof(NullableFlowShowcase).GetProperty(nameof(NullableFlowShowcase.Display))!;
        var getter = property.GetGetMethod(nonPublic: true)!;
        var setter = property.GetSetMethod(nonPublic: true)!;

        return $"getter-special-name={getter.IsSpecialName} setter-special-name={setter.IsSpecialName} " +
               $"getter-prefix={getter.Name.StartsWith("get_", StringComparison.Ordinal)} " +
               $"setter-prefix={setter.Name.StartsWith("set_", StringComparison.Ordinal)}";
    }
}
