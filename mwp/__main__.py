# Muck about with paths :(
import sys
import os
CURRENT_PATH = os.path.dirname(__file__)
PARENT_PATH = os.path.split(CURRENT_PATH)[0]
sys.path.insert(0, PARENT_PATH)

from mwp import web

web.main()
