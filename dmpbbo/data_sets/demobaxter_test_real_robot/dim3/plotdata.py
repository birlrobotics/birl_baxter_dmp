import numpy                                                                  
import matplotlib.pyplot as plt                                               
directory = '/home/tony/dmpbbo/data_sets/demobaxter_test_real_robot/dim3'                                        
inputs   = numpy.loadtxt(directory+'/inputs.txt')                             
targets  = numpy.loadtxt(directory+'/targets.txt')                            
outputs  = numpy.loadtxt(directory+'/outputs.txt')                            
fig = plt.figure()                                                            
plt.plot(inputs,targets, '.', label='targets',color='black')                  
plt.plot(inputs,outputs, '.', label='predictions',color='red')                
plt.xlabel('input'); plt.ylabel('output');                                    
plt.legend(loc='lower right')                                                 
plt.show()                                                                    

