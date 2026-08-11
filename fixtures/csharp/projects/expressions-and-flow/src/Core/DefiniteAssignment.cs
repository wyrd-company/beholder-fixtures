namespace ExpressionsFlow.Core;

public static class DefiniteAssignmentFlow
{
    public static int Branch(int flag)
    {
        int result;
        if (flag > 0)
        {
            result = 1;
        }
        else
        {
            result = -1;
        }

        return result;
    }

    public static int Loop(int limit)
    {
        int sum = 0;
        for (int i = 0; i < limit; i++)
        {
            sum += i;
        }

        return sum;
    }

    public static int TryFlow(string text)
    {
        int value;
        try
        {
            value = int.Parse(text);
        }
        catch (FormatException)
        {
            value = -1;
        }
        catch (OverflowException)
        {
            value = -2;
        }
        finally
        {
            // finally does not affect definite assignment of value because both try and catch assigned.
        }

        return value;
    }

    public static bool TryOutVar(string text, out int parsed)
    {
        if (int.TryParse(text, out var tmp))
        {
            parsed = tmp;
            return true;
        }

        parsed = 0;
        return false;
    }

    public static int PatternScope(object input)
    {
        if (input is string s && s.Length > 0)
        {
            return s.Length;
        }

        if (input is int n)
        {
            return n;
        }

        // Boolean pattern scope: variable declared in pattern is only definite when pattern succeeds.
        // Example: 'input is string { Length: >0 }' would scope inside true branch.
        return 0;
    }

    public static (int X, int Y) DeconstructionAssignment()
    {
        var (a, b) = GetPair();
        int x = a;
        int y = b;
        return (x, y);
    }

    public static int CapturedVariable()
    {
        int captured = 0;
        Func<int> getter = () => captured;
        captured = 41;
        captured += 1;
        return getter();
    }

    public static int StructDefiniteAssignment()
    {
        var holder = new StructHolder(5, 7);
        return holder.X + holder.Y;
    }

    public static int ClassDefiniteAssignment()
    {
        var holder = new ClassHolder();
        holder.X = 3;
        holder.Y = 4;
        return holder.X + holder.Y;
    }

    public static int GotoFlow(int selector)
    {
        int value;
        switch (selector)
        {
            case 0:
                value = 10;
                goto case 1;
            case 1:
                value = 20;
                break;
            default:
                value = -1;
                break;
        }

        return value;
    }

    public static int ReturnCompleteness(bool flag)
    {
        if (flag)
        {
            return 1;
        }
        else
        {
            return 2;
        }
    }

    public static string NullStateSeparated(string? maybe)
    {
        // Definite assignment and nullable flow are separate analyses.
        // The following shows nullable narrowing without affecting definite assignment of 'result'.
        string result;
        if (maybe is not null)
        {
            result = maybe.ToUpperInvariant();
        }
        else
        {
            result = string.Empty;
        }

        // Flow-state after null check: maybe is known non-null inside the if, but that knowledge does not
        // carry outside without explicit check.
        return result;
    }

    // Reachability: the method below has an unconditional return, so code after would be unreachable.
    // A diagnostic example would be:
    //   return 0;
    //   int unreachable = 1; // CS0162 unreachable code
    // That example is not present as live code; the comment preserves the intended diagnostic shape.
    // Similarly, reading an unassigned variable:
    //   int unassigned; Console.WriteLine(unassigned); // CS0165 use of unassigned local
    // is a diagnostic and is shown only as a comment.

    // Else-branch failure is illustrated by ensuring every branch assigns before use.
    public static int ElseBranchFailureExample(bool condition)
    {
        int value;
        if (condition)
        {
            value = 100;
        }
        else
        {
            value = 200;
        }

        return value;
    }

    // Local shadowing rejection:
    //   void Invalid() { int item = 1; { int item = 2; } } // CS0136 local shadows enclosing
    // That invalid shape is documented but not emitted.

    private static (int, int) GetPair() => (3, 4);
}

public struct StructHolder
{
    public int X;
    public int Y;

    public StructHolder(int x, int y)
    {
        X = x;
        Y = y;
    }
}

public sealed class ClassHolder
{
    public int X { get; set; }

    public int Y { get; set; }

    public ClassHolder()
    {
    }

    public ClassHolder(int x, int y)
    {
        X = x;
        Y = y;
    }
}
