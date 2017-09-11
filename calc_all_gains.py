#!/usr/bin/python
# Draws scurves from tests made using test board, where first column is the DAC threshold number and the rest of the columns are values of pe for each pixel
# Draws one graph being an average of all pixels and in separate canvas multigraph of all pixels' graphs

import numpy as np
import ROOT
import sys
from scipy.ndimage.filters import gaussian_filter
sys.path.append("/opt/le_pymodules")
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion

ion()

#from misc_func import wait4key

ag = ROOT.TGraphErrors()

a = np.loadtxt(sys.argv[1])
start_pixel = int(sys.argv[2])
end_pixel = int(sys.argv[3])
#title = sys.argv[4]

g = ROOT.TGraph()
g1 = ROOT.TGraph()
g2 = ROOT.TGraph()
curve = []
dac = []
h = ROOT.TH1I("h", "h", 25, -1, -1)

(r,c) = a.shape
after=[]

DAC_PM=[]
pmt=[]

for j in range(np.shape(a)[0]):
	DAC_PM.append(a[j][0])
	pmt.append(a[j][1:65])


for p in xrange(start_pixel+1,end_pixel+1):
	curve = []
	dac = []
	for line in a:
		curve.append(line[p])
		dac.append(line[0])
	
	der = gaussian_filter(curve, 4, 1)
	der2nd = -gaussian_filter(curve, 4, 2)

	zero_level = 0

	
	#cut out long lists of zero indices then shift to match DAC index
	zero_indices = np.where(np.logical_xor((der2nd[1:]>=zero_level),(der2nd[:-1]>=zero_level)))[0]+1 


	#if len(zero_indices)>=4 and der[zero_indices[np.argsort(-der[zero_indices])[1]]]>10 and der2nd[zero_indices[np.argsort(-der[zero_indices])[1]]]>=0:
	if len(zero_indices)>=4 and der[zero_indices[0]]>50:
		gain = dac[zero_indices[np.argmax(der[zero_indices])]]-dac[zero_indices[0]]
		print '0: '+str(p)
	#elif der2nd[zero_indices[np.argsort(-der[zero_indices])[1]]]<0:
	elif len(zero_indices)>=4:
		gain = dac[zero_indices[np.argmax(der[zero_indices])]]-dac[zero_indices[np.argsort(-der[zero_indices])[1]]]
		print '1: '+str(p)
	else:
		gain = np.nan
		print 'nan: '+str(p)

	after.append(gain)

	plt.figure()
	plt.plot(dac,curve)
	plt.scatter(dac[zero_indices[np.argsort(-der[zero_indices])[1]]],curve[zero_indices[np.argsort(-der[zero_indices])[1]]],s=30,color='red') #plt infl pt
	plt.scatter(dac[zero_indices[0]],curve[zero_indices[0]],s=30,color='green')
	plt.scatter(dac[zero_indices[np.argmax(der[zero_indices])]],curve[zero_indices[np.argmax(der[zero_indices])]],s=30,color='blue')	
	axes=plt.gca()
	axes.set_ylim([0,10000])
			

###
PMTn='PMT1461'
###
"""
plt.hist(before,label='unpotted')
plt.hist(after,label='potted')
plt.xlabel('gain')
plt.ylabel('#')
plt.title(PMTn)
plt.legend()
#plt.savefig('plots/gain_comparison_alt/gain_hist_'+PMTn)

before[before==0] = np.nan
print(np.nanmean((before-after)/before*100))
"""
#h.GetXaxis().SetTitle("Gain [DAC]")
#h.SetTitle("Gain estimation for PMT "+title)
#h.Draw()


#wait4key()
