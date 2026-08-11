library;

class StatefulBase {
  int _state = 0;

  void bump() {
    _state++;
  }

  int get state => _state;
}
