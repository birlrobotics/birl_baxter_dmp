#!/usr/bin/env python

## \file demoTrainFunctionApproximators.py
## \author Freek Stulp
## \brief  Visualizes results of demoTrainFunctionApproximators.cpp
## 
## \ingroup Demos
## \ingroup FunctionApproximators

import matplotlib.pyplot as plt
import os, sys, subprocess

# Include scripts for plotting
lib_path = os.path.abspath('../plotting')
sys.path.append(lib_path)
from plotData import plotDataFromDirectory
from plotData import getDataDimFromDirectory
from plotLocallyWeightedLines import plotLocallyWeightedLinesFromDirectory
from plotBasisFunctions import plotBasisFunctionsFromDirectory

if __name__=='__main__':
    executable = "/home/tony/build-dmpbbo-Desktop-Default/src/functionapproximators/demos/demoTrainFunctionApproximators"
    
    if (not os.path.isfile(executable)):
        print("")
        print("ERROR: Executable '"+executable+"' does not exist.")
        print("Please call 'make install' in the build directory first.")
        print("")
        sys.exit(-1);
    
    # Call the executable with the directory to which results should be written
    directory = "/home/tony/dmpbbo/data_sets/demoTrainFunctionApproximators"
    subprocess.call([executable, directory])
    
    # Plot the results in each directory
    function_approximator_names = ["WLS","LWR","LWPR","IRFRLS","GMR","RBFN","GPR"]
        
    fig_number = 1;
    for name in function_approximator_names:
        fig = plt.figure(fig_number)

        directory_fa = directory +"/"+ name
        if (getDataDimFromDirectory(directory_fa)==1):
            ax = fig.add_subplot(111)
        else:
            ax = fig.add_subplot(111, projection='3d')

        fig_number += 1;
    
        try:
            if (name=="WLS" or name=="LWR" or name=="LWPR" or name=="GMR"):
                plotLocallyWeightedLinesFromDirectory(directory_fa,ax)
            elif (name=="RBFN" or name=="GPR" or name=="IRFRLS"):
                plotBasisFunctionsFromDirectory(directory_fa,ax)
            plotDataFromDirectory(directory_fa,ax)
            ax.set_ylim(-1.0,1.5)
        except IOError:
            print("WARNING: Could not find data for function approximator "+name)
        ax.set_title(name)
    
    ax.legend(['f(x)','+std','-std','residuals'])
    
    plt.show()
    
    #fig.savefig("lwr.svg")

