using System;

#pragma warning disable CS0414

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

    private int hiddenPrivate = 99;

    protected string HiddenProtected => "base protected";
}

public class HidingWithoutNewBase
{
    public int Value = 1;
}

public class HidingWithoutNewDerived : HidingWithoutNewBase
{
#pragma warning disable CS0108
    public int Value = 2;
#pragma warning restore CS0108
}

public class InaccessibleBase
{
    private int secret = 1;
}

public class InaccessibleDerived : InaccessibleBase
{
    public int secret = 2;
}

public class GenericHidingBase<T>
{
    public T BaseValue = default!;

    public string DescribeBase(T value) => $"base:{value}";
}

public class GenericHidingDerived : GenericHidingBase<int>
{
    public new string BaseValue = "derived";

    public new string DescribeBase(int value) => $"derived:{value}";
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

    public string AccessHiddenProtected() => HiddenProtected;

    public int AccessHiddenPrivateViaDerived()
    {
        var derived = new InaccessibleDerived();
        return derived.secret;
    }

    public string GenericBaseHidingDemo()
    {
        var derived = new GenericHidingDerived();
        string viaDerived = derived.BaseValue;
        string viaBase = ((GenericHidingBase<int>)derived).BaseValue.ToString()!;
        return $"{viaDerived}:{viaBase}";
    }
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
