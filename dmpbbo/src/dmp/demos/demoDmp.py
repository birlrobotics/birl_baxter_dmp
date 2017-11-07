#!/usr/bin/env python
## \file demoDmp.py
## \author Freek Stulp
## \brief  Visualizes results of demoDmp.cpp
## 
## \ingroup Demos
## \ingroup Dmps

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys, subprocess

lib_path = os.path.abspath('../plotting')
sys.path.append(lib_path)

from plotTrajectory import plotTrajectoryFromFile
from plotDmp import plotDmp

executable = "/home/tony/build-dmpbbo-Desktop-Default/src/dmp/demos/demoDmp"

if (not os.path.isfile(executable)):
    print("")
    print("ERROR: Executable '"+executable+"' does not exist.")
    print("Please call 'make install' in the build directory first.")
    print("")
    sys.exit(-1);

# Call the executable with the directory to which results should be written
directory = "/home/tony/dmpbbo/data_sets/demoDmp_test3"
subprocess.call([executable, directory])

print("Plotting")

fig = plt.figure(1)
axs = [ fig.add_subplot(131), fig.add_subplot(132), fig.add_subplot(133) ] 

lines = plotTrajectoryFromFile(directory+"/demonstration_traj.txt",axs)
plt.setp(lines, linestyle='-',  linewidth=4, color=(0.8,0.8,0.8), label='demonstration')

lines = plotTrajectoryFromFile(directory+"/reproduced_traj.txt",axs)
plt.setp(lines, linestyle='--', linewidth=2, color=(0.0,0.0,0.5), label='reproduced')

plt.legend()

# Read data
xs_xds        = numpy.loadtxt(directory+'/reproduced_xs_xds.txt')
forcing_terms = numpy.loadtxt(directory+'/reproduced_forcing_terms.txt')
fa_output     = numpy.loadtxt(directory+'/reproduced_fa_output.txt')

fig = plt.figure(2)
plotDmp(xs_xds,fig,forcing_terms,fa_output)


plt.show()
