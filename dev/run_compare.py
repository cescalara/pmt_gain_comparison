# Run the comparison of unpotted and potted PMTs

from compare import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
import numpy as np 
import fnmatch
import os

ion()
setup=np.genfromtxt('setup.dat', dtype= None)
pd=[]

for i in range(np.shape(setup)[0]):
	
	PMT=setup[i][0]
	ped=setup[i][1]
	corrfac=setup[i][2]
	k=setup[i][3]
	ASIC=setup[i][4]
	y_lim=10000

	#calculate gains
	gains_before, gains_after, perc_diff = compare(PMT,ped,corrfac,k,ASIC)
	pd.append(perc_diff)


	#plot and save histograms + S-curves
	for file in os.listdir('unpotted_data'):
		if fnmatch.fnmatch(file,'*'+str(PMT)+'*'):
			unpot='unpotted_data/'+file

			pot='potted_data/PMT/PMT'+str(PMT)+'_potted.txt'

			DAC_PM_unpot, pmt_unpot = pltPMT(unpot)
			DAC_PM_pot, pmt_pot = pltPMT(pot)

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
			plt.savefig('plots/gain_comparison_final/gain_comp_PMT'+str(PMT)+'.png')

			print('Completed PMT '+str(PMT))





	
