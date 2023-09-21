#!/bin/bash
#by ishida 2022/10

#------ pjsub option --------#
#PJM -L rscgrp=short
#PJM -L node=1
#PJM --mpi proc=56
#PJM -L elapse=2:00:00
#PJM -g gy29
#PJM -j
#PJM -m e



#mpiexec.hydra -n ${PJM_MPI_PROC} ./fvcom --casename Tokyo
module load hdf5 
module load netcdf-fortran 
module load netcdf 

export HOME=/work/gy29/y29007

export LD_LIBRARY_PATH="${HOME}/Github/fvcom442/FVCOM_source/libs/install/lib:$LD_LIBRARY_PATH"

mpiexec.hydra -n ${PJM_MPI_PROC} ./fvcom --casename Tokyo3

