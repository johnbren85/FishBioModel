#!C:\Anaconda3\python.exe


import cgi, cgitb
cgitb.enable()



print ('''Content-type:text/html\r\n\r\n
<html>
<head>
<title>This is where we get user input.</title>
</head>
<body>

<h2>Enter Values for Bioenergetics model</h2>

<body background="bgrnd">
<form action="RunModel.py" method="post" target="_blank">

Use Default Values? <input type="radio" name="defa" value="yes" /> Yes
<input type="radio" name="subject" value="physics" /> No<br>

Fish Starting Mass:<input type="range" name="Starting_Mass_In" id="SMassInID" value="60" min="0" max="200" oninput="SMassOutID.value = SMassInID.value"><output name="SMassOut" id="SMassOutID"> 60 </output> <br>

Total Daphnia:<input type="range" name="Total_Daphnia_Input_Name" id="TotDInID" value="500" min="0" max="1000" oninput="TotDOutID.value = TotDInID.value"><output name="TotDOut" id="TotDOutID"> 500 </output> <br>

Daphnia Size:<input type="range" name="Daphnia Size" id="DaphSInID" value=".75" min=".5" max="1.5" step=".01" oninput="DaphSOutID.value = DaphSInID.value"><output name="DaphSOut" id="DaphSOutID">65</output>  <br>

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
print ('</html>')