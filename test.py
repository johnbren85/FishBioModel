#!/usr/bin/python2.7


import cgi, cgitb
cgitb.enable() 

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>This is where we get user input.</title>'
print '</head>'
print '<body>'
print '<h2>Enter Values for Bioenergetics model</h2>'


<form action="/nfs/stak/students/j/myusername/testenv/Working.py" method="get">
Total Daphnia: <input type="text" name="Total Daphnia">  <br />

Daphnia Size: <input type="text" name="Daphnia Size" />  <br />

Please Select Month: <select name="Month">
<option value="March" selected>March</option>
<option value="April">April</option>
<option value="May">May</option>
<option value="June">June</option>
<option value="July">July</option>
<option value="August">August</option>
</select>
<input type="submit" value="Submit"/>
</form>
 
print '</body>'
print '</html>'
