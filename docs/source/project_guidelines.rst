Project guidelines
==================


Project planning workflow
-------------------------

All projects will be initially documented on the `Foundation Podio instance
<https://podio.com/stream>`_. The final client could be invited to the podio
workspace.


License
-------

While we don't know at the moment which license will be used for the
distribution of the applications developed, we will write every application
using strict coding standards, under the understanding that it might be released
as open source.

Standard copyright disclaimer (to be included with all source code files):

Copyright template for source files::

    Copyright (c) 2013 <ahref Foundation -- All rights reserved.
    Author: Name Surname <user@example.com>

    This file is part of <project_name>.

    This file can not be copied and/or distributed without the express
    permission of <ahref Foundation.


Development Tools and Practices
-------------------------------

All the project of <ahref are web based platform. We will follow best practices
on web development with a standard set of tools.

We acknowledge that web platform have to be usable from mobile phones and that
an integration with mobile apps could be done in the near feature.


gitlab
++++++

Our preferred distribuited version control system is `git
<http://git-scm.com/>`_.

The branching model of our projects will be managed with `git-flow
<https://github.com/nvie/gitflow>`_.

We will use our `gitlab <http://gitlab.ahref.eu/>`_ installation for::

- Code review
- Wiki (Maily for wip documentation)
- Milestone planning
- Issues traking
- Merge Requests
- Continuous Integration (with ``gitlab-ci``)


Weekly meeting
++++++++++++++

A weekly meeting will be held on ``Skype`` every Friday at 9 Europe/Rome between
developers and project managers.


Code review
+++++++++++

Peer code review will be performed on all code committed to the repository.

Code review will be done post commit.

Developer will declare on ``skype flow`` or using the gitlab issue tracker that
he is going to finish a part of feature by when, any one from development group
can pick the code review.

Code review will be done on gitlab may be by screen sharing. Code with fixes
suggested in code review need to be checked in with proper message in commit.


Testing
+++++++

Unit testing will be used to test all API.

Additionally static check will be performed:


- on ``Python``, using ``pylint``
- on ``PHP``, using ``CodeSniffer``
- on ``JavaScript`` using ``Jshint``

Front-end development will be tested on the latest major browser versions,
depending on the audience of the project.

Responsive design will be tested using ``viewport resizer``.


Languages and frameworks
++++++++++++++++++++++++

- CSS development will be based on ``Bootstrap``.
- `flask micro framewor <http://flask.pocoo.org/>`_ for the backend
- `YII framework <http://www.yiiframework.com/>`_ for the frontend
- jQuery will be our main Javascript library
- we could evaluate later EXTJS for the administration part


Other software
--------------

``postgresql`` and ``mongodb`` will be our primary choice as database servers.


Documentation
-------------

We will document all the project using:

- Inline comments
- Function and parameter documentation using sphinx-autodoc (for python)
- Development environment documentation sphinx
- Service documentation: follow the `opscard
  <http://opsreportcard.com/section/11>`_ best practices
