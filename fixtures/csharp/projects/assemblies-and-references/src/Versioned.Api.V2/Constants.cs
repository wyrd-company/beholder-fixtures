namespace Acme.Versioned;

public static class ApiConstants
{
    public const string ApiConstant = "v2-constant";
    public const int ApiValue = 200;
}

public static class OptionalDefaults
{
    public static string Greet(string name = "WorldV2") => $"Hello {name} from V2";
}

public static class OverloadSet
{
    public static string Execute(string payload) => $"V2 Execute({payload})";
    // Added overload in V2: recompilation changes binding target
    public static string Execute(string payload, int repeat) => $"V2 Execute({payload}, {repeat})";
}

public class WidgetBase
{
    // Virtual changed: in V2 this is non-virtual (or sealed) changing dispatch
    public string Describe() => "WidgetBase V2 non-virtual";
}

public interface IApiContract
{
    void LegacyOperation();
    // Default interface addition in V2: binary compatible, source-visible change
    void NewDefaultOperation() => System.Console.WriteLine("default impl V2");
}

public sealed class RemovedMemberDemo
{
    public void StillPresent() { }
    // ToBeRemovedInV2 is removed: old consumers built against V1 that call it would get MissingMethodException at runtime
}
