using System.Collections;
using System.Reflection;
using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

public static class StateMachineHost
{
    public static IEnumerable<int> GetSequence()
    {
        yield return 1;
        yield return 2;
    }

    public static async Task<int> ComputeAsync()
    {
        await Task.Yield();
        return 42;
    }
}

/// <summary>
/// Reflects over the compiler-generated state machine types for an iterator
/// method and an async method, identified only by
/// <see cref="CompilerGeneratedAttribute"/> plus the state-machine interface
/// they implement, never by their synthesized names, per CS-CAN-125.
/// </summary>
public static class StateMachineObservation
{
    public static string DescribeIteratorStateMachine()
    {
        var stateMachineType = typeof(StateMachineHost)
            .GetNestedTypes(BindingFlags.NonPublic)
            .SingleOrDefault(t => t.IsDefined(typeof(CompilerGeneratedAttribute), false) && typeof(IEnumerator).IsAssignableFrom(t));

        return stateMachineType is null
            ? "no-iterator-state-machine"
            : $"iterator-state-machine-present implements-IEnumerator={typeof(IEnumerator).IsAssignableFrom(stateMachineType)}";
    }

    public static string DescribeAsyncStateMachine()
    {
        var stateMachineType = typeof(StateMachineHost)
            .GetNestedTypes(BindingFlags.NonPublic)
            .SingleOrDefault(t => t.IsDefined(typeof(CompilerGeneratedAttribute), false) && typeof(IAsyncStateMachine).IsAssignableFrom(t));

        return stateMachineType is null
            ? "no-async-state-machine"
            : $"async-state-machine-present implements-IAsyncStateMachine={typeof(IAsyncStateMachine).IsAssignableFrom(stateMachineType)}";
    }
}
