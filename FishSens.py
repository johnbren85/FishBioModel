import os
import sys
from Bioenergetics import *

os.chdir('/home/brent/Documents')

# RESERVOIR CONDITIONS
# season_to_month = {'Early Summer':'June',
#                   'Midsummer':'July',
#                   'Late Summer':'August'}

batch = Batch('Fall Creek', 'May', '2015', 0.5, None, None, 5)



# if either depth or temp are None, autocompute from temperature curves
day_depth = 5
day_temp = None
night_depth = 10
night_temp = None

#if SensParam == 'SMass':
#    Sparam = StartingMass
#elif SensParam == 'SLength':
#    Sparam = StartingLength
#elif SensParam == 'TDaph':
#    Sparam = Total_Daphnia
#elif SensParam == 'DaphS':
#    Sparam = DaphSize

daylength = dict([('March',11.83),('April',13.4),('May',14.73),('June',15.42),('July',15.12),('August',13.97),('September',12.45)])
# March 11:50 (11.83), April 13:24 (13.4), May 14:44 (14.73), June 15:25 (15.42), July 15:07 (15.12), August 13:58 (13.97), September 12:27 (12.45)
monthlength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
ndays = monthlength[batch.Month]
day_hours = daylength[batch.Month]
night_hours = 24 - day_hours
day_length = day_hours / 24.0
night_length = night_hours / 24.0
##Foraging equation linked to bioenergetics model is for salmonids only!##
O2Conv = 13560  # J/gram of O2 in respiration conversions (Elliot and Davidson 1975).
DayLight = 10000  # lux http://sustainabilityworkshop.autodesk.com/buildings/measuring-light-levels
NightLight = 0.11  
SwimSpeed = 2 #Body lengths (from grey lit((())))
#SwimSpeed = 0.8 #From Beauchamp paper
# DOUBLE CHECK THIS EQUATION - MUST BE IN GRAMS!
DaphWeightdry = (exp(1.468 + 2.83 * log(batch.DaphSize))) / 1000000  # Based of Cornell equation (g) #WetDaphWeight <- DaphWeight*(8.7/0.322) #From Ghazy, others use ~10%
DaphWeight = DaphWeightdry * 8.7 / 0.322
DaphEnergy = 22700  # From Luecke 22.7 kJ/g
prey = [1]
digestibility = [0.174]  # Noue and Choubert 1985 suggest Daphnia are 82.6% digestible by Rainbow Trout
preyenergy = [DaphEnergy]

## ADD CODE FOR GONAD LOSS HERE IF NEEDED ##

## main script area ##

f = 'ChinookAppendixA.csv'
## if these give problems, just make sure that the categories have quotes around them (and not any tilty ones)
with open(f) as fid:
    reader = DictReader(fid, quoting=QUOTE_NONNUMERIC)
    params = next(reader)

temperature_file = '{0}_smoothed_{1}_{2}.csv'.format(batch.Site, batch.Month, batch.Year)
with open(temperature_file) as fid:
    reader = DictReader(fid)
    temperatures = []
    depths = []
    for row in reader:
        temperatures.append(float(row['temp']))
        depths.append(float(row['depth']))
depth_from_temp = interp1d(temperatures, depths, fill_value=0, bounds_error=False)
temp_from_depth = interp1d(depths, temperatures, fill_value=0, bounds_error=False)

day_temp = day_temp or temp_from_depth(day_depth)
day_depth = day_depth or depth_from_temp(day_temp)
night_temp = night_temp or temp_from_depth(night_depth)
night_depth = night_depth or depth_from_temp(night_temp)

with open('Daphnia VD 2015.csv') as fid:
    reader = DictReader(fid)
    zooplankton_data = [r for r in reader]
(daphline, daph_auc) = batch.compute_daphniabydepth(zooplankton_data)

#L = StartingLength
#W = 0.0003 * StartingLength ** 2.217
StartingLength = (StartingMass/0.0003)**(1/2.217)

    ##NOTE this still underestimates length, as in the equation below... appears fish are longer more than fat...
TotalConsumption = 0
predatorenergy = predatorenergy(params, StartingMass)
output = []
finalLW = []




    # result = minimize_scalar(growth_fn, method='brent', bracket=(min(depths),max(depths)), args=(L,StartingMass,hours,light))
    # if result.success:
    #     return result.x, -result.fun
    # else:
    #     print('Could not optimize growth: %s' % result.message)

out = {'StartingLength':[],'StartingMass':[],'growth':[],'day_depth':[],'night_depth':[]}

# best_depth(L,W,24,DayLight)
# pyplot.show()
# sys.exit(0)

for d in range(ndays):
    (day_depth, day_growth, day_consumption) = best_depth(StartingLength, StartingMass, day_hours, DayLight)
    (night_depth, night_growth, night_consumption) = best_depth(StartingLength, StartingMass, night_hours, NightLight)

    growth = day_growth + night_growth
    dailyconsume = ((day_consumption + night_consumption)*StartingMass)/DaphWeight

    StartingMass += growth
    StartingLength = (StartingMass / 0.0003) ** (1 / 2.217)  # weight to fork length (MacFarlane and Norton 2008)
        #Checked fish lengths against this and by end of summer fish weigh much less than they 'should' based on their length

    out['day_depth'].append(day_depth)
    out['night_depth'].append(night_depth)
    out['growth'].append(growth)
    out['StartingMass'].append(StartingMass)
    out['StartingLength'].append(StartingLength)

print("weight",StartingMass,
      "length",StartingLength,
      "growth",growth,
      "depth(day)",day_depth,
      "depth(night)",night_depth,
      "Daphnia eaten",dailyconsume)

#pyplot.figure()
#pyplot.subplot(121)
#pyplot.plot(out['L'])
#pyplot.ylabel('Length')
#pyplot.subplot(122)
#pyplot.ylabel('Depth')
#pyplot.plot(out['day_depth'],'orange')
#pyplot.plot(out['night_depth'],'black')
#pyplot.show()




##Export results to csv
import csv
s = [('day_depth',[]),('night_depth',[]),('growth',[]),('StartingMass',[]),('StartingLength',[])]
RESULTS = defaultdict(list)
for k, v in s:
    RESULTS[k].append(v)
RESULTS = {'day_depth':[],'night_depth':[],'growth':[],'StartingMass':[],'StartingLength':[]}
for i in range(ndays):
    RESULTS['day_depth'].append(out['day_depth'][i])
    RESULTS['night_depth'].append(out['night_depth'][i])
    RESULTS['growth'].append(out['growth'][i])
    RESULTS['StartingMass'].append(out['StartingMass'][i])
    RESULTS['StartingLength'].append(out['StartingLength'][i])

resultFile = open("output.csv",'wb')
wr = csv.writer(resultFile, dialect='excel')

wr.writerows([
        RESULTS['day_depth'],
        RESULTS['night_depth'],
        RESULTS['growth'],
        RESULTS['StartingMass'],
        RESULTS['StartingLength']
    ])
resultFile.close()