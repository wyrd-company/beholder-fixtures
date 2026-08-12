namespace Catalog.FunctionsAndAsync.Disposal;

public sealed class TrackingResource : IDisposable
{
    private readonly Action<string> _log;
    private readonly string _name;

    public TrackingResource(string name, Action<string> log)
    {
        _name = name;
        _log = log;
    }

    public void Dispose() => _log($"dispose:{_name}");
}

public sealed class StructTrackingResource : IDisposable
{
    private readonly Action<string> _log;
    private readonly string _name;

    public StructTrackingResource(string name, Action<string> log)
    {
        _name = name;
        _log = log;
    }

    public void Dispose() => _log($"dispose-struct:{_name}");
}

public ref struct RefStructResource
{
    private readonly Action<string> _log;
    private readonly string _name;

    public RefStructResource(string name, Action<string> log)
    {
        _name = name;
        _log = log;
    }

    public void Dispose() => _log($"dispose-ref:{_name}");
}

public sealed class AsyncTrackingResource : IAsyncDisposable, IDisposable
{
    private readonly Action<string> _log;
    private readonly string _name;

    public AsyncTrackingResource(string name, Action<string> log)
    {
        _name = name;
        _log = log;
    }

    public void Dispose() => _log($"dispose-sync:{_name}");

    public ValueTask DisposeAsync()
    {
        _log($"dispose-async:{_name}");
        return ValueTask.CompletedTask;
    }
}

public sealed class DualDisposable : IDisposable, IAsyncDisposable
{
    private readonly Action<string> _log;

    public DualDisposable(Action<string> log) => _log = log;

    public void Dispose() => _log("dispose-sync");

    public ValueTask DisposeAsync()
    {
        _log("dispose-async");
        return ValueTask.CompletedTask;
    }
}

public readonly struct ReadonlyStructResource : IDisposable
{
    private readonly Action<string> _log;
    private readonly string _name;

    public ReadonlyStructResource(string name, Action<string> log)
    {
        _name = name;
        _log = log;
    }

    public void Dispose() => _log($"dispose-readonly-struct:{_name}");
}

public static class DisposalCatalog
{
    public static void UsingStatement(Action<string> log)
    {
        using (var a = new TrackingResource("a", log))
        using (var b = new TrackingResource("b", log))
        {
            log("body");
        }
    }

    public static void UsingDeclaration(Action<string> log)
    {
        using var a = new TrackingResource("a", log);
        using var b = new TrackingResource("b", log);
        log("body");
    }

    public static void MultipleReverseOrder(Action<string> log)
    {
        using (var first = new TrackingResource("first", log))
        using (var second = new TrackingResource("second", log))
        using (var third = new TrackingResource("third", log))
        {
            log("inside");
        }

        log("outside");
    }

    public static void NullableResource(Action<string> log, bool create)
    {
        TrackingResource? resource = create ? new TrackingResource("maybe", log) : null;
        using (resource)
        {
            log("body");
        }
    }

    public static void StructResource(Action<string> log)
    {
        using (var r = new StructTrackingResource("struct", log))
        {
            log("body");
        }
    }

    public static void RefStructPattern(Action<string> log)
    {
        using var r = new RefStructResource("ref", log);
        log("body");
    }

    public static void EarlyReturn(Action<string> log, bool early)
    {
        using var r = new TrackingResource("early", log);
        log("start");
        if (early)
        {
            return;
        }

        log("end");
    }

    public static void ExceptionInBody(Action<string> log)
    {
        try
        {
            using var r = new TrackingResource("exc-body", log);
            log("body");
            throw new InvalidOperationException("body-fail");
        }
        catch (InvalidOperationException)
        {
            log("caught");
        }
    }

    public static void ExceptionInDispose(Action<string> log)
    {
        try
        {
            using var r = new ThrowingDisposeResource(log);
            log("body");
        }
        catch (InvalidOperationException)
        {
            log("caught-dispose");
        }
    }

    public static void BodyAndDisposeExceptionInteraction(Action<string> log)
    {
        try
        {
            using var r = new ThrowingDisposeResource(log);
            log("body");
            throw new InvalidOperationException("body");
        }
        catch (Exception ex)
        {
            log($"caught:{ex.GetType().Name}");
        }
    }

    public static async Task AwaitUsingStatement(Action<string> log)
    {
        await using (var r = new AsyncTrackingResource("async-a", log))
        {
            log("body");
        }
    }

    public static async Task AwaitUsingDeclaration(Action<string> log)
    {
        await using var r = new AsyncTrackingResource("async-b", log);
        log("body");
    }

    public static async Task UsingWithAsyncDisposableDual(Action<string> log)
    {
        await using var d = new DualDisposable(log);
        log("body-sync-async");
    }

    public static void UsingWithDisposableDual(Action<string> log)
    {
        using var d = new DualDisposable(log);
        log("body-sync");
    }

    public static void ReadonlyStructUsing(Action<string> log)
    {
        using var r = new ReadonlyStructResource("readonly-struct", log);
        log("body-readonly-struct");
    }

    public static void ReadonlyVariableRestriction(Action<string> log)
    {
        using var resource = new TrackingResource("readonly-var", log);
        log("body-readonly");
    }

    public static void DynamicUsing(Action<string> log)
    {
        dynamic resource = new TrackingResource("dynamic", log);
        using (resource)
        {
            log("body-dynamic");
        }
    }

    public static void DynamicNullUsing(Action<string> log)
    {
        dynamic resource = null!;
        using (resource)
        {
            log("body-dynamic-null");
        }
    }

    public static void ScopeDifference(Action<string> log)
    {
        log("before-block");
        using (var r = new TrackingResource("block", log))
        {
            log("inside-block");
        }

        log("after-block");

        log("before-decl");
        using var d = new TrackingResource("decl", log);
        log("after-decl");
    }
}

internal sealed class ThrowingDisposeResource : IDisposable
{
    private readonly Action<string> _log;

    public ThrowingDisposeResource(Action<string> log) => _log = log;

    public void Dispose()
    {
        _log("dispose-throw");
        throw new InvalidOperationException("dispose-fail");
    }
}
