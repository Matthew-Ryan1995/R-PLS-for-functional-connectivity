#!/bin/bash
#SBATCH -p batch            	                             # partition (this is the queue your job will be added to)
#SBATCH -N 1               	                                # number of nodes (no MPI, so we only use a single node)
#SBATCH -n 10          	                                # number of cores
#SBATCH --time=00:40:00    	                                # walltime allocation, which has the format (D-HH:MM:SS), here set to 1 hour
#SBATCH --mem=5GB         	                                # memory required per node (here set to 4 GB)

# Notification configuration
#SBATCH --array=1-340
#SBATCH --mail-type=END					    	# Send a notification email when the job is done (=END)
#SBATCH --mail-user=matthew.ryan@adelaide.edu.au  	# Email to which notifications will be sent

#loading modules
module load arch/haswell
module load R/3.6.0-foss-2016b
export R_LIBS_USER=/hpcfs/users/a1668286/local/RLibs

# Execute the program

Rscript code/vip_cobre_aal_model.R
