# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 <ahref Foundation -- All rights reserved.
# Author: Daniele Pizzolli <daniele@ahref.eu>
#
# This file is part of the ProfileManager project.
#
# This file can not be copied and/or distributed without the express
# permission of <ahref Foundation.
#
###############################################################################


'''
The manager of “Profile Manager”
=================================

'''


from flask.ext.script import Manager, Server
from ProfileManager import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    port=8002,
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


def main():
    '''Convenience function to run the manager'''
    manager.run()


if __name__ == "__main__":
    main()
