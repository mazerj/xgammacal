# Gamma correction for Optix DTP92

## Intro

Gamma correction is done by a pypenv program `xgammacal.py` that
uses a c-based binary `dtp92` to communication with the Optix
DTP92. This all run by a shell script called `xgammacal`

To install, you need to install the required packages (libusb-dev)
and compile a version of dtp92 by doing:

> % make deps
> % make install

This will require sudo access to install and setup dtp92 as suid-root,
so any user can access the dtp92. This also means you should not run
these tools as root. It's not necessary and root won't find pypenv
without some playing around.

## Actual calibration procedure


1. Plug DTP92 into USB port on the rig machine to calibrate
2. Run the `xgammacal` program. It should be on everyone's
   path, if not add `/auto/share/pypeextra` to your path:

    % gammacal ConfigFile lcd outfilename

where ConfigFile is the pypeconfig file (Config.$(HOSTNAME)).

3. Then you can plot the results by firing up matlab and doing

    >> showcalib('outfilename');

4. You can then optionally validate the calibration:

    % gammacal ConfigFile lcd outfilename gamma

where gamma is the overall gamma value plotted by showcalib().
