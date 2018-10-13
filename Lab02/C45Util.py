# Name: Lucas Robertson
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Util.py
# Description: Provides utilities for parsing schema xml and csv data files

import numpy as np
import xml.etree.ElementTree as et

SPLIT_ITERATIONS = 10 # For 10 fold cross evaluation
SPLIT_RATIO = 10

class C45Util:
    # Parses a .csv file containing rows of election data
    # Returns a dictionary with the structure:
    # { 'Bush Approval': array(['Approve', 'Disapprove', 'Approve', ...]),
    #   ...
    # }
    @staticmethod
    def parse_data(file_name):
        data = np.genfromtxt(file_name, delimiter=',', dtype=str, skip_header=3)
        headers = np.genfromtxt(file_name, delimiter=',', dtype=str,  skip_footer=len(data) + 2)
        dict = {}
        for i in range(len(headers)):
            dict[headers[i]] = data[:, i]

        return dict

    # Parses an .xml schema file and returns all attribute labels and options (unique)
    # Returns a dictionary with the structure:
    # { 'Bush Approval': array(['Approve', 'Disapprove']),
    #   'Race': array(['Black', 'White', 'Other']),
    #   ...
    # }
    @staticmethod
    def parse_attr(file_name):
        xml = et.parse(file_name).getroot().getchildren()
        dict = {}
        for variable in xml:
            if variable.tag == "Category":
                continue
            class_name = variable.attrib['name']
            dict[class_name] = [child.attrib['name'] for child in variable.getchildren()]

        return dict

    # Parses an .xml schema file and returns the categorizable variable and class labels
    # Returns a tuple with the structure:
    # ('Vote', ['Obama', 'Mccain'])
    @staticmethod
    def parse_categ(file_name, use_numbers=False):
        xml = et.parse(file_name).getroot().find("Category")
        dict = {}
        class_label = xml.attrib['name']
        if use_numbers:
            return (class_label, [child.attrib['type'] for child in xml.getchildren()])
        else:
            return (class_label, [child.attrib['name'] for child in xml.getchildren()])


    # Returns:
    # [
    #   {
    #       training: {"gender": [...], "age": [...]},
    #       validation: {"gender": [...], "age": [...]}
    #   },
    #   {
    #       ...
    #   },
    #   ...
    # ]
    @staticmethod
    def split_data(input_data):
        datasets = []
        for i in range(SPLIT_ITERATIONS):
            datasets.append(C45Util.__build_set(input_data))

        return datasets


    # Builds one set of training and validation data from 'input_data'
    @staticmethod
    def __build_set(input_data):
        training = {}
        validation = {}
        set_size = len(input_data.values()[0])
        validation_count = set_size // SPLIT_RATIO
        rand_indexes = []
        while len(rand_indexes) < validation_count:
            rand_index = np.random.randint(set_size)
            if rand_index in rand_indexes:
                continue
            rand_indexes.append(rand_index)

        for key in input_data:
            validation[key] = [input_data[key][i] for i in rand_indexes]
            training[key] = np.delete(input_data[key], rand_indexes)

        return {
            "training": training,
            "validation": validation
        }

    @staticmethod
    def tree_from_xml(xml_filename):
        xml = et.parse(xml_filename).getroot()
        return C45Node(xml)
