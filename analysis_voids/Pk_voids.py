import numpy as np
import sys,os
import MAS_library as MASL
import Pk_library as PKL

################################## INPUT ######################################
grid    = 512    #size of the density field
BoxSize = 1000.0 #Mpc/h
MAS     = 'CIC'  #Mass assignment scheme
axis    = 0      #axis along which RSD are place
threads = 8      #openmp threads

fin     = 'VIDE_voids1_z=0.txt'
fout1   = 'Pk_voids1_z=0.txt'
fout2   = 'Pk_voids1_volume-weighted_z=0.txt'
###############################################################################

# read voids positions and volumes
pos, vol = np.loadtxt(fin, unpack=True)

# compute the density field of voids
delta = np.zeros((grid,grid,grid), dtype=np.float32)
MASL.MA(pos, delta, BoxSize, MAS)
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

# compute Pk of voids
Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads)
np.savetxt(fout1, np.transpose([Pk.k3D, Pk.Pk[:,0]]))


# compute the density field of volume-weighted voids
delta = np.zeros((grid,grid,grid), dtype=np.float32)
MASL.MA(pos, delta, BoxSize, MAS, W=vol)
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

# compute Pk of voids
Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads)
np.savetxt(fout2, np.transpose([Pk.k3D, Pk.Pk[:,0]]))
