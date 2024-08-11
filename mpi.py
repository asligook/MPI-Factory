# Nazlıcan Aka 2020400027
# Aslı Gök 2020400189
# Group 19

#from re import T
from mpi4py import MPI
import numpy as np
import sys
from read import read_input

# create the communication world that will be responsible for the communication between the control room and machines
comm1 = MPI.COMM_WORLD

rank = comm1.Get_rank()

# get the input and output file names from the command line input
FILENAME = sys.argv[1]
OUTFILE = sys.argv[2]

# take the values read by the input file with read_input function
# the control room will send this information as a list to each machine in the production line
machine_number, production_cycle_number, wear_dict, threshold_value, machine_dict, leaf_product_dict, root_id = read_input(FILENAME)
data_list = [machine_number, production_cycle_number, wear_dict, threshold_value, machine_dict, leaf_product_dict, root_id]

# this is the key part of the project
# all machines in the production line will be spawned as seperate processes by the control room
# this spwan function provides the parallelism functionality of the program
comm1 = comm1.Spawn(sys.executable, args=['worker.py'], maxprocs=machine_number)
size = comm1.Get_size()

# create a dictionary to fecth machine_id with process_id (rank of the process created by spawn)
machine_process_fetch_dict = dict()
machine_process_fetch_dict = dict(zip(machine_dict.keys(), range(machine_number)))

for i in range(0, machine_number):
  comm1.send(data_list, dest = i)
  comm1.send(machine_process_fetch_dict, dest = i)

# send all machines the machine id and process rank information
for machine_id, process_rank in machine_process_fetch_dict.items():
  comm1.send({"machine": machine_dict[machine_id], 
              "machine_id": machine_id,
              "process_rank": process_rank}, dest=process_rank)

# open the output file
file_out = open(OUTFILE,"w")
source_process = None

for machine in machine_dict.values():
  if machine.parent_id == 0:
    source_process = machine_process_fetch_dict[machine.machine_id]

# take the final product after each production cycle
for i in range(production_cycle_number):
  final_product = comm1.recv(source=source_process,tag=2)
  # write the final product to the output file
  file_out.write(f"{final_product}\n")


# check whether there is a maintenance message coming from a machine
# for the maintenance messages, the tag is 3 
while comm1.Iprobe(source=MPI.ANY_SOURCE, tag=3):
    request = comm1.recv(source=MPI.ANY_SOURCE, tag=3)
    file_out.write(f"{request}\n")

file_out.close()

