#include <Python.h>

static PyObject *ext_hello(PyObject *self, PyObject *Py_UNUSED(args)) {
    return PyUnicode_FromString("native-hello");
}

static PyMethodDef methods[] = {
    {"hello", ext_hello, METH_NOARGS, "Return hello from native extension"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moddef = {
    PyModuleDef_HEAD_INIT,
    "_native_ext",
    "Native extension representative for PY-CAN-MOD-017",
    -1,
    methods
};

PyMODINIT_FUNC PyInit__native_ext(void) {
    return PyModule_Create(&moddef);
}
