#pragma warning disable CS0067
namespace GenericsAndDispatch.Core.Dispatch;

public interface IRenderer
{
    string Render();
    string Tag { get; }
    event EventHandler Rendered;
}

public interface IExporter
{
    string Render();
    string Export();
}

public interface ITagReset
{
    void Reset();
    string Tag { get; set; }
}

public class BaseRenderer : IRenderer
{
    public string Tag => "base";
    public event EventHandler? Rendered;
    public virtual string Render() => "base-render";
    protected void Raise() => Rendered?.Invoke(this, EventArgs.Empty);
}

// Implicit, explicit, and base-member participation.
public sealed class MappedWidget : BaseRenderer, IRenderer, IExporter, ITagReset
{
    // Separate explicit implementations for same-signature members.
    string IRenderer.Render() => "renderer";
    string IExporter.Render() => "exporter";
    string IExporter.Export() => "export";

    // Implicit implementation via base virtual.
    public override string Render() => "mapped";

    // Accessor-level mismatch: ITagReset has setter.
    public new string Tag { get; set; } = "mapped";
    string IRenderer.Tag => Tag;
    void ITagReset.Reset() => Tag = string.Empty;
    public event EventHandler? Exported;
    public void Fire() => Exported?.Invoke(this, EventArgs.Empty);
}

// Shared same-signature mapping: one member satisfies both IRenderer and IExporter.
public sealed class SharedWidget : IRenderer, IExporter
{
    public string Tag => "shared";
    public event EventHandler? Rendered;
    public string Render() => "shared";
    public string Export() => "shared-export";
}

// Derived reimplementation.
public class ReimplementedBase : IRenderer
{
    public string Tag => "re-base";
    public event EventHandler? Rendered;
    public virtual string Render() => "re-base";
    protected void Raise() => Rendered?.Invoke(this, EventArgs.Empty);
}

public sealed class ReimplementedDerived : ReimplementedBase, IRenderer
{
    public override string Render() => "re-derived";
    string IRenderer.Render() => "re-derived-explicit";
}

// Struct boxing and runtime interface mapping inspection.
public struct StructRenderer : IRenderer
{
    public string Tag => "struct";
    public event EventHandler? Rendered;
    public string Render() => "struct-render";
    public void Raise() => Rendered?.Invoke(this, EventArgs.Empty);
}

public static class InterfaceMappingExercises
{
    public static void Run()
    {
        var widget = new MappedWidget();
        IRenderer asRenderer = widget;
        IExporter asExporter = widget;

        string viaBase = ((BaseRenderer)widget).Render();
        string viaRenderer = asRenderer.Render();
        string viaExporter = asExporter.Render();
        string export = asExporter.Export();

        // Shared mapping: one Render serves both interfaces.
        var shared = new SharedWidget();
        string sharedViaRenderer = ((IRenderer)shared).Render();
        string sharedViaExporter = ((IExporter)shared).Render();
        shared.Rendered += (_, _) => { };
        ((IRenderer)shared).Rendered += (_, _) => { };
        var sharedMapRenderer = typeof(SharedWidget).GetInterfaceMap(typeof(IRenderer));
        var sharedMapExporter = typeof(SharedWidget).GetInterfaceMap(typeof(IExporter));
        bool sameTarget = sharedMapRenderer.TargetMethods[0] == sharedMapExporter.TargetMethods[0];

        // Explicit-call cast requirement.
        string tagRenderer = asRenderer.Tag;
        string tagReset = ((ITagReset)widget).Tag;

        // Runtime interface mapping.
        var map = typeof(MappedWidget).GetInterfaceMap(typeof(IRenderer));
        var mapExporter = typeof(MappedWidget).GetInterfaceMap(typeof(IExporter));

        // Struct boxing for interface call.
        StructRenderer s = new();
        IRenderer boxed = s;
        string structRender = boxed.Render();
        s.Rendered += (_, _) => { };
        boxed.Rendered += (_, _) => { };

        // Derived reimplementation.
        ReimplementedBase reBase = new ReimplementedDerived();
        string reBaseRender = reBase.Render();
        string reExplicit = ((IRenderer)reBase).Render();

        _ = viaBase; _ = viaRenderer; _ = viaExporter; _ = export;
        _ = sharedViaRenderer; _ = sharedViaExporter; _ = sharedMapRenderer; _ = sharedMapExporter; _ = sameTarget;
        _ = tagRenderer; _ = tagReset; _ = map; _ = mapExporter;
        _ = structRender; _ = reBaseRender; _ = reExplicit;
    }
}
