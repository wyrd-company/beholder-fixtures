namespace Catalog.Core.Events;

public interface INotifier
{
    event Action<string>? Changed;
}

public sealed class NoticeSink
{
    public void Record(string message) => _ = message;
}

public class EventSurface : INotifier
{
    public event Action<string>? Changed;

    public static event Action<int>? GlobalTick;

    public virtual event Func<int, string>? Transformed
    {
        add => _transformed += value;
        remove => _transformed -= value;
    }

    private event Func<int, string>? _transformed;

    event Action<string>? INotifier.Changed
    {
        add => Changed += value;
        remove => Changed -= value;
    }

    public void RaiseChanged(string message) => Changed?.Invoke(message);

    public static void SubscribeAndUnsubscribe(EventSurface surface, NoticeSink sink)
    {
        surface.Changed += sink.Record;
        surface.Changed += LogNotice;
        surface.Changed += message => sink.Record(message);
        surface.Changed -= sink.Record;
        surface.Changed -= LogNotice;
        surface.Changed -= message => sink.Record(message);
    }

    private static void LogNotice(string message) => _ = message;

    public static void RaiseGlobalTick(int value) => GlobalTick?.Invoke(value);

    protected virtual void OnTransformed(int value) => _transformed?.Invoke(value);
}

public sealed class DerivedEventSurface : EventSurface
{
    public override event Func<int, string>? Transformed
    {
        add => base.Transformed += value;
        remove => base.Transformed -= value;
    }
}

public sealed class CustomEventHost
{
    private Action<string>? _handlers;

    public event Action<string> CustomChanged
    {
        add => _handlers = (Action<string>)Delegate.Combine(_handlers, value);
        remove => _handlers = (Action<string>?)Delegate.Remove(_handlers, value);
    }

    public void Publish(string message) => _handlers?.Invoke(message);
}
