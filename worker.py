# Nazlıcan Aka 2020400027
# Aslı Gök 2020400189
# Group 19

"""
The parallel factory production line logic of the project is implemented here
The messages will be sent to the control room, comm1
The machines can also communicate each other, comm2
"""
from mpi4py import MPI
import numpy as np
import sys
from methods import add,enhance,trim,split,chop,reverse


comm1 = MPI.Comm.Get_parent()
rank = comm1.Get_rank()

comm2 = MPI.COMM_WORLD

mydata_list = comm1.recv(source=0)
machine_rank_dict = comm1.recv(source=0)
my_dict = comm1.recv(source=0)

terminal_id = mydata_list[-1]
machine_n = mydata_list[0] # get the total machine number from the dictionary, it is the first element of the dictionary.
machine_id = my_dict["machine_id"]
mach = mydata_list[4][machine_id]
threshold = mydata_list[3]
wear_dict = mydata_list[2]

# the operation order for the odd and even machines are specified in the description which is used in this function
def change_operation(machine):
    if machine.machine_id == terminal_id:
        return machine.start_operation
    elif machine.machine_id % 2 == 1:
        operations_cycle = ["trim", "reverse"]
    else:
        operations_cycle = ["split", "chop", "enhance"]

    current_index = operations_cycle.index(machine.start_operation)
    next_index = (current_index + 1) % len(operations_cycle)
    machine.start_operation = operations_cycle[next_index]

    return machine.start_operation

# find the operation and get the functionality from methods.py
def helper(mach, input_str):
  if mach.start_operation == "enhance":
    return enhance(input_str)
  elif mach.start_operation == "split":
    return split(input_str) 
  elif mach.start_operation == "chop":
    return chop(input_str) 
  elif mach.start_operation == "trim":
    return trim(input_str) 
  else:
    return reverse(input_str)

pro_dict = mydata_list[5]

# calculate the maintenance cost
def cost_cal(threshold, wear_dict, machine, last_operation):
  cost = (machine.acc_wear - threshold + 1) * wear_dict[last_operation]
  return cost

# this is the function that provides operation functionality to the machines
# results of operations calculated
# results are sent to its parent
# If the machine is root machine, result is sent to the control room 
def do_operation(machine, pro_dict,machine_rank_dict,machine_n, threshold, wear_dict):
  # if leaf machine
  if len(machine.child_list) == 0:
    initial_product = pro_dict[machine.machine_id]
    added_product = add([initial_product])
    will_be_send_str = helper(mach, added_product)
    machine.acc_wear += wear_dict[machine.start_operation]
    parent_rank = machine_rank_dict[machine.parent_id]
    sender_machine_id = machine.machine_id
    will_list = [sender_machine_id, will_be_send_str]
    # send the result string to its parent
    comm2.send(will_list, dest=parent_rank, tag = 1)
    change_operation(machine)

  else:
    # root machine 
    # only add operation and send the final product to the main control room
    if(machine_rank_dict[machine.machine_id]== machine_n-1):
      input_list = list() # ex: [5, IE]
      all_input = list() # ex: [[8, 'EI'], [13, 'OX']]
      sorted_input = list()
      for i in range(len(machine.child_list)):
        input_list = comm2.recv(source=machine_rank_dict[machine.child_list[i]], tag = 1)
        all_input.append(input_list)
      sorted_all_input = sorted(all_input, key=lambda x: x[0])
      for inp in sorted_all_input:
        sorted_input.append(inp[1])  
      added_product = add(sorted_input)
      return added_product
    # not root machine and not leaf machine
    else:
      input_list = list() # ex: [5, IE]
      all_input = list() # ex: [[8, 'EI'], [13, 'OX']]
      sorted_input = list()
      for i in range(len(machine.child_list)):
        input_list = comm2.recv(source=machine_rank_dict[machine.child_list[i]], tag = 1)
        all_input.append(input_list)
        sorted_all_input = sorted(all_input, key=lambda x: x[0])
      for inp in sorted_all_input:
        sorted_input.append(inp[1])
      added_product = add(sorted_input)
      will_be_send_str = helper(mach, added_product)
      machine.acc_wear += wear_dict[machine.start_operation]
      parent_rank = machine_rank_dict[machine.parent_id]
      sender_machine_id = machine.machine_id
      will_list = [sender_machine_id, will_be_send_str]
      comm2.send(will_list, dest=parent_rank, tag = 1)
      change_operation(machine)

# repeat the production production_cycle_number times  
for i in range(mydata_list[1]):
  last_operation = mach.start_operation
  final_product = do_operation(mach,pro_dict=pro_dict, machine_rank_dict=machine_rank_dict, machine_n= machine_n, threshold=threshold, wear_dict=wear_dict)
  comm1.send(final_product, dest=0, tag = 2)
  # if accumulated wear >= threshold send the maintenance message to the control room
  if mach.acc_wear >= threshold:
        cost = cost_cal(threshold, wear_dict, mach,last_operation=last_operation)
        msg_maintenance = str(mach.machine_id) + "-" + str(cost) + "-" + str(i+1)
        comm1.send(msg_maintenance, dest =0, tag=3)
        mach.acc_wear = 0  # reset accumulated wear after sending the maintenance msg
  


