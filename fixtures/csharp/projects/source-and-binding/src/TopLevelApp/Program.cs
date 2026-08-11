using SourceBinding.Core.Lexical;

// Top-level statements synthesized entry point (C# 9).
System.Console.WriteLine(LexicalIdentity.EscapedIdentifiers());

string[] arguments = args;
System.Console.WriteLine($"args count: {arguments.Length}");

await Task.Delay(1);

int LocalFunction(int value) => value + 1;
System.Console.WriteLine(LocalFunction(41));

return 0;

partial class Program
{
    // Augment the synthesized Program with a partial declaration.
    public static string Augmented() => "augmented program";
}
