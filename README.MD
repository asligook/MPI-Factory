This project is implemented using Python. 
Make sure that Python version is 3.7+. You can check your python version with the command "python --version" or if you have python3 you can use the command "python3 --version".

Required imports:
from mpi4py import MPI
import numpy as np
import sys

If mpiexec is installed on the machine, you can use this command to run the project, change the python3 to python if necessary:
mpiexec --allow-run-as-root --map-by :OVERSUBSCRIBE -n 1 python3 mpi.py input.txt output.txt

As an alternative, we used Google Collab environment. To run the project in Collab we used the following commands:
!apt-get install -y mpich
!pip install mpi4py
!mpiexec --allow-run-as-root --map-by :OVERSUBSCRIBE -n 1 python mpi.py input.txt output.txt

Change input-output.txt names with your intended file names.


