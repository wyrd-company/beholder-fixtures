using Acme.Graph.Core;

namespace Acme.Graph.Middle;

public sealed class MiddleService
{
    public TransitType CreateTransit() => new TransitType();
    public string Forward() => new TransitType().Describe();
}
