##

import numpy as np
from scipy.optimize import curve_fit
from math import pi


##

def fit_sin(xdata, ydata, initial):

    def function(x,A,b,phi,c):
        y = A*np.sin(b*x+phi)+c
        return y
    
    popt, pcov = curve_fit(function, xdata, ydata, initial)
    return popt


##

xdata = [x.timestamp() for x in mix_abscisse]
ydata = mixes[2]
initial = (1, 2*pi/(3600*24*365), 2, 0.4) #(amplitude, angular frequency, phase, shift)

A, b, phi, c = fit_sin(xdata, ydata, initial)

plt.plot(xdata, ydata)
plt.plot(xdata, [function(x,A,b,phi,c) for x in xdata])
plt.show()