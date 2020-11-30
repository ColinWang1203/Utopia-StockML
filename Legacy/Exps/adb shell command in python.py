from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO

from subprocess import call,check_output

for i in list(range(125,400)) :
    print('keycode is '+str(i))
    check_output(["adb", "shell", "input", "keyevent", str(i)])
    sleep(0.5)



