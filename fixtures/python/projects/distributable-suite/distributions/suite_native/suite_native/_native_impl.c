#include <Python.h>

static PyObject *hello(PyObject *self, PyObject *args) {
    return PyUnicode_FromString("hello from native");
}

static PyMethodDef methods[] = {
    {"hello", hello, METH_NOARGS, "Return greeting"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_native_impl",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC PyInit__native_impl(void) {
    return PyModule_Create(&moduledef);
}
