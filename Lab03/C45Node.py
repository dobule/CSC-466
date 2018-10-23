# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Node.py
# Description: Impliments the C4.5 classifier using information gain and
#  information gain ratio measures.

import numpy as np
import math
import xml.etree.ElementTree as et

DEFAULT_THRESHOLD = 0.6

class C45Node(object):

    def __init__(self):
        """
        Variables in all nodes:
            isLeaf  --  Boolean value that states whether the node is
                a leaf or not (if not then decision node)

        Variabls in decision nodes:
            children -- An array of other C45Nodes, with each index
                corresponding to a given attribute values at the same index in
                attrList.

            attribute -- The attribute that the node decides on as a string.

            attrList  -- A list of attribute values as strings, corresponding to
                the nodes in children.

        Variables in leaf nodes:
            p -- The proportion of data points with the leaf's choice value in
                the data set given to the leaf when it was created

            choice -- A tuple of the form (num, "str"), indicating the two
                corresponding choice values of the node.
        """
        
        self.children = []      # Contains children in ordered list
        self.attrList = []      # Holds the attr strings of the children
        self.isLeaf = False     # States whether the node is a leaf
        return


    def build_from_elem_tree(self, root_node):
        if root_node.tag == "decision":
            self.isLeaf = True
            self.choice = (root_node.attrib['end'], 
                           root_node.attrib['choice'])
            self.p = root_node.attrib['p']
            return

        self.attribute = root_node.attrib['var']
        self.isLeaf = False
        self.children = []
        self.attrList = []

        for edge in root_node.getchildren():
            newNode = C45Node()
            self.attrList.insert(int(edge.attrib['num']) - 1,
                                 edge.attrib['var'])

            self.children.insert(int(edge.attrib['num']) - 1,
                                 newNode)
            newNode.build_from_elem_tree(edge.getchildren()[0])

        return


    def classify(self, item):
        """
           Takes a datapoint and classifies it using the built-in tree

           item -- a dictionary of attribute : value pairs. Each value 
            should be a single integer or string.
        """

        node = self

        while node.isLeaf == False:
            itemAttrVal = item[node.attribute]
            if itemAttrVal.isdigit():
                node = node.children[int(itemAttrVal) - 1]
            else:
                node = node.children[node.attrList.index(itemAttrVal)]

        return node.choice


    def to_xml_tree(self, treeName):
        """
           Returns the tree as an xml element tree
        """

        xmlRoot = et.Element("Tree", name=treeName)
        C45Node.__to_xml_tree_r(self, xmlRoot)       
        C45Node.__indent_xml_tree(xmlRoot)
        return et.ElementTree(xmlRoot)


    @staticmethod
    def __to_xml_tree_r(C45Root, xmlRoot):
       

        if C45Root.isLeaf == True:
            idxOfDecision = int(C45Root.choice[0])
            decision =  et.SubElement(xmlRoot, "decision", 
                                      end=str(idxOfDecision), 
                                      choice=C45Root.choice[1], 
                                      p=str(C45Root.p))
            return decision

        xmlChild = et.SubElement(xmlRoot, "node", 
         var=C45Root.attribute)

        for child in C45Root.children:
            if type(child) is C45Node:
                idxOfChild = C45Root.children.index(child)
                xmlEdge = et.SubElement(xmlChild, "edge", 
                                        var=str(C45Root.attrList[idxOfChild]), 
                                        num=str(idxOfChild+1))
                C45Node.__to_xml_tree_r(child, xmlEdge)

        return xmlChild


    @staticmethod
    def __indent_xml_tree(elem, level=0):
        spacing = '\n' + level*'  '

        if len(elem):
            elem.text = spacing + '  '
            elem.tail = spacing
            children = list(elem)
            for child in children:
                C45Node.__indent_xml_tree(child, level+1)
            children[-1].tail = spacing
        else:
            elem.tail = spacing


    def C45_algorithm(self, attr, data, categ, threshold):
        """
        Constructs a decision tree using the C4.5 algorithm.

        attr -- Dictionary that contains an array of categories for each
            attribute.

        data -- a dictionary with the attribute being the key in data 
            and an array of all values in that attribute. Each datapoint 
            is in the same index across all attribute arrays.

        categ -- Tuple with attribute name in index 0 and an array of values
            that attribute in index 1. This parameter specifies the attribue
            that the decision tree classifies items into.

         threshold -- Information gain of an attribute must be greater than
            this number in order to split along that attribute.
        """

        # Check termination conditions
        if self.__check_homogenous_data(data[categ[0]]):
            self.__set_to_leaf(data[categ[0]], categ, homogenous=True)
            return
        elif len(attr.keys()) == 0:
            self.__set_to_leaf(data, categ)
            return

        # Select splitting attribute
        splitAttr = self.__select_splitting_attribute(attr, data, categ, threshold)

        if splitAttr is None:
            self.__set_to_leaf(data[categ[0]], categ)
        else:
            # Construct tree
            self.attribute = splitAttr
            self.attrList = attr[splitAttr]
            self.children = range(len(attr[splitAttr]))
            splitData = self.__split_dataset((splitAttr, attr[splitAttr]), data)
            newAttr = attr.copy()
            curAttr = newAttr.pop(splitAttr, None)

            for i in range(len(splitData)):
                if len(splitData[i][categ[0]]) > 0:
                    newNode = C45Node()
                    newNode.C45_algorithm(newAttr, splitData[i], categ, threshold)
                    self.children[i] = newNode 
                else:
                    newNode.__set_to_leaf(data[categ[0]], categ)
                    self.children[i] = newNode

        return


    @staticmethod
    def __check_homogenous_data(data):
        """ Returns True if all values in a list are equal. False otherwise. """
        firstVal = data[0]
        for val in data:
            if val != firstVal:
                return False
        return True


    def __set_to_leaf(self, data, categ, homogenous=False):
        """
           Sets the current node to a leaf.

           data -- A single array of values
        """

        self.isLeaf = True

        if homogenous == True:
            self.choice = (str(data[0] + 1), categ[1][data[0]])
            self.p = 1.0
        else:
            # self.choice is numeric to get p value
            self.choice = self.__find_most_frequent_label(data)
            unique, counts = np.unique(data, return_counts=True)
            countDict = dict(zip(unique, counts))
            self.p = float(countDict[self.choice]) / len(data)
            self.choice = (str(self.choice + 1), categ[1][self.choice])
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
        best = 0

        # Find the entropy for each attribute in data
        for a in attr.keys():
            pA[a] = C45Node.__entropy(data[categ[0]], data[a])
            gain[a] = p0 - pA[a]

        # Find attribute with best gain ratio
        best = max(gain, key=gain.get)

        if gain[best] > threshold:
            return best
        else:
            return None


    @staticmethod
    def __entropy(data, attr=None):
        """ Calculates the entropy of the array data. """
        if attr is None:
            return C45Node.__entropy_aux(data)
        else:
            # Separate data by attr array value
            datasets = {}
            for i in range(len(data)):
                if attr[i] in datasets.keys():
                    datasets[attr[i]].append(data[i])
                else:
                    datasets[attr[i]] = []
                    datasets[attr[i]].append(data[i]) 

            avgEnt = 0
            for ds in datasets.values():
               avgEnt = (avgEnt + 
                (float(len(ds)) / len(data) * C45Node.__entropy_aux(ds)))
 
            return avgEnt


    @staticmethod
    def __entropy_aux(data):
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
        # Get list of attributes from the data dictionary
        attrVals = data[attr[0]]

        # Initialize split data dictionaries
        for i in range(len(splitData)):
            dataPart = {}
            # Initialize keys in a data dictionary in splitData
            for key in data.keys():
                dataPart[key] = []
            splitData[i] = dataPart

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
