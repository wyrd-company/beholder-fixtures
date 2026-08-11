/*
 * Declarations for a small, stable subset of the C standard library, used
 * only as ffigen's parse input (DART-CAN-BUILD-005). This header is never
 * compiled; the bound symbols already exist in every Linux libc, so the
 * committed generated bindings resolve them from the running process at
 * runtime via `DynamicLibrary.open`.
 */
#ifndef TOOLSHED_LIBC_SUBSET_H
#define TOOLSHED_LIBC_SUBSET_H

#include <stddef.h>

/* Computes the length of a NUL-terminated byte string, scanning at most
 * max_length bytes. */
size_t strnlen(const char *string, size_t max_length);

/* Rounds a double to the nearest integer value, halfway cases away from
 * zero. */
double round(double value);

#endif
