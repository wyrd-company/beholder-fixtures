using System;
using System.Collections.Generic;
using SysMath = System.Math;

namespace SourceBinding.Core.Lookup;

public class ScopedLookupBase
{
    protected string Value => "base";
    protected static string StaticValue => "base-static";
}

public class ScopedLookup : ScopedLookupBase
{
    private new string Value => "derived-member";

    private string _value = "field";

    public string DemonstrateShadowing(string value)
    {
        string Value = value; // Parameter 'value' and local 'Value' with colliding name; local shadows parameter via distinct casing/lookup.

        // Local shadows member.
        string result = Value; // binds to local, not this.Value.

        // Qualification to select winner.
        string viaThis = this.Value; // derived member.
        string viaBase = base.Value; // base member.
        string viaGlobal = global::SourceBinding.Core.Lookup.ScopedLookupBase.StaticValue;

        // Type parameter shadowing.
        return $"{result}:{viaThis}:{viaBase}:{viaGlobal}:{_value}";
    }

    public void TypeParameterShadow<T>()
    {
        T shadow = default!;
        _ = shadow;
    }

    public void NamespaceAndImportCollision()
    {
        // Closer using scope via alias SysMath shadows System.Math.
        double viaAlias = SysMath.Abs(-3.0);
        double viaFull = System.Math.Abs(-4.0);
        _ = viaAlias;
        _ = viaFull;

        // Contextual var: 'var' as type versus identifier.
        var var = 5; // 'var' used as variable name with inferred type.
        int varTyped = var + 1;
        _ = varTyped;
    }

    public void InaccessibleCandidate()
    {
        // Inaccessible private member in base is not a candidate; lookup skips it.
        // Demonstrate that accessible derived wins without ambiguity.
        _ = Value;
    }

    // Nested type shadowing import.
    public sealed class Item { }

    public void NestedTypeShadow()
    {
        var item = new Item();
        _ = item;
        // Qualification disambiguates nested type from namespace.
        var globalItem = new global::SourceBinding.Core.Lookup.ScopedLookup.Item();
        _ = globalItem;
    }
}

public static class VarContextual
{
    public static int UseVar(string? input)
    {
        if (input is var x) // 'var' pattern.
        {
            return x?.Length ?? 0;
        }

        return 0;
    }
}
