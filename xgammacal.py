#!/usr/bin/env pypenv
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

"""
Thu Apr  5 18:23:14 2001 mazer

- Color and luminance calibration program for X-RITE DTP94
  on-screen colorimeter. Dumps to stdout..

Wed Jun 15 15:00:12 2005 mazer

- calib3.py -> dtp94_cal.py (for new usb-based X-RITE DTP94)

Tue Apr 18 09:23:52 2006 mazer

- Cleaned up and renamed to calibrate.py. Now this takes the
  config info directly out of the ~/.pyperc/Config.$HOST file.

Fri Dec 14 10:30:01 2007 mazer

- massive cleanup to get things working with all the different
  systems in the lab -- mostly this involves fixing up the
  makefile and dtp94.c

- however, the calibration run now requires that you specify a
  pyperc Config.host file on the command line in order to ensure
  you're correctly calibrating the monitor using the same settings
  you'll use during recording/testing...

- errors in dtp94 are also better detected and lead to an abort
  with a slightly more informative error message on console..

"""

import os, string
from sys import *
from pype import *
from config import *
from pype_aux import *
from sprite import *

DTP='/auto/share/pypeextra/dtp94'

def query_XYZ():
    s = os.popen(DTP+' 0201RM', 'r').read()
    s = string.strip(string.split(s, '\r')[0])
    return map(float,string.split(s)[1::2])
    
def query_Yxy():
    s = os.popen(DTP+' 0301RM', 'r').read()
    s = string.strip(string.split(s, '\r')[0])
    return map(float,string.split(s)[1::2])


if len(sys.argv) < 4:
    sys.stderr.write('usage: %s configfile lcd|crt outfile [gamma]\n' % \
                     sys.argv[0])
    sys.stderr.write('  - configfile is something like ~/.pyperc/Config.foo\n')
    sys.stderr.write('  - lcd or crt specifies what to calibrate\n')
    sys.stderr.write('  - output file\n')
    sys.stderr.write('  - [optional] gamma is for validating an old\n')
    sys.stderr.write('    by rerunning the calibration at specified gamma\n')
    sys.exit(1)

configfile = Config(sys.argv[1])
bugmode = sys.argv[2]
outfile = sys.argv[3]
if len(sys.argv) == 5:
    gammatest = float(sys.argv[4])
    sys.stdout.write('validation mode: gamma=%f\n' % gammatest);
else:
    gammatest = None

w = configfile.iget('DPYW')
h = configfile.iget('DPYH')
bits = 32
dpy = configfile.get('SDLDPY')
flags = DOUBLEBUF | FULLSCREEN

sys.stdout.write('specs: %dx%d %dbits dpy=%s\n' % (w, h, bits, dpy,))

if (flags & FULLSCREEN) and os.geteuid != 0:
    sys.stdout.write('WARNING: no full screen mode w/o root access!\n')
    
s = os.popen(DTP+' 010aCF', 'r').read()
if s == 'DTP94-ERROR\n':
    sys.stdout.write('Problem reading calibration bug, is it attached?\n')
    sys.exit(1)

if bugmode == 'lcd':
    s = os.popen(DTP+' 0216CF', 'r').read()
elif bugmode == 'crt':
    s = os.popen(DTP+' 0116CF', 'r').read()
else:
    sys.stdout.write("mode must be 'lcd' or 'crt'\n");
    sys.exit(1)
    
s = os.popen(DTP+' CE', 'r').read()
s = os.popen(DTP+' CE', 'r').read()
s = os.popen(DTP+' CE', 'r').read()

sys.stdout.write("Calibrate offsets 1st? [yN] ")
sys.stdout.flush()
x=sys.stdin.readline()
if x[0] == 'y' or x[0] == 'Y':
    sys.stdout.write('Place calibration bug on an opaque surface:\n')
    sys.stdout.write('and then hit return >>')
    sys.stdout.flush()
    sys.stdin.readline()
    sys.stdout.write('please wait -- this will take ~10 secs...\n');
    s = os.popen(DTP+' CO', 'r').read()
    sys.stdout.write('Done!\n');

sys.stdout.write('Attach calibration bug to monitor (under framebuffer)\n')
sys.stdout.write('and hit return >>')
sys.stdout.flush()
sys.stdin.readline()

fb = FrameBuffer(dpy, w, h, bits, flags, sync=0)

if gammatest:
    fb.set_gamma(gammatest, gammatest, gammatest)

sys.stdout.write('.....calibration is running....\n')

out = open(outfile, 'w')

out.write("%% bugmode=%s\n" % bugmode)
out.write("%% gammatest=%s\n" % gammatest)
out.write("%% columns: |r|g|b|Y|x|y|\n")

R = range(0,255,10)
if R[-1] != 255:
    R.append(255)

for l in R:
    for (rw,gw,bw) in ((1,0,0), (0,1,0), (0,0,1), (1,1,1)):
        r, g, b = rw*l, gw*l, bw*l
        fb.clear(color=(r, g, b))
        fb.flip()
        (Y, x, y) = query_Yxy()
        out.write('%f %f %f %f %f %f\n' % (r, g, b, Y, x, y,))
        sys.stdout.write("%s -> %s\n" % ((r,g,b), (Y,x,y)))
        out.flush()
