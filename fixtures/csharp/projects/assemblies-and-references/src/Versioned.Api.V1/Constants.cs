namespace Acme.Versioned;

public static class ApiConstants
{
    public const string ApiConstant = "v1-constant";
    public const int ApiValue = 100;
}

public static class OptionalDefaults
{
    public static string Greet(string name = "WorldV1") => $"Hello {name} from V1";
}

public static class OverloadSet
{
    public static string Execute(string payload) => $"V1 Execute({payload})";
}

public class WidgetBase
{
    public virtual string Describe() => "WidgetBase V1 virtual";
}

public interface IApiContract
{
    void LegacyOperation();
}

public sealed class RemovedMemberDemo
{
    public void StillPresent() { }
    public void ToBeRemovedInV2() { }
}
