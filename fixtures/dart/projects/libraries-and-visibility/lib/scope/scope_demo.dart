library;

// A library-scope (top-level) binding. Nothing in `ScopeDemo.describe()`
// shadows this name at any block, local, or member level, so every
// reference to it resolves through library-level lookup, the outermost
// scope a name passes through.
int _libraryScopeOffset = 1000;

class ScopeDemo {
  int field = 1;

  String describe() {
    // Local lookup: this `field` shadows the member `field` within the rest
    // of this block. `this.field` below disambiguates back to the member.
    final field = this.field + 10;

    String describeOuterLocal() =>
        'outer:$field'; // Member/local lookup from a nested function.

    String render() {
      // Block lookup: this innermost `field` shadows both the outer local
      // and the member within this nested block. `_libraryScopeOffset`
      // alongside it resolves via library lookup, unaffected by any of the
      // block/local/member shadowing above.
      final field = this.field * 100;
      return 'inner:$field outer-local:${describeOuterLocal()} member:${this.field} library:$_libraryScopeOffset';
    }

    return render();
  }
}
