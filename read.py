# Nazlıcan Aka 2020400027
# Aslı Gök 2020400189
# Group 19

"""
Reading input from file is done here
Each line of input file is read and kept in necessary data structures to later use
"""

from machine import Machine
def read_input(FILENAME):

    file = open(FILENAME, "r")
    lines = list()
    for line in file:
        line = line.replace("\n","")
        lines.append(line)
        
    machine_number = int(lines[0])
    production_cycle_number = int(lines[1])
    factors = lines[2].split(" ")

    enhance_wear = int(factors[0])
    reverse_wear = int(factors[1])
    enhance_wear = int(factors[0])
    chop_wear = int(factors[2])
    trim_wear = int(factors[3])
    split_wear = int(factors[4])

    wear_dict = {"enhance": enhance_wear ,  # wear factor of each operation
    "reverse": reverse_wear,
    "chop":chop_wear,
    "trim": trim_wear,
    "split":split_wear,
    "add":0}

    machine_dict = dict()
    machine_list = list()
    threshold_value = int(lines[3])
    machine_id_list = list()
    parent_id_list = list()
    start_operation_list = list()
    child_list = list()
    
    # read input line by line in the format {machine id} {parent id} {start operation}
    for i in range(4, machine_number - 1 + 4):
        l = lines[i].split(" ")
        machine_id = int(l[0])
        machine_id_list.append(machine_id)
        parent_id = int(l[1])
        parent_id_list.append(parent_id)
        start_operation = l[2]
        start_operation_list.append(start_operation)
        machine = Machine(parent_id=parent_id, machine_id=machine_id, start_operation=start_operation,child_list = child_list, acc_wear = 0)
        machine_dict[machine_id] = machine
        machine_list.append(machine)
    
    # Add the root machine to the machine dictionary,
    # We assumed that parent id of the root machine is zero
    for i in parent_id_list:
      if i not in machine_id_list:
        root_machine = Machine(parent_id = 0, machine_id=i,start_operation= "add",child_list=[], acc_wear = 0)
        machine_dict[i] = root_machine
        machine_list.append(root_machine)
    # Create child list for each machine object
    for machine_id, machine in machine_dict.items():
        children_ids = [child_id for child_id, child_machine in machine_dict.items() if child_machine.parent_id == machine_id]
        machine.child_list = children_ids
    # Construct leaf machine list
    leaf_machines_lists = list()
    for child in machine_id_list:
        if child not in parent_id_list:
            leaf_machines_lists.append(child)

    # In the description, it says in the input file products received by leaf machines will be given in sorted order according to their machine ids.
    sorted_leaves = sorted(leaf_machines_lists)

    products_received_by_leaf_machines = list()
    for i in range((machine_number-1)+4, len(lines)):
        products_received_by_leaf_machines.append(lines[i])
    # Fetch leaf machine ids and products received by them 
    leaf_product_dict = dict()
    for leaf, product in zip(sorted_leaves, products_received_by_leaf_machines):
        leaf_product_dict[leaf] = product

    # Return values will be disributed to each machine by the control room in mpi.py
    return machine_number, production_cycle_number, wear_dict, threshold_value, machine_dict, leaf_product_dict, root_machine.machine_id

