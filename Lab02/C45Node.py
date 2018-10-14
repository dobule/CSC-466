# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Node.py
# Description: Impliments the C4.5 classifier using information gain and
#  information gain ratio measures.

import numpy as np
import math
import xml.etree.ElementTree as et

class C45Node(object):

    def __init__(self):
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
        self.children = []
        self.isLeaf = False
        return


    def build_from_xml(self, xml_node):
        if xml_node.tag == "decision":
            self.isLeaf = True
            self.choice = xml_node.attrib['choice']
            #self.p = xml_node.attrib['p']
            return

        self.attribute = xml_node.attrib['var']
        self.isLeaf = False
        self.children = []

        for edge in xml_node.getchildren():
            newNode = C45Node()
            self.children.append(newNode.build_from_xml(edge.getchildren()[0]))

        return


    def classify(self, item):
        """
           Takes a datapoint and classifies it using the built-in tree

           item -- a dictionary or attribute : value pairs
        """

        node = self

        while node.isLeaf == False:
            node = node.children[item[node.attribute]].classify(item)

        return node.choice

    def to_xml_tree(self, treeName, attr):
        """
           Returns the tree as an xml element tree
        """

        xmlRoot = et.Element("Tree", name=treeName)
        C45Node.__to_xml_string_r(self, xmlRoot, attr)       
        C45Util.__indent(xmlRoot)
        return et.ElementTree(xmlRoot) 

    @staticmethod
    def __to_xml_tree_r(C45Root, xmlRoot, attr):
        if C45Root.isLeaf == True:
            return et.SubElement(xmlRoot, "decision",
             choice=C45Root.choice, p=C45Root.p)

        xmlChild = et.SubElement(xmlRoot, "node", 
         choice=C45Root.attribute)

        varArr = attr[C45Root.attribute]

        for child in C45Root.children:
            idxOfChild = C45Root.children.index(child)
            xmlEdge = et.SubElement(xmlChild, "edge", var=varArr[idxOfChild],
             num=idxOfChild+1)
            C45Node.__to_xml_string(child, xmlEdge, attr)


    def C45_algorithm(self, attr, data, categ, threshold):
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
        splitAttr = self.__select_splitting_attribute(attr, data, categ, threshold)

        if splitAttr == None:
            self.__set_to_leaf(data[categ[0]], categ)
        else:
            # Construct tree
            self.attribute = splitAttr
            self.children = range(len(attr[splitAttr]))
            splitData = self.__split_dataset(data, splitAttr)
            attr.pop(splitAttr, None)

            for val, dataSet in splitData:
                newNode = C45Node()
                newNode.C45_algorithm(attr, dataSet, categ, threshold)
                self.children[attr[splitAttr].index(val)] = newNode 

        return

    @staticmethod
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
            unique, counts = np.unique(data, return_counts=True)
            countDict = dict(zip(unique, counts))
            self.p = float(countDict[self.choice]) / len(data)

        return

    def __add_child(self, attr, data, categ, threshold, idx):
        """ Adds a child to current node """
        node = C45Node(attr, data, categ, threshold)
        self.children[idx] = node
        return

    @staticmethod
    def __find_most_frequent_label(data):
        """
           Finds the most frequent label in array 'data'.
        """

        hist = C45Node.__histogram(data)
        return max(hist, key=hist.get)

    @staticmethod
    def __select_splitting_attribute(attr, data, categ, threshold):
        """
           Returns the attribute that is most apt for splitting the dataset.
        """

        # Find the entropy for the category in data
        p0 = C45Node.__entropy(data[categ[0]])
        pA = {}
        gain = {}
        gainRatio = {}

        # Find the entropy for each attribute in data
        for a in attr.keys():
            pA[a] = C45Node.__entropy(data[a])
            gain[a] = p0 - pA[a]
            gainRatio[a] = gain[a] / pA[a]

        # Find attribute with besst gain ratio
        best = max(gainRatio, key=gainRatio.get)

        if abs(gain[best]) > threshold:
            return best
        else:
            return None


    @staticmethod
    def __entropy(data):
        """ Calculates the entropy of the array data """

        hist = C45Node.__histogram(data)
        sumProb = 0

        for val in hist.values():
            prob = float(val) / len(data)
            sumProb = sumProb + prob * math.log(prob, 2)

        return -1 * sumProb


    @staticmethod
    def __split_dataset(attr, data):
        """
           Splits data into multiple data sets based on attr tuple.

           attr -- A tuple with the attribute name in index 0 and the values
              of the attribute as a list in index 1

           data -- The standard data
        """

        # An array the same length as attr[1] and values being data dictionaries
        splitData = range(len(attr[1]))
        # Remove the list of attributes from the data dictionary
        attrVals = data.pop(attr[0])

        # Initialize split data dictionaries
        for idx in range(len(splitData)):
            dataPart = {}
            # Initialize keys in a data dictionary in splitData
            for key in data.keys():
                dataPart[key] = []
            splitData[idx] = dataPart

        # Iterate over indecies of data values
        for i in range(len(attrVals)):
            # Find the data set to add to
            dataSet = splitData[int(attrVals[i])]

            # Iterate over key values pairs in data and add data points
            for key in data.keys():
                dataSet[key].append(data[key][i])
            
            splitData[int(attrVals[i])] = dataSet

        return splitData

    
    @staticmethod
    def __histogram(data):
        """ Creates histogram from data array. Returns as dict """
        hist = {}

        for val in data:
            if val in hist.keys():
                hist[val] = hist[val] + 1
            else:
                hist[val] = 1

        return hist
