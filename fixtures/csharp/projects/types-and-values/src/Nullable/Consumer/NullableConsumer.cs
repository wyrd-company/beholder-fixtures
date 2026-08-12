using System.Diagnostics.CodeAnalysis;
using Bakery.TypesAndValues.Nullable.AnnotatedApi;
using Bakery.TypesAndValues.Nullable.AnnotationsOnly;
using Bakery.TypesAndValues.Nullable.DisabledScope;
using Bakery.TypesAndValues.Nullable.ObliviousLegacy;
using Bakery.TypesAndValues.Nullable.WarningsOnly;

namespace Bakery.TypesAndValues.Nullable.Consumer;

// CS-CAN-024: cross-assembly consumer — enabled scope consuming annotated, oblivious,
// annotations-only, warnings-only, and disabled metadata; guards, !, flow attributes,
// override mismatch, constructor initialization, generic T?, warnings-as-errors, old-metadata.

public sealed class NullableConsumer
{
    public void ConsumeAnnotated()
    {
        AnnotatedInventory inventory = new();
        string? maybe = inventory.FindByName("rye");
        if (maybe is not null)
        {
            _ = maybe.Length;
        }

        string forced = maybe!;
        _ = forced;

        if (inventory.TryFind("sourdough", out string? found))
        {
            _ = found.Length;
        }

        if (inventory.TryGetCount("brioche", out string? normalized))
        {
            _ = normalized.Length;
        }

        inventory.EnsureInitialized();
        _ = inventory.GetInitializedLabel().Length;

        if (inventory.HasLazyLabel())
        {
            _ = inventory.LazyLabel!.Length;
        }

        string? mapped = inventory.MapIfNotNull("hello");
        _ = mapped?.Length;

        GenericBox<string> box = new() { Value = "seed" };
        if (box.HasValue(out string? value))
        {
            _ = value.Length;
        }
    }

    public void ConsumeOblivious()
    {
        LegacyInventory legacy = new();
        string result = legacy.Find("rye");
        _ = result.Length;

        // Old metadata: LegacyInventory never emitted nullable attributes; consumer
        // treats its string members as non-nullable oblivious. No warning is produced
        // when assigning to a non-nullable variable, but the value could be null at runtime.
        string oblivious = legacy.GetLabel("test");
        _ = oblivious;
    }

    public void ConsumeDisabled()
    {
        DisabledInventory disabled = new();
        string result = disabled.Find("rye");
        _ = result.Length;

        string maybeNull = disabled.MaybeReturnsNull(string.Empty);
        _ = maybeNull;
    }

    public void ConsumeAnnotationsOnly()
    {
        AnnotationsOnlyInventory inventory = new();
        string? maybe = inventory.Find(null);
        string fallback = inventory.Require(maybe);
        _ = fallback.Length;
    }

    public void ConsumeWarningsOnly()
    {
        WarningsOnlyInventory inventory = new();
        string? maybe = inventory.Find("brioche");
        inventory.Consume(maybe);
    }

    public void GuardedDereference(string? maybe)
    {
        if (maybe is null)
        {
            return;
        }

        _ = maybe.Length;

        string? nullableParam = maybe;
        string nonNull = nullableParam!;
        _ = nonNull.Length;
    }

    public void FlowAttributes(AnnotatedInventory inventory, string? input)
    {
        string guarded = inventory.EnsureNotNull(input ?? "fallback");
        _ = guarded.Length;

        if (input is not null)
        {
            inventory.SetLabel(input);
        }
    }

    // Real override/interface nullability mismatch with local suppression at declaration.
    public abstract class OverrideMismatchBase
    {
        public virtual string? Describe(string? input) => input;
    }

    public sealed class OverrideMismatchDerived : OverrideMismatchBase
    {
#pragma warning disable CS8765
        public override string Describe(string input) => input ?? "fallback";
#pragma warning restore CS8765
    }

    public interface IMismatchContract
    {
        string? Fetch(string? query);
    }

    public sealed class MismatchContractImpl : IMismatchContract
    {
#pragma warning disable CS8767
        public string Fetch(string query) => query ?? "fallback";
#pragma warning restore CS8767
    }

    public void DemonstrateOverrideMismatch()
    {
        OverrideMismatchBase asBase = new OverrideMismatchDerived();
        string? result = asBase.Describe(null);
        _ = result;

        IMismatchContract contract = new MismatchContractImpl();
        string? fetched = contract.Fetch(null);
        _ = fetched;
    }

    public void ConstructorInitializationDemo()
    {
        ConstructorInitialization instance = new("ready");
        _ = instance.Label.Length;
        instance.InitializeIfNeeded();
        _ = instance.Label.Length;

        _ = new ConstructorInitialization("starter").Label.Length;
    }

    public void GenericTNullable()
    {
        GenericBox<string> classBox = new() { Value = null };
        _ = classBox.Value is null;

        GenericStructBox<int> structBox = new() { Value = 5 };
        _ = structBox.Value.GetValueOrDefault();
        _ = structBox.Value ?? 0;
    }

    // WarningsAsErrors demo: Consumer.csproj sets <WarningsAsErrors>nullable</WarningsAsErrors>
    // so any unsuppressed nullable warning fails the build. This method is warning-free.
    public void WarningsAsErrorsIsEnforced(string? maybe)
    {
        string value = maybe ?? "default";
        _ = value.Length;
    }

    // Valid dereference-warning source in enabled scope with narrowly scoped suppression.
    public void EnabledDereferenceWarning(string? maybe)
    {
#pragma warning disable CS8602
        _ = maybe.Length;
#pragma warning restore CS8602
    }

    // Enabled + disabled scopes coexisting via #nullable directives in same file.
    public void MixedDirectives()
    {
#nullable disable
        string disabledMaybe = null!;
        int lenDisable = disabledMaybe.Length;
        _ = lenDisable;
#nullable enable
        string? enabledMaybe = null;
        if (enabledMaybe is not null)
        {
            _ = enabledMaybe.Length;
        }
    }

    // Oblivious file-level scope demonstration.
#nullable disable
    public void ObliviousFileScope(Bakery.TypesAndValues.Nullable.ObliviousLegacy.LegacyInventory legacy)
    {
        string value = legacy.Find("sourdough");
        _ = value.Length;
    }
#nullable restore
}
