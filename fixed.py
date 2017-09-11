# Comparison of PMTs before and after fixing in Japan

import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion

ion()

#load the gain files
before = np.loadtxt(sys.argv[1])
after = np.loadtxt(sys.argv[2])

plt.hist(before,bins=10,label='before')
plt.hist(after,bins=10,label='after')
plt.title('PMT 1767')
plt.xlabel('gain')
plt.ylabel('#')
plt.legend()
