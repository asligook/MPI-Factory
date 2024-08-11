# Nazlıcan Aka 2020400027
# Aslı Gök 2020400189
# Group 19

"""
These function are operations of the machines
This file is used in worker.py
"""

def add(str_list):
    return ''.join(str_list)

def enhance(input_str):
    first_letter = input_str[0]
    last_letter = input_str[-1]
    middle_str = input_str[1: -1]
    if(len(input_str) == 1):
      return 3*input_str
    else:
      return first_letter*2 + middle_str + last_letter*2

def reverse(input_string):
    return input_string[::-1]

def chop(input_string):
    if len(input_string) > 1:
        return input_string[:-1]
    else:
        return input_string

def trim(input_string):
    if len(input_string) > 2:
        return input_string[1:-1]
    else:
        return input_string

def split(input_string):
    length = len(input_string)
    if length > 1:
        split_index = length // 2 if length % 2 == 0 else (length + 1) // 2
        return input_string[:split_index]
    else:
        return input_string
