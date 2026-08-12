namespace SourceBinding.Core.Usings;

public static class ImplicitOnlyDemo
{
    // Binds only through SDK-generated implicit usings (Core has ImplicitUsings enable).
    // No explicit using for System.Linq or System.Threading.Tasks is present in this file,
    // and GlobalUsings.cs does not declare them. These names are supplied by obj/**/GlobalUsings.g.cs.
    public static int ViaImplicitLinq()
    {
        var values = new[] { 1, 2, 3 };
        return values.Sum();
    }

    public static Task<int> ViaImplicitTask()
    {
        return Task.FromResult(ViaImplicitLinq());
    }

    // Alternative using implicit System.Collections.Generic via implicit usings only for collection construction
    // is not suitable here because GlobalUsings explicitly declares System.Collections.Generic.
    // Linq and Tasks are the implicit-only witnesses.
}
