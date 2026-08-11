using System.Reflection;
using Fixture.AttributesAndMetadata.Core.Attributes;
using Fixture.AttributesAndMetadata.Core.Metadata;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

/// <summary>Implements <see cref="IShowcaseContract"/> explicitly, so the implementing method is not directly accessible by its simple name.</summary>
public sealed class ExplicitContractImplementation : IShowcaseContract
{
    void IShowcaseContract.Act()
    {
    }
}

/// <summary>
/// Reflects over an explicit interface implementation, a generic type
/// definition versus a closed construction, a <c>modreq</c> custom modifier
/// emitted for an <see langword="init"/> accessor, and an attribute applied
/// to a parameter.
/// </summary>
public static class ExplicitInterfaceAndGenericDefinitionObservation
{
    public static string DescribeExplicitImplementation()
    {
        var map = typeof(ExplicitContractImplementation).GetInterfaceMap(typeof(IShowcaseContract));
        var implementingMethod = map.TargetMethods.Single();

        return $"explicit-impl-is-private={implementingMethod.IsPrivate} " +
               $"explicit-impl-name-contains-interface-qualifier={implementingMethod.Name.Contains(nameof(IShowcaseContract), StringComparison.Ordinal)}";
    }

    public static string DescribeGenericDefinition()
    {
        var openDefinition = typeof(ShowcaseGeneric<>);
        var closedConstruction = typeof(ShowcaseGeneric<int>);

        return $"open-is-definition={openDefinition.IsGenericTypeDefinition} " +
               $"closed-is-definition={closedConstruction.IsGenericTypeDefinition} " +
               $"closed-shares-definition={closedConstruction.GetGenericTypeDefinition() == openDefinition}";
    }

    public static string DescribeInitAccessorCustomModifier()
    {
        var setter = typeof(InitOnlyRecord).GetProperty(nameof(InitOnlyRecord.Value))!.GetSetMethod(nonPublic: true)!;
        var requiredModifiers = setter.ReturnParameter.GetRequiredCustomModifiers();

        return $"init-setter-has-isexternalinit-modreq={requiredModifiers.Any(m => m.Name == "IsExternalInit")}";
    }

    public static string DescribeParameterAttributeReflection()
    {
        var method = typeof(AttributeTargetShowcase).GetMethod(nameof(AttributeTargetShowcase.Compute))!;
        var parameter = method.GetParameters().Single();
        var hasShowcaseAttribute = parameter.IsDefined(typeof(ShowcaseAttribute), false);

        return $"parameter-attribute-reflected={hasShowcaseAttribute}";
    }
}
