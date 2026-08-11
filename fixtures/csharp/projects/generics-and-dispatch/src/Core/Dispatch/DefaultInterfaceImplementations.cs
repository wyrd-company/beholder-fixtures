namespace GenericsAndDispatch.Core.Dispatch;

public interface ILogger
{
    string Prefix => "log";
    string Format(string message) => $"{Prefix}:{message}";
    void Log(string message) => Console.WriteLine(Format(message));
    private static string Tag() => "private";
    static string StaticTag => "static";
}

public interface IAdvancedLogger : ILogger
{
    string ILogger.Format(string message) => $"advanced:{message}";
}

public interface IFirst
{
    string Identify() => "first";
}

public interface ISecond
{
    string Identify() => "second";
}

// Resolved diamond: derived interface overrides.
public interface ICombined : IFirst, ISecond
{
    string IFirst.Identify() => "combined-first";
    string ISecond.Identify() => "combined-second";
    string Resolve() => ((IFirst)this).Identify() + "+" + ((ISecond)this).Identify();
}

// Re-abstraction.
public interface IReAbstracted : ILogger
{
    abstract new string Format(string message);
}

public sealed class ConsoleLogger : ILogger
{
    // Class member wins over default.
    public string Format(string message) => $"console:{message}";
}

public sealed class SimpleLogger : ILogger { }

public sealed class AdvancedLogger : IAdvancedLogger { }

public sealed class DiamondResolved : ICombined { }

public sealed class OverridingLogger : ILogger
{
    public string Format(string message) => $"overriding:{message}";
    public void Log(string message) => Console.WriteLine(Format(message));
}

public sealed class ReAbstractedLogger : IReAbstracted
{
    public string Format(string message) => $"re:{message}";
}

public static class DefaultInterfaceExercises
{
    public static void Run()
    {
        ILogger simple = new SimpleLogger();
        string formatted = simple.Format("hello");
        simple.Log("hello");

        ILogger console = new ConsoleLogger();
        string consoleFormatted = console.Format("hello");
        string directCall = new ConsoleLogger().Format("hello");

        IAdvancedLogger advanced = new AdvancedLogger();
        string advancedFormatted = ((ILogger)advanced).Format("hi");

        // Class member winning verified via interface reference versus class surface.
        ILogger overriding = new OverridingLogger();
        string overridingFormatted = overriding.Format("x");

        // Resolved diamond.
        ICombined combined = new DiamondResolved();
        string resolved = combined.Resolve();

        // Re-abstraction.
        IReAbstracted re = new ReAbstractedLogger();
        string reFormatted = re.Format("again");

        // Private/static interface members not visible on class surface.
        string staticTag = ILogger.StaticTag;

        // Ambiguous diamond without combined resolution would be invalid (not fixture);
        // resolved diamond above shows valid case.

        _ = formatted;
        _ = consoleFormatted;
        _ = directCall;
        _ = advancedFormatted;
        _ = overridingFormatted;
        _ = resolved;
        _ = reFormatted;
        _ = staticTag;
    }
}
