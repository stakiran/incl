# -*- coding: utf-8 -*-

import os
import subprocess

def execute(cmdline):
    """ NonBlocking Execution.
    @return A return code. """
    childobj = subprocess.Popen(cmdline, shell=True)
    childobj.communicate()
    return childobj.returncode
