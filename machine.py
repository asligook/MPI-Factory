# Nazlıcan Aka 2020400027
# Aslı Gök 2020400189
# Group 19

"""
Define the machine class to represent machine object
Machine' s attributes are: its parent id, its machine id, 
its next operation, its child list and its accumulated wear
"""
class Machine:
    def __init__(self, parent_id, machine_id, start_operation, child_list, acc_wear):
        self.parent_id = parent_id
        self.machine_id = machine_id
        self.start_operation = start_operation
        self.child_list = child_list
        self.acc_wear = acc_wear

    def display_info(self):
        print(f"Parent ID: {self.parent_id}")
        print(f"Machine ID: {self.machine_id}")
        print(f"Start Operation: {self.start_operation}")
        print(f"Child list: {self.child_list}")
        print(f"accumulator wear: {self.acc_wear}")

    