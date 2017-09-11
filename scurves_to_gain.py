# Run the comparison of unpotted and potted PMTs

from gain_analysis import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
import numpy as np 
import fnmatch
import os

ion()

#Define the setup parameters
config=np.genfromtxt('config.txt', dtype= None)
pd=[]
y_lim=10000

for i in range(np.shape(config)[0]):
	PMT=config[i][0]
	corrfac=config[i][1]
	k=config[i][2]
	ASIC=config[i][3]


	#Find potted and unpotted data files for PMTs of interest and loop
	for file in os.listdir('unpotted_data'):
		if fnmatch.fnmatch(file,'*'+str(PMT)+'*'):
			unpot='unpotted_data/'+file

			#alternatively could take user input, or get labview to tag EC unit or smth
			#at the moment requires use of conv() function to produce files tagged with PMT #
			pot='potted_data/PMT/PMT'+str(PMT)+'_potted.txt'

			#Get S-curve data for plotting
			DAC_PM_unpot, pmt_unpot = pltPMT(unpot)
			DAC_PM_pot, pmt_pot = pltPMT(pot)

			#Get gains
			gains_before = deldac_to_gain(calc_deldac(unpot),PMT,True,ASIC,corrfac,k)
			gains_after = deldac_to_gain(calc_deldac(pot),PMT,False,ASIC,corrfac,k)
			

			#Find average percentage difference between pixel gains (+ve <=> decrease)
			perc_diff = (gains_before-gains_after)/gains_before*100
			pd.append(perc_diff)

			f, axarr = plt.subplots(2,2,figsize=(16,12),facecolor='w',edgecolor='k')
			plt.suptitle('PMT '+str(PMT),size=20)
			axarr[0, 0].plot(DAC_PM_unpot,pmt_unpot)
			axarr[0, 0].set_title('Unpotted S-curve')
			axarr[0, 0].set_ylim([0,y_lim])
			axarr[0, 0].set_xlabel('DAC')
			axarr[0, 1].plot(DAC_PM_pot,pmt_pot)
			axarr[0, 1].set_title('Potted S-curve')
			axarr[0, 1].set_ylim([0,y_lim])
			axarr[0, 1].set_xlabel('DAC')
			axarr[1, 0].hist(gains_before[~np.isnan(gains_before)],label='Unpotted')
			axarr[1, 0].hist(gains_after[~np.isnan(gains_after)],label='Potted')
			axarr[1, 0].legend()
			axarr[1, 0].set_title('Gain comparison')
			axarr[1, 0].set_xlabel('Gain')
			axarr[1, 0].set_ylabel('#')
			axarr[1, 1].scatter(range(64),gains_before,s=20,label='Unpotted')
			axarr[1, 1].scatter(range(64),gains_after,s=20,c='g',label='Potted')
			axarr[1, 1].legend()
			axarr[1, 1].set_title('Gain comparison pixel by pixel')
			axarr[1, 1].set_xlabel('pixel #')
			axarr[1, 1].set_ylabel('Gain')

			plt.show()
			#plt.savefig('plots/gain_comparison_lech/gain_comp_PMT'+str(PMT)+'.png')

			print('Completed PMT '+str(PMT))



print('Average percentage decrease: '+str(np.nanmean(pd)))
print('Percentage of nan values: '+str(np.sum(np.isnan(pd))/(64.*np.shape(config)[0])*100))	