"""
Runs updates to widgets in background

TODO:  This is WIP - Take a look at the daemoniker package and refactor.
"""

import subprocess
import sys
import os
import typing
import presalytics.lib.exceptions


class BackgrounderMixIn(object):
    """
    A quick and dirty implementation to "daemonize" updating of widgets.
    TODO: Some research to make this more robust and cross-platform


    A note to script kiddies: the pickled objects are never serailized
    server-side.  The only computer you'll be hacking is your own.
    """

    DETACHED_PROCESS = 8

    def __init__(self):
        self.path_to_current_interpreter = sys.executable
        if os.name == 'nt':
            self.isWindows = True
            self.process_file = "background_linux.py"
        else:
            self.isWindows = False
            self.process_file = "background_nt.pyw"

    def run_in_background(self):
        if not getattr(self, "update", None):
            message = "The {} object requires an update() method with no parameters in order to use BackgrounderMixin".format(self.__class__.__name__)
            raise presalytics.lib.exceptions.InvalidConfigurationError(message)
        else:
            update_method = getattr(self, "update")
            try:
                bound = update_method.im_self
            except AttributeError:
                message = "The update attribute on the {} object must be a bound method".format(self.__class__.__name__)
                raise presalytics.lib.exceptions.InvalidConfigurationError(message)
            if not bound:
                message = "the update method is not bound to the class and cannot be serialized"
                raise presalytics.lib.exceptions.InvalidConfigurationError(message)
        p = subprocess.run(self.process_file, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    @staticmethod
    def get_backgrounded_widgets() -> typing.List[str]:
        pass

    @staticmethod
    def kill_backgrounded_widget(widget_name: str) -> bool:
        pass
        
    def kill_background(self) -> bool:
        return BackgrounderMixIn.kill_backgrounded_widget(self.name)

        
            
            
        

        