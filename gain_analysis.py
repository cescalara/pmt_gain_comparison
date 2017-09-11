import numpy as np
from scipy.ndimage.filters import gaussian_filter


def poly3(x, a, b, c, d):
	return a*x**3 - b*x**2 + c*x - d


def calc_deldac(file, ASIC='A'):
	"""
	Function to find pedestal and inflection point on S-curve and then calculate the difference
	"""
	#Load the scurve file, determine if PMT is in EC or not, and if so, select ASIC 
	file_PM = np.loadtxt(file)
	ASIC_sel = {0: [1,65], 1: [65,129], 2: [129,193], 3: [193,157], 4: [257,321], 5: [321,385]}
	
	n = ord(ASIC) - 65
	dac_all = []
	scurve_all = []
	deldac_all =[]

	#Find the delta DAC (ped-inlfpt)
	for p in range(ASIC_sel[n][0], ASIC_sel[n][1]):
		scurve = []
		dac = []
		for line in file_PM:
			scurve.append(line[p])
			scurve_all.append(line[p])
			dac.append(line[0])
			dac_all.append(line[0])

		scurve=np.array(scurve)
		der = gaussian_filter(scurve, 4, 1)
		der2nd = -gaussian_filter(scurve, 4, 2)
		zero_level = 0

		zero_indices = np.where(np.logical_xor((der2nd[1:]>=zero_level),(der2nd[:-1]>=zero_level)))[0]+1
			
		if len(zero_indices)>=4:
			if der[zero_indices[0]]>=50:
				deldac = dac[zero_indices[np.argmax(der[zero_indices])]]-dac[zero_indices[0]]
			elif der[zero_indices[0]]<50 and scurve[zero_indices[np.argsort(-der[zero_indices])[1]]]>=100:
				deldac = dac[zero_indices[np.argmax(der[zero_indices])]]-dac[zero_indices[np.argsort(-der[zero_indices])[1]]]	
			else:
				der = gaussian_filter(scurve, 2.5, 1)
				der2nd = -gaussian_filter(scurve, 2.5, 2)	
				zero_indices = np.where(np.logical_xor((der2nd[1:]>=zero_level),(der2nd[:-1]>=zero_level)))[0]+1
				deldac = dac[zero_indices[np.argmax(der[zero_indices])]]-dac[zero_indices[np.argsort(-der[zero_indices])[1]]]
		else:
			deldac = np.nan
			
		if deldac > 0:
			deldac_all.append(deldac)
		else:
			deldac_all.append(np.nan)
			
	return deldac_all


def deldac_to_gain(deldac_all,PMT,single=True,ASIC='A',corrfac=1,k=1):
	"""
	Function to calculate the gain from the delta DAC. Uses ASIC response file as an input. 

	Single PMTs are converted via a simple multiplying factor k
	PMTs in ECs are converted via a 3rd degree polynomial 

	Divide by 160 fC = charge of photoelectron with gain of 10e6
	"""
	config = np.genfromtxt('config.txt', dtype= None)

	#For single PMTs
	if single == True:
		gains_all = np.array(deldac_all)*corrfac*k/160.
	else:
		ASICresponse = np.genfromtxt('ASICresponse.dat',dtype = None)
		o = ord(ASIC) - 65
		poly = np.array([ASICresponse[o][1],ASICresponse[o][2],ASICresponse[o][3],ASICresponse[o][4]])
		gains_all = np.array(poly3(np.array(deldac_all),poly[0],poly[1],poly[2],poly[3]))/160. 

	return gains_all

def conv(file_EC,PMT,ASIC):
	"""
	Converts EC files output by labview into single PMT files labelled with PMT #
	"""
	
	file_EC = np.loadtxt(sys.argv[1])
	ASIC_sel = {0: [1,65], 1: [65,129], 2: [129,193], 3: [193,157], 4: [257,321], 5: [321,385]}
	n = ord(ASIC)-65

	pmt=[]
	for i in range(np.shape(file_EC)[0]): 
		pmt.append([file_EC[i][0].tolist()]+file_EC[i][ASIC_sel[n][0]:ASIC_sel[n][1]].tolist())

	PMTn='PMT'+PMT

	np.savetxt('potted_data/PMT/'+PMTn+'_potted.txt',pmtsave,fmt='%i',delimiter='\t')
	return 0

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

	

	return DAC_PM, pmt




	
