/* _native_multi.c — multi-phase extension with per-module state */
#include <Python.h>

typedef struct {
    long counter;
    PyObject *last_label;
} multi_state;

static PyObject *multi_get_counter(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    multi_state *st = (multi_state *)PyModule_GetState(self);
    if (!st) return NULL;
    return PyLong_FromLong(st->counter);
}

static PyObject *multi_increment(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    multi_state *st = (multi_state *)PyModule_GetState(self);
    if (!st) return NULL;
    st->counter += 1;
    Py_RETURN_NONE;
}

static PyObject *multi_set_label(PyObject *self, PyObject *args) {
    multi_state *st = (multi_state *)PyModule_GetState(self);
    const char *label;
    if (!PyArg_ParseTuple(args, "s", &label)) return NULL;
    PyObject *new_label = PyUnicode_FromString(label);
    if (!new_label) return NULL;
    Py_XSETREF(st->last_label, new_label);
    Py_RETURN_NONE;
}

static PyObject *multi_get_label(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    multi_state *st = (multi_state *)PyModule_GetState(self);
    if (!st) return NULL;
    if (!st->last_label) Py_RETURN_NONE;
    Py_INCREF(st->last_label);
    return st->last_label;
}

static PyMethodDef multi_methods[] = {
    {"get_counter", multi_get_counter, METH_NOARGS, "Return per-module counter"},
    {"increment", multi_increment, METH_NOARGS, "Increment per-module counter"},
    {"set_label", multi_set_label, METH_VARARGS, "Set per-module label"},
    {"get_label", multi_get_label, METH_NOARGS, "Get per-module label"},
    {NULL, NULL, 0, NULL}
};

static int multi_traverse(PyObject *mod, visitproc visit, void *arg) {
    multi_state *st = (multi_state *)PyModule_GetState(mod);
    if (st) Py_VISIT(st->last_label);
    return 0;
}

static int multi_clear(PyObject *mod) {
    multi_state *st = (multi_state *)PyModule_GetState(mod);
    if (st) Py_CLEAR(st->last_label);
    return 0;
}

static void multi_free(void *mod) {
    /* free called with module object */
}

static int multi_exec(PyObject *mod) {
    multi_state *st = (multi_state *)PyModule_GetState(mod);
    if (!st) return -1;
    st->counter = 0;
    st->last_label = PyUnicode_FromString("initialized");
    if (!st->last_label) return -1;
    return 0;
}

static struct PyModuleDef_Slot multi_slots[] = {
    {Py_mod_exec, multi_exec},
    {0, NULL}
};

static struct PyModuleDef multi_def = {
    PyModuleDef_HEAD_INIT,
    "_native_multi",
    "Multi-phase extension with per-module state (PEP 489)",
    sizeof(multi_state),
    multi_methods,
    multi_slots,
    multi_traverse,
    multi_clear,
    multi_free
};

PyMODINIT_FUNC PyInit__native_multi(void) {
    return PyModuleDef_Init(&multi_def);
}
