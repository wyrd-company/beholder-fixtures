using Acme.Forwarding.Legacy;

namespace Acme.Forwarding.Composition;

// Controlled runtime composition for the pre-move half of the forwarding pair.
//
// Forwarding.Consumer.Legacy is compiled against Forwarding.Facade.PreMove, whose
// "Forwarding.Facade" identity DEFINES RelocatedType directly. This executable deploys the
// POST-move "Forwarding.Facade.dll" (a forwarder carrying [assembly: TypeForwardedTo]) plus
// Forwarding.Definition.dll next to that unchanged legacy binary. Because both facade shapes
// share the simple assembly name "Forwarding.Facade", the legacy binary loads the forwarder
// at run time, and the CLR follows TypeForwardedTo to Forwarding.Definition without the
// legacy binary being recompiled.
//
// The pre-move binary was built expecting RelocatedType.Version == 1 and the pre-move
// Describe() text. Observing Version == 2 and the Forwarding.Definition text at run time is
// the proof that the CLR, not the compiler, followed the forward for a pre-move binary.
internal static class Program
{
    private static int Main()
    {
        var legacy = new LegacyConsumer();

        var declaring = legacy.ReflectDeclaringAssembly();
        var described = legacy.ConsumeDirect();

        Console.WriteLine("[composition] pre-move legacy binary running against the post-move forwarder");
        Console.WriteLine("[legacy.ReflectDeclaringAssembly] " + declaring);
        Console.WriteLine("[legacy.ConsumeDirect] " + described);

        // The forward is followed only if the pre-move binary now resolves RelocatedType in
        // Forwarding.Definition (the post-move location) rather than the Forwarding.Facade
        // identity it was compiled against.
        var followed = declaring.Contains("DeclaringAssembly=Forwarding.Definition")
            && described.Contains("now lives in Forwarding.Definition");

        Console.WriteLine(followed
            ? "[composition] CLR followed TypeForwardedTo: RelocatedType resolved in Forwarding.Definition at run time"
            : "[composition] forward NOT followed: RelocatedType did not resolve to Forwarding.Definition");

        return followed ? 0 : 1;
    }
}
