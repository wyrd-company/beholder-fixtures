#include <stdint.h>
#include <string.h>
#include <errno.h>

#if defined(_WIN32) || defined(_MSC_VER)
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

// native_add is the canonical native operation bound via both DllImport
// and LibraryImport. Uses only blittable 32-bit integers.
EXPORT int32_t native_add(int32_t a, int32_t b)
{
    return a + b;
}

// native_transform exercises marshalled types (UTF-8 string, boolean-as-int)
// alongside a blittable integer so one export demonstrates both families.
EXPORT int32_t native_transform(int32_t value, const char *tag, int32_t use_tag)
{
    if (use_tag != 0 && tag != NULL)
    {
        return value + (int32_t)strlen(tag);
    }

    return value;
}

// native_set_error stores a caller-supplied code in errno so SetLastError
// callers can observe last-error propagation. Returns the stored code.
EXPORT int32_t native_set_error(int32_t code)
{
    errno = code;
    return code;
}
