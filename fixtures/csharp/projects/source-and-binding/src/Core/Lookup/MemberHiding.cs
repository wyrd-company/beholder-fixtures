using System;

namespace SourceBinding.Core.Lookup;

public class HidingBase
{
    public int Field = 1;

    public virtual string Describe() => "base";

    public string Label => "base-label";

    public void Execute(int value) => _ = value;

    public void Execute(string value) => _ = value;

    public class NestedBase
    {
        public static string Describe() => "nested base";
    }

    protected string HiddenProtected => "base protected";
}

public class HidingDerived : HidingBase
{
    public new int Field = 2;

    public new string Label => "derived-label";

    // Overload group hiding: derived overload hides base overloads unless new is explicit and overload resolution selects.
    public new void Execute(int value) => _ = value * 2;

    // New virtual creates a separate slot from base virtual.
    public new virtual string Describe() => "derived new virtual";

    public new class NestedBase
    {
        public static string Describe() => "nested derived hides base";
    }

    public string ViaBaseQualification()
    {
        string viaBase = base.Describe(); // base qualification bypasses hiding.
        string viaThis = Describe(); // derived.
        string viaBaseCast = ((HidingBase)this).Describe(); // base slot via static type.
        return $"{viaBase}:{viaThis}:{viaBaseCast}";
    }

    public string AccessHiddenProtected() => HiddenProtected; // inaccessible base member not hidden; still accessible via inheritance.

    // Generic base hiding demonstration.
    public string DescribeGeneric<T>(T value) => value?.ToString() ?? "null";
}

public class HidingMostDerived : HidingDerived
{
    public override string Describe() => "most derived overrides new virtual slot";
}

public static class HidingSurface
{
    public static int FieldViaStaticType()
    {
        HidingDerived derived = new HidingDerived();
        HidingBase asBase = derived;
        int viaDerived = derived.Field; // 2
        int viaBase = asBase.Field; // 1, hidden field via base static type.
        return viaDerived + viaBase;
    }

    public static string LabelViaStaticType()
    {
        HidingDerived derived = new HidingDerived();
        HidingBase asBase = derived;
        string viaDerived = derived.Label; // derived
        string viaBase = asBase.Label; // base
        return $"{viaDerived}/{viaBase}";
    }

    public static string NestedViaQualification()
    {
        string viaHiding = HidingDerived.NestedBase.Describe();
        string viaBaseQual = global::SourceBinding.Core.Lookup.HidingBase.NestedBase.Describe();
        return $"{viaHiding}:{viaBaseQual}";
    }
}
