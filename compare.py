import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion


def poly3(x, a, b, c, d):
	return a*x**3 - b*x**2 + c*x - d

def compare(PMT,ped,corrfac,k,ASIC):
	"""
	Function to calculate pixel gains for single PMTs before and after potting

	Copes with dead and high gain pixels

	Example input
	########
	#PMT=1461
	#corrfac=1.5
	#ped=820
	#k=1.09
	#ASIC = 'E'
	########
	"""

	#ion()

	#load the unpotted deltaDAC and convert to gain 
	deldac_before = np.loadtxt('unpotted_data/AllGain.dat', delimiter=',')  
	#find the PMT of interest and extract deltaDAC
	l = (np.where(deldac_before==PMT)[0])[0]
	#G = deltaDAC*k/(charge per photon); coorfac accounts for PMTs sorted at 1000V
	gains_before = ((deldac_before[l][2:65])*corrfac*k)/160.

	#load the potted inflection points 
	inflpt_after = np.loadtxt('potted_output/'+str(PMT)+'_potted_gain.dat')
	#subtract from pedestal and convert to gain
	ped_array_after = np.tile(ped,64)
	deldac_after = (ped_array_after-inflpt_after)
	ASICresponse = np.genfromtxt('ASICresponse.dat',dtype = None)
	m = ord(ASIC) - 65
	poly = np.array([ASICresponse[m][1],ASICresponse[m][2],ASICresponse[m][3],ASICresponse[m][4]])
	gains_after_raw = poly3(deldac_after,poly[0],poly[1],poly[2],poly[3]) 


	#Deal with dead and overly high gain pixels
	m=max(gains_after_raw)
	if m > (ped-100):
		index = [i for i, j in enumerate(gains_after_raw) if j==m]
		gains_after_raw[index] = np.nan
	else: 
		gains_after_raw=gains_after_raw
	
	gains_before[gains_before==0] = np.nan
	gains_after_raw[gains_after_raw==0] = np.nan

	gains_after=gains_after_raw/160.

	#NB: Only 63 channels for unpotted PMTs as always one dead channel in sorting
	gains_before = np.append(gains_before,[np.nan]) 

	#Calculate average percentage difference (+ve <=> decrease in gain)
	perc_diff = (gains_before-gains_after)/gains_before*100

	return gains_before, gains_after, perc_diff

def pltPMT(file):
	"""
	Function to plot the S-curve of a single PMT
	""" 
	file_PM = np.loadtxt(file)

	DAC_PM=[]
	pmt=[]
	#pmtp=[] #use to highlight a single pixel

	for j in range(np.shape(file_PM)[0]):
		DAC_PM.append(file_PM[j][0])
		pmt.append(file_PM[j][1:65])
		#pmtp.append(file_PM[j][n])

	#ylim=10000

	"""
	plt.figure()
	plt.plot(np.array(DAC_PM),np.array(pmt))
	plt.title('PMT'+str(PMT))
	plt.xlabel('DAC')
	#plt.ylabel()
	axes=plt.gca()
	axes.set_ylim([0,ylim])
	"""

	return DAC_PM, pmt




	
