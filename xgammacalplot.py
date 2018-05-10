#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def estimateGamma(calfile):
	data = np.loadtxt(calfile, comments='%')

	c = 'rgbk'
	g = []
	p0 = None
	lines = []
	plt.subplot(1,2,1)
		
	for n in range(4):
		if n == 3:
			col = 0
		else:
			col = n
		x = data[n::4,col]			# r,g,b,r
		y = data[n::4,3]			# Y,Y,Y,Y
		params, covar = curve_fit(lambda x,alpha,beta,gamma:\
								alpha*(x**gamma)+beta, x, y, p0=p0)
		p0 = params
		g.append(round(params[2], 3))
		xx = np.linspace(min(x),max(x), 100)
		yy = params[0]*(xx**params[2])+params[1]
		l = plt.plot(x, y, c[n]+'o', xx, yy, c[n]+'-')
		lines.append(l[1])
		plt.hold(1)
			
	plt.hold(0)
	plt.xlabel('computer output [0-255]')
	plt.ylabel('luminance [cd/m^2]')
	plt.legend(lines, map(lambda x:'%s'%x, g), loc=0)
	plt.title(calfile)

	# plot color gamut
	plt.subplot(1,2,2)
	x = data[:,4]
	y = data[:,5]
	plt.plot(x, y, 'k.');
	plt.hold(1)
	a = np.nonzero(x == np.max(x))[0]
	b = np.nonzero(y == np.max(y))[0]
	plt.plot([x[a[0]], x[b[0]]], [y[a[0]], y[b[0]]], 'k-')
	a = np.nonzero(x == np.max(x))[0]
	b = np.nonzero(y == np.min(y))[0]
	plt.plot([x[a[0]], x[b[0]]], [y[a[0]], y[b[0]]], 'k-')
	a = np.nonzero(y == np.max(y))[0]
	b = np.nonzero(y == np.min(y))[0]
	plt.plot([x[a[0]], x[b[0]]], [y[a[0]], y[b[0]]], 'k-')
	plt.axis('equal')
	plt.xlabel('CIE x')
	plt.ylabel('CIE y')		   
	plt.title('gamut')
		
	plt.show()
	g = [g[3], g[0], g[1], g[2],]
	return g

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.stderr.write('usage: %s calibrationfile\n' % sys.argv[0])
		sys.exit(1)
	print 'L,R,G,B gamma: ', estimateGamma(sys.argv[1])
