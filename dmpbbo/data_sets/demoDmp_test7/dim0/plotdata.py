import numpy                                                                  
import matplotlib.pyplot as plt                                               
directory = '/home/tony/dmpbbo/data_sets/demoDmp_test7/dim0'                                        
inputs   = numpy.loadtxt(directory+'/inputs.txt')                             
targets  = numpy.loadtxt(directory+'/targets.txt')                            
outputs  = numpy.loadtxt(directory+'/outputs.txt')                            
fig = plt.figure()                                                            
plt.plot(inputs,targets,  label='targets',color='black')                  
plt.plot(inputs,outputs, label='predictions')                
plt.xlabel('input'); 
plt.ylabel('output');                                    
plt.legend(loc='lower right')                                                 
plt.show()                                                                    

