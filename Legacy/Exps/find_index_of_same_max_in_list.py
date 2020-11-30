from Utopia_tools import *
from datetime import date, datetime
from dateutil import rrule, relativedelta

#find_index_of_same_max_in_list.py

a = [32, 37, 28, 30, 37, 25, 27, 24, 35, 55, 23, 31, 55, 21, 40, 18, 50,
             35, 41, 49, 37, 19, 40, 41, 31]

m = max(a)
print([i for i, j in enumerate(a) if j == m])