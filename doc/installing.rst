..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _installing:

**********
Installing
**********

.. highlight:: bash

.. note::

    Using :term:`Virtualenv` is recommended when evaluating or running locally.

Installation is simple with `pip <http://www.pip-installer.org/>`_::

    pip install sawmill

Building from source
====================

You can also build manually from the source for more control. First obtain a
copy of the source by either `downloading
<https://github.com/4degrees/sawmill/zipball/master>`_ or cloning the public
repository::

    $ git clone https://github.com/4degrees/sawmill

Then you can build and install the package into your current Python
site-packages folder::

    pip install .

When actively developing, you can install an editable version along with
additional dependencies for building and running tests::

    pip install -e .[dev]

Alternatively, just build locally and manage yourself::

    python setup.py build

Building documentation from source
----------------------------------

To build the documentation from source::

    python setup.py build_sphinx

Then view in your browser::

    file:///path/to/sawmill/build/doc/html/index.html

Running tests against the source
--------------------------------

With a copy of the source it is also possible to run the unit tests::

    python setup.py -q test

With a coverage report::

    python setup.py -q test --addopts --cov=sawmill
