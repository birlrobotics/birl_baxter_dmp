from mpl_toolkits.mplot3d import Axes3D                                       
import numpy                                                                  
import matplotlib.pyplot as plt                                               
directory = '/home/tony/dmpbbo/data_sets/demoDmpContextualGoal/Step1'                                        
inputs   = numpy.loadtxt(directory+'/inputs.txt')                             
targets  = numpy.loadtxt(directory+'/targets.txt')                            
outputs  = numpy.loadtxt(directory+'/outputs.txt')                            
fig = plt.figure()                                                            
ax = Axes3D(fig)                                                              
ax.plot(inputs[:,0],inputs[:,1],targets, '.', label='targets',color='black')  
ax.plot(inputs[:,0],inputs[:,1],outputs, '.', label='predictions',color='red')
ax.set_xlabel('input_1'); ax.set_ylabel('input_2'); ax.set_zlabel('output')   
ax.legend(loc='lower right')                                                  
plt.show()                                                                    

