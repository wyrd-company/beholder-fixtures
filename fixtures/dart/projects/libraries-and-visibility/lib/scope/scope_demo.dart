library;

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
      // and the member within this nested block.
      final field = this.field * 100;
      return 'inner:$field outer-local:${describeOuterLocal()} member:${this.field}';
    }

    return render();
  }
}
