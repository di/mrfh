mrfh (Multiprocess Rotating File Handler)
=========================================

.. image:: https://travis-ci.org/di/mrfh.svg?branch=master
    :target: https://travis-ci.org/di/mrfh

Description
-----------

The `MultiprocessRotatingFileHandler` is a drop-in replacement for the
`logging` modules's `RotatingFileHandler
<https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`__
which provides a process-safe rotating log file handler using file-based locks.

Documentation
-------------

Installation
~~~~~~~~~~~~

Installing:

::

    $ pip install mrfh

Quickstart
~~~~~~~~~~

Where you once had:

.. code:: python

    from logging.handlers import RotatingFileHandler

    logger = logging.getLogger('my_logger')
    handler = RotatingFileHandler('my_log.log', maxBytes=2000, backupCount=10)
    logger.addHandler(handler)

    logger.debug('Some debug message!')

You can now have:

.. code:: python

    from mrfh import MultiprocessRotatingFileHandler

    logger = logging.getLogger('my_logger')
    handler = MultiprocessRotatingFileHandler('my_log.log', maxBytes=2000, backupCount=10)
    logger.addHandler(handler)

    logger.debug('Some debug message!')

Your rotating file handler is now process-safe!

Testing
~~~~~~~

To run the tests:

::

    python setup.py test

Authors
-------

-  `Dustin Ingram <https://github.com/di>`__

Credits
-------

Roughly based on the defunct `ConcurrentLogHandler
<https://launchpad.net/python-concurrent-log-handler>`__.

License
-------

Open source MIT license.
