import numpy as np
import matplotlib.pyplot as plt
import sys, os
def plotRollout(cost_vars,ax):
    viapoint = [1.500000, 2.000000]
    viapoint_time = 0.200000
    # y      yd     ydd    1  forcing
    # n_dofs n_dofs n_dofs ts n_dofs
    n_dofs = len(viapoint)
    y = cost_vars[:,0:n_dofs]
    t = cost_vars[:,3*n_dofs]
    line_handles = ax.plot(y[:,0],y[:,1],linewidth=0.5)
    ax.plot(viapoint[0],viapoint[1],'ok')
    return line_handles

if __name__=='__main__':
    # See if input directory was passed
    if (len(sys.argv)==2):
      directory = str(sys.argv[1])
    else:
      print 'Usage: '+sys.argv[0]+' <directory>';
      sys.exit()
    cost_vars = np.loadtxt(directory+"/cost_vars.txt")
    fig = plt.figure()
    ax = fig.gca()
    plotRollout(cost_vars,ax)
    plt.show()
