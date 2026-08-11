namespace SourceBinding.Core.Preprocessor;

public static class LineMapping
{
    public static int CurrentLine()
    {
        return CurrentLineCore();
    }

    private static int CurrentLineCore()
    {
#line 200 "MappedFile.cs"
        return 200;
#line default
    }

    // Hidden and default line mapping.
#line hidden
    public static int HiddenLine()
    {
        return 1;
    }
#line default

    // Enhanced #line is exercised in contexts/csharp10.

    public static string CallerPath([System.Runtime.CompilerServices.CallerFilePath] string path = "")
    {
        return path;
    }
}
