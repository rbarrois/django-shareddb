# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

"""Utilities to delegate execution of a set of functions to a single background thread."""


import contextlib
import logging
from .compat import queue
import threading

logger = logging.getLogger(__name__)


class Task(object):
    """A simple object representing a task to run."""
    KIND_STOP = 'STOP'
    KIND_DATA = 'DATA'

    def __init__(self, kind=KIND_DATA, function=None, args=None, kwargs=None):
        self.kind = kind
        self.function = function
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.done = threading.Event()
        self.result = None
        self.exception = None

    def execute(self):
        """Execute the task.

        This *will* catch exceptions raised within the task, and won't re-raise them.
        """
        try:
            self.result = self.function(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e
        self.done.set()

    def __repr__(self):
        if self.kind == self.KIND_STOP:
            return '<Task: STOP>'
        if not self.done.is_set():
            return "<Task: %s(*%r, **%r) (pending)>" % (
                self.function, self.args, self.kwargs)
        if self.exception is None:
            return "<Task: %s(*%r, **%r) --> %r>" % (
                self.function, self.args, self.kwargs, self.result)
        else:
            return "<Task: %s(*%r, **%r) !-> %r>" % (
                self.function, self.args, self.kwargs, self.exception)


STOP_TASK = Task(kind=Task.KIND_STOP)


class DelegateThread(threading.Thread):
    """Support for the background work."""
    def __init__(self, queue, name=None):
        self.queue = queue
        super(DelegateThread, self).__init__(name=name)

    def run(self):
        while True:
            with self.queue.consume() as task:
                if task.kind == task.KIND_STOP:
                    break
                task.execute()


class DelegateQueue(object):
    """Delegates calls to a background thread.

    Can be used to enforce serialized accesses, or to wrap calls to a
    non-thread-safe library.

    Usage:

        >>> queue = threlegate.DelegateQueue(name='bg-task')  # Optional name for thread naming
        >>> queue.start()
        >>> queue.execute(os.path.join, '/', 'foo')
        '/foo'
        >>> queue.stop()

    Notes:
        * If a ``name`` is provided, it is used for the underlying thread (helps with logging)
        * When the DelegateQueue is garbage-collected, it will attempt to stop the background thread
        * There is a single, synchronous entry point for code execution: ``execute(callable, *args, **kwargs)
    """

    def __init__(self, name=None):
        self.inner_queue = queue.Queue()
        self.started = False
        self.inner_thread = None
        self.name = name

    # Thread management
    # =================

    def start(self):
        assert not self.started
        self.inner_thread = DelegateThread(queue=self, name=self.name)
        self.inner_thread.daemon = True
        self.inner_thread.start()
        self.started = True
        logger.debug("Started delegate thread %s(%s) from %s(%s)",
            self.inner_thread.ident, self.inner_thread.name,
            threading.current_thread().ident, threading.current_thread().name,
        )

    def stop(self):
        assert self.started
        self.inner_queue.put(STOP_TASK)
        self.inner_queue.join()

    def __del__(self):
        self.stop()

    # Incoming tasks
    # ==============

    def execute(self, function, *args, **kwargs):
        assert self.started

        if threading.current_thread().ident == self.inner_thread.ident:
            # Don't delegate tasks generated from within another task,
            # as that would lock.
            return function(*args, **kwargs)

        # We're calling from outside the worker thread, let's run properly.
        task = Task(function=function, args=args, kwargs=kwargs)
        self.inner_queue.put(task)

        # Wait for completion
        task.done.wait()
        if task.exception is not None:
            raise task.exception
        return task.result

    # Thread-side functions
    # =====================

    def _assert_in_thread(self):
        """Ensure that the code is executing within the background thread."""
        assert threading.current_thread().ident == self.inner_thread.ident

    @contextlib.contextmanager
    def consume(self, block=True, timeout=None):
        """Handle an incoming task.

        This code *must* be executed within the background thread."""
        self._assert_in_thread()

        item = self.inner_queue.get(block=block, timeout=timeout)
        try:
            yield item
        finally:
            self.inner_queue.task_done()


