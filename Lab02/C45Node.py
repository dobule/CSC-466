# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Node.py
# Description: Impliments the C4.5 classifier using information gain and
#  information gain ratio measures.

import math
import xml.etree.ElementTree as et

class C45Node:

    def __init__(self, attr, data, categ, threshold):
        """
             Constructor for C45Node

             attr -- Dictionary that contains an array of categories for each
                attribute.

             data -- a dictionary with the attribute being the key in data and an
                array of all values in that attribute. Each datapoint is in the same
                index across all attribute arrays.

             categ -- Tuple with attribute name in index 0 and an array of values
                that attribute in index 1. This parameter specifies the attribue
                that the decision tree classifies items into.

             threshold -- Information gain of an attribute must be greater than
                this number in order to split along that attribute.
          """
        self.children = {}
        self.isLeaf = False
        self.__C45_algorithm(attr, data, categ, threshold)
        return

    def __init__(self, xml_node):
        if xml_node.tag == "decision":
            self.isLeaf = True
            self.choice = xml_node.attrib['choice']
            #self.p = xml_node.attrib['p']
            return

        self.attribute = xml_node.attrib['var']
        self.isLeaf = False
        self.children = {}

        for edge in xml_node.getchildren():
            self.children[edge.attrib['var']] = C45Node(edge.getchildren()[0])

        return

    def classify(self, item):
        """
           Takes a datapoint and classifies it using the built-in tree

           item -- a dictionary or attribute : value pairs
        """

        if self.isLeaf == True:
            return self.choice

        return self.children[item[self.attribute]].classify(item)

    def to_xml_string(self, p=1.0):
        """
           Returns the tree as a string formatted in XML
        """
        return

    def __C45_algorithm(self, attr, data, categ, threshold):
        """
           Constructs a decision tree using the C4.5 algorithm.
        """

        # Check termination conditions
        if self.__check_homogenous_data(data[categ[0]]):
            self.__set_to_leaf(data[categ], categ, homogenous=True)
            return
        elif len(attr.keys()) == 0:
            self.__set_to_leaf(data, categ)
            return

        # Select splitting attribute
        splitAttr = self.__select_splitting_attribute(attr, data, threshold)

        if splitAttr == None:
            self.__set_to_leaf(data[categ[0]], categ)
        else:
            # Construct tree
            self.attribute = splitAttr
            splitData = self.__split_dataset(data, splitAttr)
            attr.pop(splitAttr, None)

            for val, dataSet in splitData:
                self.__add_child(val, attr, dataSet, categ, threshold)

        return

    def __check_homogenous_data(data):
        """ Returns True if all values in a list are equal. False otherwise. """
        firstVal = data[0]
        for val in data:
            if val != firstVal:
                return False
        return True

    def __set_to_leaf(self, data, homogenous=False):
        """
           Sets the current node to a leaf.

           data -- An array of values
        """

        self.isLeaf = True

        if homogenous == True:
            self.choice = data[0]
            self.p = 1.0
        else:
            self.choice = self.__find_most_frequent_label(data)
            self.p = float(data.count(self.value)) / len(data)

        return

    def __add_child(self, val, attr, data, categ, threshold):
        """ Adds a child to current node """
        node = C45Node(attr, data, categ, threshold)
        self.children[val] = node
        return

    def __find_most_frequent_label(self, data):
        """
           Finds the most frequent label in array 'data'.
        """

        hist = self.__histogram(data)
        return max(hist, key=hist.get)

    def __select_splitting_attribute(self, attr, data, categ, threshold):
        """
           Returns the attribute that is most apt for splitting the dataset.
        """

        # Find the entropy for the category in data
        p0 = self.__entropy(data[categ[0]])
        pA = {}
        gain = {}
        gainRatio = {}

        # Find the entropy for each attribute in data
        for a in attr.keys():
            pA[a] = self.__entropy(data[a])
            gain[a] = p0 - pA[a]
            gainRatio[a] = gain[a] / pA[a]

        # Find attribute with besst gain ratio
        best = max(gainRatio, key=gainRatio.get)

        if gain[best] > threshold:
            return best
        else:
            return None

    def __entropy(self, data):
        """ Calculates the entropy of the array data """

        hist = self.__histogram(data)
        sumProb

        for val in hist.values():
            prob = float(val) / len(data)
            sumProb = prob * math.log(prob, 2)

        return -1 * sumProb

    def __split_dataset(self, attr, data):
        """
           Splits data into multiple data sets based on attr tuple.

           attr -- A tuple with the attribute name in index 0 and the values
              of the attribute as a list in index 1

           data -- The standard data
        """

        # Dictionary with keys from attr[1] and values being data dictionaries
        splitData = {}
        # Remove the list of attributes from the data dictionary
        attrVals = data.pop(attr[0])

        # Initialize split data dictionaries
        for val in attr[1]:
            splitData[val] = {}
            # Initialize keys in a data dictionary in splitData
            for key in data.keys():
                splitData[val][key] = []

        # Iterate over indecies of data values
        for i in range(len(attrVals)):
            # Find the data set to add to
            dataSet = splitData[attrVals[i]]

            # Iterate over key values pairs in data and add data points
            for key, val in data:
                dataSet[key].append(data[i])

            splitData[attrVals[i]] = dataSet

        return splitData

    def __histogram(self, data):
        """ Creates histogram from data array. Returns as dict """
        hist = {}

        for val in data:
            if val in hist.keys():
                hist[val] = hist[val] + 1
            else:
                hist[val] = 1

        return hist
