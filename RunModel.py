#!C:\Anaconda3\python.exe

import os
import sys
import csv
from Bioenergetics import *
import cgi, cgitb
import pylab
from io import BytesIO
from PIL import Image, ImageDraw
import base64
from scipy.interpolate import griddata
import pandas
import seaborn
cgitb.enable()
os.chdir(r'C:\xampp\cgi-bin')

def Sensitivity_Expand(Sparam_Range, Sparam_Exp):
    step_size = Sparam_Range/5
    Sparam_Range = Sparam_Range*-1
    for i in range(0,11):
        Sparam_Exp.append(Sparam_Range)
        Sparam_Range = Sparam_Range + step_size
    return Sparam_Exp


form = cgi.FieldStorage()
# Get data from fields
if form.getvalue('defa') == 'yes':
    def_flag = 'YES'
else:
    def_flag = 'NO'

if form.getvalue('depr') == 'yes':
    depr_flag = 'YES'
else:
    depr_flag = 'NO'

if def_flag == 'YES':
    Total_Daphnia = 1000
    DaphSize = .5
    Month = 'May'
    k = .5
    StartingMass = 60
    Year = '2015'
    Site = 'Fall Creek'
    Dmax = 1000
    Dmin = -1
else:
    StartingMass = float(form.getvalue('Starting_Mass_In'))
    Total_Daphnia = float(form.getvalue('Total_Daphnia_Input_Name'))
    DaphSize  = float(form.getvalue('Daphnia Size'))
    Month = form.getvalue('Month')
    k = float(form.getvalue('K'))
    StartingMass = float(form.getvalue('Starting_Mass_In'))
    Year = form.getvalue('Year')
    Site = form.getvalue('Site')
    if depr_flag == 'YES':
        Dmax = float(form.getvalue('DmaxIn'))
        Dmin = float(form.getvalue('DminIn'))
    else:
        Dmax = 10000
        Dmin = -1
    #Dmax = float(form.getvalue('DmaxIn'))
    #Dmin = float(form.getvalue('DminIn'))

print ('Content-type:text/html; charset=utf-8\r\n\r\n')
print ('<html>')
print ('<head>')
print ('<title>Here are Your Results.</title>')
print ('</head>')


FreshBatch = Batch(Site, Month, Year, k, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin)
BaseResults = FreshBatch.Run_Batch()

print ('''<h3>Input Values:<br>
       Starting Mass - %f <br>
       Total Daphnia - %f <br>
       Daphnia Size - %f <br>
       k - %f <br>
       Month - %s <br>
       Site - %s <br>
       Year - %s</h3>''' % (StartingMass,Total_Daphnia,DaphSize,k,Month,Site,Year))
if def_flag == "NO":
    print('''<h3>Depth restricted to between %fm and %fm.</h3>''' % (Dmin,Dmax))

fig = pyplot.figure()
massax = fig.add_subplot(221)
massax.plot(BaseResults['StartingMass'])
massax.set_ylabel('Mass')
grax = fig.add_subplot(222)
grax.plot(BaseResults['growth'])
grax.set_ylabel('Growth')
dax = fig.add_subplot(223)

if def_flag == 'NO':
    df = pandas.read_csv('FCApril15.csv')
    OldTemps = df.Temperature
    OldDays = df.Day
    OldDepths = df.Depth
    NewTemps = []
    NewDepths = []
    NewDays = []
    for i in range(30):
        for j in range(len(OldDepths)):
            if ((OldDepths[j] < Dmax) and (OldDepths[j] > Dmin)):
                NewDays.append(i)
                NewDepths.append(OldDepths[j])
                NewTemps.append(OldTemps[j])

    columns = ["Days", "Depths", "Temperatures"]
    index = NewDays
    df_ = pandas.DataFrame(index=index, columns=columns)
    df_ = df_.fillna(0)
    df_.Days = NewDays
    df_.Depths = NewDepths
    df_.Temperatures = NewTemps
    df_.to_csv('output.csv')



#temps = pandas.read_csv('output.csv')
#temps = temps.pivot_table("Temperatures","Depths", "Days")
#dax =seaborn.heatmap(temps, xticklabels=5, yticklabels=5, vmin = 0, vmax=25, cmap = pyplot.cm.rainbow)
dax.plot(BaseResults['day_depth'], 'black')
dax.set_ylabel('Day Depth')
nax = fig.add_subplot(224)
#nax = seaborn.heatmap(temps, xticklabels=5, yticklabels=5, vmin=0, vmax=25, cmap=pyplot.cm.ocean)
nax.set_ylabel('Night Depth')
nax.plot(BaseResults['night_depth'],'black')
#CS = nax.contourf(xi, yi, zi, 15, cmap=pyplot.cm.winter
fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
#pyplot.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pylab.savefig( "new.png")
data_uri = base64.b64encode(open('new.png', 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)
os.remove('new.png')

print ('''<h3>Output Values: Final Mass - %f <br>
       Final Daily Growth - %f <br>
       Final Day Depth - %f <br>
       Final Night Depth - %f <br>
       </h3>''' % (StartingMass,BaseResults['growth'][29],BaseResults['day_depth'][29],BaseResults['night_depth'][29]))

print('''
<form action="RunModel.py" method="post">

Use Default Values? <input type="radio" name="defa" value="yes" /> Yes
<input type="radio" name="subject" value="physics" /> No<br>

Fish Starting Mass:<input type="range" name="Starting_Mass_In" id="SMassInID" value="60" min="0" max="200" oninput="SMassOutID.value = SMassInID.value"><output name="SMassOut" id="SMassOutID"> 60 </output> <br>

Total Daphnia:<input type="range" name="Total_Daphnia_Input_Name" id="TotDInID" value="500" min="0" max="1000" oninput="TotDOutID.value = TotDInID.value"><output name="TotDOut" id="TotDOutID"> 500 </output> <br>

Daphnia Size:<input type="range" name="Daphnia Size" id="DaphSInID" value=".75" min=".5" max="1.5" step=".01" oninput="DaphSOutID.value = DaphSInID.value"><output name="DaphSOut" id="DaphSOutID">.75</output>  <br>

K value:<input type="range" name="K" id="KInID" value=".3" min="0" max="1" step=".01" oninput="KOutID.value = KInID.value"><output name="KOut" id="KOutID">.3</output>  <br/>

Please Select Year: <select name="Year">
<option value="2013" selected>2013</option>
<option value="2014">2014</option>
<option value="2015">2015</option>
</select>
<br>
<br>

Please Select Site: <select name="Site">
<option value="Fall Creek" selected>Fall Creek</option>
<option value="Hills Creek">Hills Creek</option>
<option value="Lookout Point">Lookout Point</option>
</select>
<br>
<br>

Please Select Month: <select name="Month">
<option value="March" selected>March</option>
<option value="April">April</option>
<option value="May">May</option>
<option value="June">June</option>
<option value="July">July</option>
<option value="August">August</option>
</select>
<br>
<br>

Restrict Depth? <input type="radio" name="depr" value="yes" /> Yes
<input type="radio" name="depr" value="no" /> No<br>
Maximum Depth:<input type="range" name="DmaxIn" id="DmaxInID" value="60" min="0" max="200" oninput="DmaxOutID.value = DmaxInID.value"><output name="DmaxOut" id="DmaxOutID"> 60 </output> <br>
Minimum Depth:<input type="range" name="DminIn" id="DminInID" value="60" min="0" max="200" oninput="DminOutID.value = DminInID.value"><output name="DminOut" id="DminOutID"> 60 </output> <br>
<input type="submit" value="Submit"/>
</form>
</body>''')

quit()