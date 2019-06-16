=========
timertool
=========

A simple timer tool to measure time of execution peaces of code. Could be used as a context-manager

Usage
=====

To start working with the ``timertool`` first import the ``timer`` function:

.. code-block::

    from timertool import timer

The ``timer`` function returns an object that provides ``start`` and ``stop`` methods. The ``start`` method
saves the beginning time, the ``stop`` method saves the time duration between these calls. To access
the elapsed time duration use the ``time`` property:

.. code-block::

    t = timer()
    t.start()
    ...
    t.stop()
    t.time  # contains the total elapsed time

You also could use the ``time`` property between ``start`` and ``stop`` calls, in this case it would contain
the time currently elapsed from the ``start`` call:

.. code-block::

    t = timer()
    t.start()
    t.time  # contains the currently elapsed time
    ...

The ``timertool`` also supports a content manager syntax:

.. code-block::

    with timer() as t:
        ...
        t.time  # contains the currently elapsed time
    t.time  # contains the total elapsed time

The ``timertool`` contains a ``timelog`` decorator that logs to stdout
the time of function executin:

.. code-block::

    from timertool import timelog

    @timelog
    def foo(*args, **kwargs):
        ...

    foo(1, bar='baz')  # print a time of foo execution
