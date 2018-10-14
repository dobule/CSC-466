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
   #  ...
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
   #  'Race': array(['Black', 'White', 'Other']),
   #  ...
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


   # Converts a dataset using strings to represent a value to using numbers
   # based off of a dictionary of attributes.
   @staticmethod
   def sanitize_data(attr, data):
      
      for a in attr.keys():
         tempData = data[a]
         tempAttr = attr[a]

         for i in range(len(data))
            if tempData[i].isdigit():
               tempData[i] = ord(tempData[i]) - 1
            else:
               tempData[i] = tempAttr.index(tempData[i]) 
         data[a] = tempData
      
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

   # indent function courtesy of user ade on this stack overflow post: https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
   # (user profile: https://stackoverflow.com/users/97238/ade)
   def __indent(elem, level=0):
     i = "\n" + level*"  "
     j = "\n" + (level-1)*"  "
     if len(elem):
        if not elem.text or not elem.text.strip():
           elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
           elem.tail = i
        for subelem in elem:
           indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
           elem.tail = j
     else:
        if level and (not elem.tail or not elem.tail.strip()):
           elem.tail = j
     return elem

   def write_tree(c45root, tree_name):
     xml_root = et.Element("Tree", name=tree_name)
     __write_tree_r(c45root, xml_root)
     __indent(xml_root)
     tree = et.ElementTree(xml_root)
     tree.write("test.xml")

   def __write_tree_r(c45root, xml_root):
     if c45root.isLeaf:
        et.SubElement(xml_root, "decision", choice=c45root.choice)
        return

     xml_child = et.SubElement(xml_root, "node", var=c45root.attribute)
     for child_key in c45root.children:
        child = c45root.children[child_key]
        xml_edge = et.SubElement(xml_child, "edge", var=child_key)
        write_tree_r(child, xml_edge)
