from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys, math
import numpy as np
import matplotlib.pyplot as plt
from dateutil import rrule
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO
from random import randint
from subprocess import call,check_output

import pickle

a = {
  'a': 1,
  'b': 2
}

with open('file.txt', 'wb') as handle:
  pickle.dump(a, handle)

with open('file.txt', 'rb') as handle:
  b = pickle.loads(handle.read())

print a == b # True


