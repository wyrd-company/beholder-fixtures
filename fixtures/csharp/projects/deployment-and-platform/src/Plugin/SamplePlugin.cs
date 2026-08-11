using Acme.Deployment.Contracts;

namespace Acme.Deployment.Plugin;

public class SamplePlugin : IPlugin
{
    public string Name => "sample";

    public string Execute(string input) => $"sample:{input}";

    // Additional member reachable only via reflection — trimming may remove it
    // if not annotated; the host preserves it via DynamicallyAccessedMembers.
    public string HiddenOperation(string input) => $"hidden:{input}";
}

public class AlternatePlugin : IPlugin
{
    public string Name => "alternate";
    public string Execute(string input) => $"alt:{input.ToUpperInvariant()}";
}
