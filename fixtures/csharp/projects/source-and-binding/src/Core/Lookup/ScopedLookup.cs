using System;
using System.Collections.Generic;
using DemoA;
using DemoB;

namespace SourceBinding.Core.Lookup;

public class ScopedLookupBase
{
    protected int shared = 1;
#pragma warning disable CS0414
    private int hidden = 99;
#pragma warning restore CS0414
    protected static int StaticValue => 10;
}

public class ScopedLookup : ScopedLookupBase
{
    private new int shared = 2;
    public int hidden = 100;

    // Parameter shadows field (same spelling 'shared').
    public int ParamShadowsField(int shared)
    {
        int viaParam = shared;
        int viaField = this.shared;
        int viaBase = base.shared;
        return viaParam + viaField + viaBase;
    }

    // Local shadows field (same spelling 'shared').
    public int LocalShadowsField()
    {
        int sharedLocal = 5;
        _ = sharedLocal;
        int shared = 10;
        int viaLocal = shared;
        int viaField = this.shared;
        return viaLocal + viaField;
    }

    // Type parameter shadowing: method type param shadows class type param.
#pragma warning disable CS0693
    public class GenericOuter<T>
    {
        private T outerValue = default!;

        public void TypeParamShadow<TInner>(TInner innerValue)
        {
            TInner local = innerValue;
            _ = local;
            _ = outerValue;
        }

        public void SameNameTypeParam<T>(T value)
        {
            T local = value;
            _ = local;
        }
    }
#pragma warning restore CS0693

    public sealed class Item
    {
        public static string Describe() => "nested Item";
    }

    public void NestedTypeLookup()
    {
        var viaNested = new Item();
        var viaGlobal = new global::SourceBinding.Core.Lookup.ScopedLookup.Item();
        _ = viaNested;
        _ = viaGlobal;
    }

    public string MemberShadowing()
    {
        int viaThis = this.shared;
        int viaBase = base.shared;
        int viaGlobal = global::SourceBinding.Core.Lookup.ScopedLookupBase.StaticValue;
        return $"{viaThis}:{viaBase}:{viaGlobal}";
    }

    public string CloserUsingScope()
    {
        string viaA = DemoA.Widget.Describe();
        string viaB = DemoB.Widget.Describe();
        return $"{viaA}:{viaB}";
    }

    public void ContextualVarDemo()
    {
        var var = 7;
        int result = var + 1;
        _ = result;
    }

    public int InaccessibleCandidateDemo()
    {
        return hidden;
    }

    public string AmbiguousResolved()
    {
        var a = new DemoA.Widget();
        var b = new DemoB.Widget();
        return $"{a.GetType().FullName}:{b.GetType().FullName}";
    }
}

public static class VarContextual
{
    public static int UseVar(string? input)
    {
        if (input is var x)
        {
            return x?.Length ?? 0;
        }

        return 0;
    }
}
