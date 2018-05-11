# Gamma correction for Optix DTP94

## Intro

Gamma correction is done by a pypenv program `xgammacal.py` that
uses a c-based binary `dtp94` to communication with the Optix
DTP94. This all run by a shell script called `xgammacal`

To install, you need to install the required packages (libusb-dev)
and compile a version of dtp94 by doing:

> % make deps
> % make install

This will require sudo access to install and setup dtp94 as suid-root,
so any user can access the dtp94. This also means you should not run
these tools as root. It's not necessary and root won't find pypenv
without some playing around.

## Actual calibration procedure


1. Plug DTP92 into USB port on the rig machine to calibrate
2. Run the `xgammacal` program. It should be on everyone's
   path, if not add `/auto/share/pypeextra` to your path:

    % xgammacal ConfigFile lcd outfilename

   where ConfigFile is the pypeconfig file (Config.$(HOSTNAME)).

3b. Then you can then plot the results from the command line:

    % xgammacalplot outfilename

3b. Then you can also the results by firing up matlab and doing

    >> showcalib('outfilename');

4. You can then optionally validate the calibration:

    % xgammacal ConfigFile lcd outfilename gamma

   where gamma is the overall gamma value you got from the
   plot program
