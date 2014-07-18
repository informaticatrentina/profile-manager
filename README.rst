.. -*- coding: utf-8 -*-

======================
ProfileManager project
======================


Developer Instructions
======================


Requirements
------------

This guide assumes that you develop the ``ProfileManager project`` on a
``Debian/GNU Linux`` version ``Wheezy``.

.. code:: sh

    sudo apt-get install python-virtualenv \
    libsqlite3-0 \

For pillow with jpg support we need also:

.. code:: sh

    sudo apt-get build-dep python-imaging


Virtualenv
----------

There are several tools that help to manage python virtualenvs.  If you are
already familiar with ``virtualenvwrapper`` you can use it.  If not just follow
the following suggestions:

.. code:: sh

    cd
    mkdir ve
    cd ve
    vitutualenv ProfileManagerVe project-ve
    . ProfileManagerVe/bin/activate

.. warning::

    Remember to activate the virtualenv every time you start developing.


Source code
-----------

The source code is manage with ``git`` using the ``git-flow`` work-flow.

You should have an account with writing privileges.

.. code:: sh

    cd
    mkdir dev
    cd dev
    git clone git@git.ahref.eu:aggregator/ProfileManager.git
    cd ProfileManager
    git checkout -b develop origin/develop


Development
-----------

The ``ProfileManager project`` is developed as a python packages.  The
``develop`` command will download and install the requirements.

.. code:: sh

    python setup.py develop

You can start developing following the issues for your milestone.


I18n
----

To add a new translation language use:

.. code:: sh

    pybabel init -i messages.pot -d ProfileManager/translations -l $LANG_CODE

where ``$LANG_CODE`` is usually ``it`` for Italian, ``de`` for ...

To extract, update and compile messages just run:

.. code:: sh

    make i18n


Testing
-------

``ProfileManager project`` follow a strict testing procedure.  Before every
commit you must check that the test pass and that the source code respect the
best practices defined by the ``python`` community.

.. code:: sh

    python setup.py test
    python setup.py flake8

An improved test runner is:

.. code:: sh

    nosetests -c nose.cfg

This will open a ``ipdb`` shell in case of errors and failures and provide a
coverage report.


Documentation
-------------

The developer documentation is made with ``sphinx`` and in particular with
``sphinxcontrib.autohttp.flask``.  A quick start:

.. code:: sh

    cd docs
    make singlehtml
    xdg-open build/singlehtml/index.html


Manage command
--------------

For convenience other flask related commands are available, just run
``pm`` to see the list.


Packaging
---------

.. code: sh

    python setup.py sdist

Will create an archive named something like: `dist/ProfileManager-<version>.tar.gz`


Installing in production
------------------------

After using the right user and entered in the right virtual environment, the
following command will take care of all the install:

.. code: sh

    pip install /path/to/ProfileManager-<verision>.tar.gz


If you experience some problem with the dependencies, just start with a brand
new virtualenv.  Please note that if you use a new virtualenv, the uwsgi config
file need to be updated!
