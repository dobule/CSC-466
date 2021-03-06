# Name: Lucas Robertson
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Util.py
# Description: Provides utilities for parsing schema xml and csv data files

import numpy as np
import xml.etree.ElementTree as et
from C45Node import C45Node

SPLIT_ITERATIONS = 10 # For 10 fold cross evaluation
SPLIT_RATIO = 10


# Parses a .csv file containing rows of election data
# Returns a dictionary with the structure:
# { 'Bush Approval': array(['Approve', 'Disapprove', 'Approve', ...]),
#  ...
# }
def parse_data(file_name):
    data = np.genfromtxt(file_name, delimiter=',', 
                         dtype=str, skip_header=3)
    headers = np.genfromtxt(file_name, delimiter=',', dtype=str,  
                            skip_footer=len(data) + 2)
    dict = {}
    for i in range(len(headers)):
        dict[headers[i]] = data[:, i]

    return dict

# Parses an .xml schema file and returns all attribute labels 
# and options (unique).
# Returns a dictionary with the structure:
# { 'Bush Approval': array(['Approve', 'Disapprove']),
#  'Race': array(['Black', 'White', 'Other']),
#  ...
# }
def parse_attr(file_name):
    xml = et.parse(file_name).getroot().getchildren()
    attrs = {}
    for variable in xml:
        if variable.tag == "Category":
            continue
        class_name = variable.attrib['name']
        attrs[class_name] = [child.attrib['name'] 
                             for child in variable.getchildren()]

    return attrs


# Parses an .xml schema file and returns the categorizable variable 
# and class labels.
# Returns a tuple with the structure:
# ('Vote', ['Obama', 'Mccain'])
def parse_categ(file_name, use_numbers=False):
    xml = et.parse(file_name).getroot().find("Category")
    class_label = xml.attrib['name']
    if use_numbers:
        return class_label, [child.attrib['type'] 
                             for child in xml.getchildren()]
    else:
        return class_label, [child.attrib['name'] 
                             for child in xml.getchildren()]


# Parses a .csv attribute restrictions file and returns them as an array
def parse_rest(rest_file, data_file):
    
    val = np.genfromtxt(rest_file, delimiter=',', dtype=int)
    word = np.genfromtxt(data_file, delimiter=',', dtype=str,
                          max_rows=1)

    return dict(zip(word, val))

# Restricts attributes in data dictionary
def rest_attr(data, rest):
    for word in rest:
        if word in data.keys():
            data.pop(word)


def get_categ_label(csv_filename):
    csv_file = open(csv_filename, 'r')
    label = ''
    for i in range(3):
        label = csv_file.readline()

    return label.strip(' \t\n\r')


# Converts a dataset using strings to represent a value to using numbers
# based off of a dictionary of attributes.
def sanitize_data(attr, data, categ):

    for a in attr.keys():
        tempData = data[a]
        tempAttr = attr[a]

        if tempData[0].isdigit():
            tempData = tempData.astype(int) 
        else:
            for i in range(len(tempData)):
                tempData[i] = tempAttr.index(tempData[i]) + 1
  
        data[a] = tempData.astype(int)
        data[a] = data[a] - 1

   
    tempData = data[categ[0]]

    if not tempData[0].isdigit():
        for i in range(len(tempData)):
            tempData[i] = categ[1].index(tempData[i]) + 1


    data[categ[0]] = tempData.astype(int)
    data[categ[0]] = data[categ[0]] - 1

    return data


# Returns:
# [
#  {
#     training: {"gender": [...], "age": [...]},
#     validation: {"gender": [...], "age": [...]}
#  },
#  {
#     ...
#  },
#  ...
# ]
def split_data(input_data, n):
    data_sets = []
    if n == -1:
        data_sets.append(__build_ab1_set(input_data))
        return data_sets

    for i in range(n):
        data_sets.append(__build_set(input_data, n))

    return data_sets


# Builds one set of training and validation data from 'input_data'
def __build_set(input_data, n):
    training = {}
    validation = {}
    set_size = len(list(input_data.values())[0])
    slice_size = set_size // n
    rand_indices = []

    # Iterate until the number of values in rand_indices is the same size as one slice of the data set
    while len(rand_indices) < slice_size:
        rand_index = np.random.randint(set_size)
        # if the index already exists in rand_indices, skip it and try again
        if rand_index in rand_indices:
            continue

        # add the random index to rand_indices
        rand_indices.append(rand_index)

    for key in input_data:
        validation[key] = [input_data[key][i] for i in rand_indices]
        training[key] = np.delete(input_data[key], rand_indices)

    return {
        "training": training,
        "validation": validation
    }


def __build_ab1_set(input_data):
    training = {}
    validation = {}
    set_size = len(list(input_data.values())[0])
    index = np.random.randint(set_size)

    for key in input_data:
        validation[key] = input_data[key][index]
        training[key] = np.delete(input_data[key], index)

    return {
        "training": training,
        "validation": validation
    }


def tree_from_xml(xml_filename):
    xml = et.parse(xml_filename).getroot().getchildren()[0]
    return C45Node(xml)


def itemize_entry(data, idx):
    entry = {}
    for key in data:
        entry[key] = data[key][idx]

    return entry


def create_diagnostics(records_processed, correct="N/a", incorrect="N/a", accuracy="N/a", error_rate="N/a", errors="N/a"):
    return {
        'records_processed': records_processed,
        'correct': correct,
        'incorrect': incorrect,
        'accuracy': accuracy,
        'error_rate': error_rate,
        'errors': errors,
        'confusion_matrix': {
            "true_positives": 0,
            "true_negatives": 0,
            "false_positives": 0,
            "false_negatives": 0
        }
    }
