#!/bin/bash
#SBATCH -J void_wiggles
#SBATCH -n 168
#SBATCH -t 07-00:00:00 
#SBATCH --exclusive        
#SBATCH -o OUTPUT.o%j             
#SBATCH -e OUTPUT.e%j                 
#SBATCH --mail-user=villaescusa.francisco@gmail.com     
#SBATCH --mail-type=ALL  
####SBATCH -p preempt --qos=preempt
#SBATCH -p cca --qos=cca


#root="/mnt/ceph/users/fvillaescusa/Christina_voids/COLA_runs/wiggles/"
root="/mnt/ceph/users/fvillaescusa/Christina_voids/COLA_runs/no-wiggles/"
COLA="/mnt/ceph/users/fvillaescusa/Christina_voids/COLA_runs/l-picola/L-PICOLA"
G3="/mnt/ceph/users/fvillaescusa/Christina_voids/COLA_runs/g3_new/P-Gadget3"

for i in {0..99} 
do
    # go to the folder
    folder=$root$i
    cd $folder
    
    # run COLA
    module purge
    module load slurm
    module load gcc
    module load openmpi2
    module load lib/fftw3/3.3.6-pl1-openmpi2
    module load lib/gsl
    mpirun $COLA COLA.params >> logfile

    # change files names
    for snapnum in 0 1
    do
	if [ $snapnum = 0 ]
	then
	    z=1
	fi

	if [ $snapnum = 1 ]
	then
	    z=0
	fi

	snapdir=$folder'/snapdir_00'$snapnum'/'
	mkdir $snapdir

	for j in {0..159}
	do
	    f1=$folder'/snap_z'$z'p000.'$j
	    f2=$snapdir'snap_00'$snapnum'.'$j
	    mv $f1 $f2
	done
    done

    # run FoF
    module purge
    module load slurm
    module load gcc
    module load openmpi
    module load lib/fftw2/2.1.5-openmpi1
    module load lib/gsl
    mpirun $G3 ../G3.param 3 0 >> logFoF
    mpirun $G3 ../G3.param 3 1 >> logFoF

    # remove unnecesary files
    rm ewald_* free_* G3.param-usedvalues memory* parameters-usedvalues PIDs.txt processes_* ps_* snap_*.info

done




