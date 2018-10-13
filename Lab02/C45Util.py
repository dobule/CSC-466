import numpy as np
import xml.etree.ElementTree as et

class C45Util:

    # Parses a .csv file containing rows of election data
    # Returns a dictionary with the structure:
    # { 'Bush Approval': array(['Approve', 'Disapprove', 'Approve', ...]),
    #   ...
    # }
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
    def parse_class(file_name, use_numbers=False):
        xml = et.parse(file_name).getroot().find("Category")
        dict = {}
        class_label = xml.attrib['name']
        if use_numbers:
            return (class_label, [child.attrib['type'] for child in xml.getchildren()])
        else:
            return (class_label, [child.attrib['name'] for child in xml.getchildren()])
