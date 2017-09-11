#convert EC files into single PMT style files 

import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion

ion()

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