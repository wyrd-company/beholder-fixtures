/* libnative_kit.c — tiny native library for ctypes FFI */
#include <stddef.h>

struct Point {
    int x;
    int y;
};

int add_ints(int a, int b) {
    return a + b;
}

double scale_double(double value, double factor) {
    return value * factor;
}

struct Point make_point(int x, int y) {
    struct Point p = {x, y};
    return p;
}

int point_sum(struct Point p) {
    return p.x + p.y;
}

typedef int (*callback_t)(int value);

int apply_callback(callback_t cb, int value) {
    if (!cb) return -1;
    return cb(value);
}

/* Thread-local error indicator: demonstrates thread-local errors variant */
static __thread int last_error = 0;

int divide_checked(int a, int b) {
    if (b == 0) {
        last_error = 1;
        return 0;
    }
    last_error = 0;
    return a / b;
}

int get_last_error(void) {
    return last_error;
}

void clear_last_error(void) {
    last_error = 0;
}
