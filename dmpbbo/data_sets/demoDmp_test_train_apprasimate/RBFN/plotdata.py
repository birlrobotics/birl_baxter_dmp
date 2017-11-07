import numpy                                                                  
import matplotlib.pyplot as plt                                               
directory = '/home/tony/dmpbbo/data_sets/demoDmp_test_train_apprasimate/RBFN'                                        
inputs   = numpy.loadtxt(directory+'/inputs.txt')                             
targets  = numpy.loadtxt(directory+'/targets.txt')                            
outputs  = numpy.loadtxt(directory+'/outputs.txt')                            
fig = plt.figure()                                                            
plt.plot(inputs,targets, '.', label='targets',color='black')                  
plt.plot(inputs,outputs, '.', label='predictions',color='red')                
plt.xlabel('input'); plt.ylabel('output');                                    
plt.legend(loc='lower right')                                                 
plt.show()                                                                    
