import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import sys
from scipy.signal import medfilt
import statistics
import csv
from matplotlib.pyplot import ion

ion()
print "calcul inflexion point: 	first argument file name; second argument: first boundary of fit;	third argument: end of fit ; fourth argument: step; 4th argument: pedestal"

#################################

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
        """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
   3     The Savitzky-Golay filter removes high frequency noise from data.
   4     It has the advantage of preserving the original shape and
   5     features of the signal better than other types of filtering
   6     approaches, such as moving averages techniques.
   7     Parameters
   8     ----------
   9     y : array_like, shape (N,)
  10         the values of the time history of the signal.
  11     window_size : int
  12         the length of the window. Must be an odd integer number.
  13     order : int
  14         the order of the polynomial used in the filtering.
  15         Must be less then `window_size` - 1.
  16     deriv: int
  17         the order of the derivative to compute (default = 0 means only smoothing)
  18     Returns
  19     -------
  20     ys : ndarray, shape (N)
  21         the smoothed signal (or it's n-th derivative).
  22     Notes
  3     -----
       The Savitzky-Golay is a type of low-pass filter, particularly
       suited for smoothing noisy data. The main idea behind this
      approach is to make for each point a least-square fit with a
       polynomial of high order over a odd-sized window centered at
       the point.
       Examples
       --------
       t = np.linspace(-4, 4, 500)
       y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
       ysg = savitzky_golay(y, window_size=31, order=4)
       import matplotlib.pyplot as plt
       plt.plot(t, y, label='Noisy signal')
       plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
       plt.plot(t, ysg, 'r', label='Filtered signal')
       plt.legend()
       plt.show()
       References
       ----------
       .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
          Data by Simplified Least Squares Procedures. Analytical
          Chemistry, 1964, 36 (8), pp 1627-1639.
       .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
          W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
          Cambridge University Press ISBN-13: 9780521880688
       """
	import numpy as np
	from math import factorial
       
	try:
		window_size = np.abs(np.int(window_size))
		order = np.abs(np.int(order))
	except ValueError, msg:
		raise ValueError("window_size and order have to be of type int")
	if window_size % 2 != 1 or window_size < 1:
		raise TypeError("window_size size must be a positive odd number")
	if window_size < order + 2:
           	raise TypeError("window_size is too small for the polynomials order")
	order_range = range(order+1)
        half_window = (window_size -1) // 2
        # precompute coefficients
        b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
       # pad the signal at the extremes with
       # values taken from the signal itself
        firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
        lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
        y = np.concatenate((firstvals, y, lastvals))
        return np.convolve( m[::-1], y, mode='valid')

#############



def func(x, a, b, c, d, e, f, g):
	return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g
def funcprime(x, a, b, c, d, e, f):
	return 6*a*x**5 + 5*b*x**4 + 4*c*x**3 + 3*d*x**2 + 2*e*x + f

def funcsecond(x, a, b, c, d, e):
	return 30*a*x**4 + 20*b*x**3 + 12*c*x**2 + 6*d*x + 2*e

file = np.loadtxt(sys.argv[1])

fileOutput=open(sys.argv[5], 'w')
writer=csv.writer(fileOutput, delimiter="\t")
zerocross=np.zeros(64)

bound=float(sys.argv[3])
step=float(sys.argv[4])
#ped=float(sys.argv[5])
start=float(sys.argv[2])

AllDAC=np.zeros(64)

FullDac=file[:,0]
DAC2=file[start/step:bound/step,0]

index=0
ChannelInfl=np.zeros(64)

channelSum=np.zeros((bound-start)/step)
#channelSum=np.zeros(len(FullDac))
infl2=0
inflMoy=0

nbInfl=0
infl=0
answerTrue="True"
answerAlt=0

nbCourbes=0 #nbCourbes de bonne qualite 

#for j in range (0,int(bound/step)):
#	for i in range (1, 65):
#		channel=0
#		channelSum[j]=channelSum[j]+file[j,i]
	
#	para, pcov=curve_fit(func, DAC, channel)

	#plt.plot(DAC, channel)
#	fig, ax1=plt.subplots()

	
	#ax1.plot(DAC, channel)	
	
	#plt.subplots(2,1)
	#ax2=ax1.twinx()
	
#	channelSum[j]=channelSum[j]/64.

for i in range (1,63):
	channelSimple=0

	#channel=file[:,i]
	channelSimple=file[start/step:bound/step,i]

	plt.plot(DAC2, channelSimple)
	plt.ylim((0, 15000))
plt.show()

start2=float(raw_input("start of the fit: \n"))
bound2=float(raw_input("end of the fit: \n"))

DAC=file[start2/step:bound2/step,0]


for i in range (1, 65):
	ysg=0
	channel=file[start2/step:bound2/step,i]
	channelFull=file[:,i]
	ysg=medfilt(channel, 3)
	ysgFull=savitzky_golay(channelFull, window_size=31, order=4)
	para2, pcov2=curve_fit(func,DAC, channel) #fit de chaque channel
	para3, pcov3=curve_fit(func,DAC, ysg)
	for j in range (0,int(bound2/step)-int(start2/step)):
		if ysgFull[50]>1:
			channelSum[j]=channelSum[j]+channel[j]
	
	for j in range (1, len(DAC)-1):
		if funcprime(DAC, para2[0],  para2[1], para2[2], para2[3], para2[4], para2[5])[j-1]==max(funcprime(DAC, para2[0],  para2[1], para2[2], para2[3], para2[4], para2[5])):
			infl2=DAC[j-1]
			break
	if ysg[20-int(start2/step)]>1:
		AllDAC[i-1]=infl2	
		nbCourbes+=1
	
		plt.subplot(8,8,i)
	
		l=plt.axvline(x=AllDAC[i-1])
		plt.text(200, 10, AllDAC[i-1])
		plt.text(200, 5, i)
		plt.plot(DAC, channel/200.)

		plt.plot(DAC, funcprime(DAC, para2[0],  para2[1], para2[2], para2[3], para2[4], para2[5]))
		plt.plot(DAC, funcprime(DAC, para3[0],  para3[1], para3[2], para3[3], para3[4], para3[5]))



#para, pcov=curve_fit(func, DAC, channelSum)

#for i in range (1, len(DAC2)-1):
	#if (funcsecond(DAC2, para[0],  para[1], para[2], para[3], para[4])[i-1]>0 and funcsecond(DAC2, para[0],  para[1], para[2], para[3], para[4])[i+1]<0 ):
			#infl += DAC2[i]
			
			##print "infl: ", DAC2[i]
			#nbInfl+=1

plt.show()

print "infl Moy: ", sum(AllDAC)/nbCourbes

index=raw_input("channel a changer; sinon, taper '-1': ")

while index!="-1":
	TrueInf=raw_input("Inflexion point DAC: ")
	AllDAC[int(index)-1]=int(TrueInf)	
	index=raw_input("channel a changer; sinon, taper '-1': ")

writer.writerow(AllDAC)

fileOutput.close()
for i in range (0, 64):
	
	inflMoy+=AllDAC[i]


print "\n nombre courbe: ", nbCourbes
#print "infl courbe moyenne: ", infl/nbInfl
print "infl moyen", inflMoy/nbCourbes
print "pstdev: ", statistics.pstdev(AllDAC)
#print "diff with pedestal: ", ped-inflMoy/nbCourbes

