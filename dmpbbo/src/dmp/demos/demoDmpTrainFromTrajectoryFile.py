#!/usr/bin/env python
## \file demoDmpTrainFromTrajectoryFile.py
## \author Freek Stulp
## \brief  A simple wrapper around demoDmpTrainFromTrajectoryFile.cpp, just for consistency
## 
## \ingroup Demos
## \ingroup Dmps

import numpy
import matplotlib.pyplot as plt
import os, sys, subprocess

executable = "/home/tony/build-dmpbbo-Desktop-Default/src/dmp/demos/demoDmpTrainFromTrajectoryFile"

if (not os.path.isfile(executable)):
    print("")
    print("ERROR: Executable '"+executable+"' does not exist.")
    print("Please call 'make install' in the build directory first.")
    print("")
    sys.exit(-1);

# Call the executable with the directory to which results should be written
input_txt_file = "trajectory.txt"
output_xml_file = "/home/tony/dmpbbo/data_sets/dmp.xml"
print([executable, input_txt_file, output_xml_file])
subprocess.call([executable, input_txt_file, output_xml_file])
