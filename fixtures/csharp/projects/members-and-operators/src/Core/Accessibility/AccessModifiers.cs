namespace Catalog.Core.Accessibility;

public class AccessModifiers
{
    public int PublicField;

    internal int InternalField;

    protected int ProtectedField;

    private int PrivateField = 1;

    protected internal int ProtectedInternalField;

    private protected int PrivateProtectedField;

    public int PublicProperty { get; set; }

    internal int InternalProperty { get; set; }

    protected int ProtectedProperty { get; set; }

    private int PrivateProperty { get; set; }

    protected internal int ProtectedInternalProperty { get; set; }

    private protected int PrivateProtectedProperty { get; set; }

    public void PublicMethod() => _ = PrivateField;

    internal void InternalMethod() => _ = InternalField;

    protected void ProtectedMethod() => _ = ProtectedField;

    private void PrivateMethod() => _ = PrivateField;

    protected internal void ProtectedInternalMethod() => _ = ProtectedInternalField;

    private protected void PrivateProtectedMethod() => _ = PrivateProtectedField;
}

public class DerivedAccessModifiers : AccessModifiers
{
    public void UseProtected() => ProtectedMethod();

    public void UseProtectedInternal() => ProtectedInternalMethod();

    public void UsePrivateProtected() => PrivateProtectedMethod();
}

public class NestedAccessHost
{
    private int _hostValue;

    public int HostValue => _hostValue;

    public class PublicNested
    {
        public void TouchHost(NestedAccessHost host) => host._hostValue = 1;
    }

    private class PrivateNested
    {
        public void TouchHost(NestedAccessHost host) => host._hostValue = 2;
    }
}

internal sealed class InternalCatalogEntry
{
    internal int InternalOnlyValue;

    internal void Touch(AccessModifiers target) => target.InternalMethod();
}

public static class SameAssemblyAccess
{
    internal static void Demonstrate(AccessModifiers target, InternalCatalogEntry entry)
    {
        target.InternalMethod();
        entry.InternalOnlyValue = 3;
    }
}

public class LessAccessibleSignatureHost
{
    private int _value;

    public int Value
    {
        get => _value;
        private set => _value = value;
    }
}
