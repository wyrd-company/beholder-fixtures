/* _native_single.c — single-phase extension, ownership and GIL demos */
#include <Python.h>
#include <structmember.h>
#include <unistd.h>

/* ---- heap type: Counter ---- */

typedef struct {
    PyObject_HEAD
    long value;
} CounterObject;

static PyObject *Counter_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    CounterObject *self = (CounterObject *)type->tp_alloc(type, 0);
    if (self) self->value = 0;
    return (PyObject *)self;
}

static int Counter_init(CounterObject *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"value", NULL};
    long v = 0;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|l", kwlist, &v)) return -1;
    self->value = v;
    return 0;
}

static void Counter_dealloc(CounterObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *Counter_get_value(CounterObject *self, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromLong(self->value);
}

static PyObject *Counter_increment(CounterObject *self, PyObject *Py_UNUSED(ignored)) {
    self->value += 1;
    Py_RETURN_NONE;
}

static PyMethodDef Counter_methods[] = {
    {"get_value", (PyCFunction)Counter_get_value, METH_NOARGS, "Return current value"},
    {"increment", (PyCFunction)Counter_increment, METH_NOARGS, "Increment value"},
    {NULL, NULL, 0, NULL}
};

static PyMemberDef Counter_members[] = {
    {"value", T_LONG, offsetof(CounterObject, value), 0, "counter value"},
    {NULL}
};

static PyType_Slot Counter_slots[] = {
    {Py_tp_new, Counter_new},
    {Py_tp_init, Counter_init},
    {Py_tp_dealloc, Counter_dealloc},
    {Py_tp_methods, Counter_methods},
    {Py_tp_members, Counter_members},
    {0, NULL}
};

static PyType_Spec Counter_spec = {
    "native_extension_kit._native_single.Counter",
    sizeof(CounterObject),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    Counter_slots
};

/* ---- functions demonstrating ownership and errors ---- */

static PyObject *owned_new_string(PyObject *self, PyObject *args) {
    const char *text;
    if (!PyArg_ParseTuple(args, "s", &text)) return NULL;
    /* owned reference: caller receives new reference */
    return PyUnicode_FromString(text);
}

static PyObject *borrowed_peek(PyObject *self, PyObject *args) {
    PyObject *seq;
    Py_ssize_t index;
    if (!PyArg_ParseTuple(args, "On", &seq, &index)) return NULL;
    /* PyList_GetItem returns borrowed reference; must INCREF before return */
    PyObject *item = PyList_GetItem(seq, index);
    if (!item) {
        PyErr_SetString(PyExc_IndexError, "borrowed_peek: index out of range");
        return NULL;
    }
    Py_INCREF(item);
    return item;
}

static PyObject *container_transfer(PyObject *self, PyObject *args) {
    PyObject *list;
    PyObject *item;
    if (!PyArg_ParseTuple(args, "OO", &list, &item)) return NULL;
    if (!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "first argument must be list");
        return NULL;
    }
    /* PyList_Append increments refcount; demonstrate container transfer */
    Py_INCREF(item);
    if (PyList_Append(list, item) < 0) {
        Py_DECREF(item);
        return NULL;
    }
    Py_DECREF(item);
    Py_RETURN_NONE;
}

static PyObject *tuple_steal_demo(PyObject *self, PyObject *args) {
    PyObject *a;
    PyObject *b;
    if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;
    PyObject *tuple = PyTuple_New(2);
    if (!tuple) return NULL;
    Py_INCREF(a);
    Py_INCREF(b);
    /* PyTuple_SetItem steals reference */
    PyTuple_SetItem(tuple, 0, a);
    PyTuple_SetItem(tuple, 1, b);
    return tuple;
}

static PyObject *raise_native_error(PyObject *self, PyObject *args) {
    const char *msg;
    if (!PyArg_ParseTuple(args, "s", &msg)) return NULL;
    PyErr_SetString(PyExc_ValueError, msg);
    return NULL;
}

static PyObject *raise_without_error(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    /* Incorrect pairing: returns NULL without setting exception -> SystemError in Python */
    return NULL;
}

static PyObject *return_with_error_set(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    /* Incorrect pairing: sets error but returns non-NULL -> SystemError */
    PyErr_SetString(PyExc_RuntimeError, "error set but returning value");
    Py_RETURN_NONE;
}

static PyObject *blocking_work(PyObject *self, PyObject *args) {
    long millis;
    if (!PyArg_ParseTuple(args, "l", &millis)) return NULL;
    /* Release GIL around blocking work; reacquire afterwards */
    Py_BEGIN_ALLOW_THREADS
    usleep((useconds_t)(millis * 1000));
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject *call_python_while_detached_error(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    /* Demonstrates that Python API must not be called while GIL is released.
       This function intentionally shows the guard: we release and immediately
       reacquire before calling Python API. Calling PyUnicode_FromString while
       detached would be undefined; we avoid it. */
    Py_BEGIN_ALLOW_THREADS
    /* blocking section - no Python API here */
    Py_END_ALLOW_THREADS
    return PyUnicode_FromString("gil-reacquired-then-called");
}

static PyMethodDef single_methods[] = {
    {"owned_new_string", owned_new_string, METH_VARARGS, "Return new owned string"},
    {"borrowed_peek", borrowed_peek, METH_VARARGS, "Peek list item via borrowed reference"},
    {"container_transfer", container_transfer, METH_VARARGS, "Transfer ownership into container"},
    {"tuple_steal_demo", tuple_steal_demo, METH_VARARGS, "Create tuple stealing references"},
    {"raise_native_error", raise_native_error, METH_VARARGS, "Set ValueError and return NULL"},
    {"raise_without_error", raise_without_error, METH_NOARGS, "Return NULL without error (SystemError)"},
    {"return_with_error_set", return_with_error_set, METH_NOARGS, "Set error but return value (SystemError)"},
    {"blocking_work", blocking_work, METH_VARARGS, "Release GIL around blocking sleep"},
    {"call_python_while_detached_error", call_python_while_detached_error, METH_NOARGS, "Shows GIL reacquire before Python API"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef single_def = {
    PyModuleDef_HEAD_INIT,
    "_native_single",
    "Single-phase extension with ownership and GIL demos",
    -1,
    single_methods,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__native_single(void) {
    PyObject *mod = PyModule_Create(&single_def);
    if (!mod) return NULL;
    PyObject *counter_type = PyType_FromSpec(&Counter_spec);
    if (!counter_type) {
        Py_DECREF(mod);
        return NULL;
    }
    if (PyModule_AddObject(mod, "Counter", counter_type) < 0) {
        Py_DECREF(counter_type);
        Py_DECREF(mod);
        return NULL;
    }
    return mod;
}
