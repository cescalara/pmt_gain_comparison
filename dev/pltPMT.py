# PLot S curve

import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion

ion()
file_PM = np.loadtxt(sys.argv[1])

DAC_PM=[]
pmt=[]
#pmtp=[]

for j in range(np.shape(file_PM)[0]):
	DAC_PM.append(file_PM[j][0])
	pmt.append(file_PM[j][1:65])
#	pmtp.append(file_PM[j][n])

ylim=200000

plt.figure()
plt.plot(np.array(DAC_PM),np.array(pmt))
axes=plt.gca()
axes.set_ylim([0,ylim])
