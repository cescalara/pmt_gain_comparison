# Comparison of PMTs before and after potting

import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
 

ion()

n=20
# Get EC (potted) data
file_EC = np.loadtxt(sys.argv[1])
DAC_EC=[]
pmt1=[]
pmt2=[]
pmt5p=[]
pmt3=[]
pmt4=[]
pmt5=[]
pmt6=[]

for i in range(np.shape(file_EC)[0]):
	DAC_EC.append(file_EC[i][0])
	pmt1.append(file_EC[i][1:65])
	pmt2.append(file_EC[i][65:129])
	pmt3.append(file_EC[i][129:193])
	pmt4.append(file_EC[i][193:257])
	pmt5.append(file_EC[i][257:321])
	pmt5p.append(file_EC[i][n+256])
	pmt6.append(file_EC[i][321:385])

"""
#Get unpotted data
file_PM = np.loadtxt(sys.argv[2])
DAC_PM=[]
pmt=[]
pmtp=[]

for j in range(np.shape(file_PM)[0]):
	DAC_PM.append(file_PM[j][0])
	pmt.append(file_PM[j][1:65])
	pmtp.append(file_PM[j][n])
"""


#plot the Scurve

###############
"""
PMTn='PMT1461'
ECn='EC2'
"""
ylim_pot=250000
pmtplot=pmt6
###############

plt.figure()
plt.plot(np.array(DAC_EC),np.array(pmtplot),label='Potted')
axes=plt.gca()
axes.set_ylim([0,ylim_pot])
#plt.title('Potted '+PMTn+' '+ECn)
#plt.savefig('plots/'+ECn+'/pot_'+'all'+PMTn+'update')
#plt.figure()
#plt.plot(np.array(DAC_PM),np.array(pmt), label='Unpotted')
#axes=plt.gca()
#axes.set_ylim([0,10000])
#plt.title('Unpotted '+PMTn)
#plt.savefig('plots/'+ECn+'/unpot_'+'all'+PMTn)

