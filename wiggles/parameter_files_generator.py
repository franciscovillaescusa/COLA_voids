# Use this script to create the initial condition parameter file when multiple
# realizations of the same cosmology are needed
import numpy as np
import sys,os

############################### INPUT ###################################
realizations  = 100
fiducial_seed = 45001

# name of fiducial file
fiducial_file = 'COLA.params'
#########################################################################

# do a loop over all realizations
for i in xrange(realizations):

    seed = i  #value of the random seed

    # create the folders if they do not exist
    folder = '%d'%i
    if not(os.path.exists(folder)):   os.system('mkdir %s'%folder)

    # open input and output files
    output_file = '%d/%s'%(i, fiducial_file)
    if os.path.exists(output_file):  continue
    fin  = open('%s'%fiducial_file, 'r')
    fout = open(output_file, 'w')

    # generate new parameter file
    for line in fin:
        if str(fiducial_seed) in line.split():
            fout.write(line.replace(str(fiducial_seed), str(seed)))
        else:  fout.write(line)
    fin.close(); fout.close()





