#!/usr/bin/python2.7


import cgi, cgitb
cgitb.enable()
import os
import sys
os.chdir('/nfs/stak/students/j/myusername/')
from numpy import *
from scipy.interpolate import interp1d
from scipy.integrate import trapz
from scipy.optimize import minimize_scalar
from csv import DictReader, QUOTE_NONNUMERIC
from matplotlib import *
 
form = cgi.FieldStorage() 

daylength = dict([('March',11.83),('April',13.4),('May',14.73),('June',15.42),('July',15.12),('August',13.97),('September',12.45)])

# Get data from fields
Total_Daphnia = form.getvalue('Total_Daphnia')
Daphnia_Size  = form.getvalue('Daphnia_Size')
Month = form.getvalue('Month')




print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Here are the results based on selected values.</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s %s</h2>" % (first_name, last_name, Month)
print "</body>"
print "</html>"
